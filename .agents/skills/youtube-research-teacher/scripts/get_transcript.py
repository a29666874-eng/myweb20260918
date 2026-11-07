#!/usr/bin/env python3
"""取得 YouTube 公開影片已存在的字幕（只拿文字，不下載影片或音訊）。

用法：
  python3 get_transcript.py --check
  python3 get_transcript.py <網址或影片ID> [--lang zh-Hant,zh-TW,zh,en] [--timestamps]

依序嘗試免費工具：youtube-transcript-api → yt-dlp（--skip-download）。
本腳本不會自動安裝任何套件，也不會使用付費 API。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ID_RE = re.compile(r"(?:v=|youtu\.be/|shorts/|embed/|live/)([A-Za-z0-9_-]{11})")


def video_id(text: str) -> str | None:
    text = text.strip()
    if re.fullmatch(r"[A-Za-z0-9_-]{11}", text):
        return text
    m = ID_RE.search(text)
    return m.group(1) if m else None


def fmt_time(sec: float) -> str:
    sec = int(sec)
    h, rem = divmod(sec, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def tools_status() -> dict[str, bool]:
    return {
        "youtube-transcript-api": importlib.util.find_spec("youtube_transcript_api") is not None,
        "yt-dlp": shutil.which("yt-dlp") is not None
        or importlib.util.find_spec("yt_dlp") is not None,
    }


def via_transcript_api(vid: str, langs: list[str]) -> list[dict]:
    from youtube_transcript_api import YouTubeTranscriptApi  # type: ignore

    if hasattr(YouTubeTranscriptApi, "get_transcript"):  # 舊版 < 1.0
        data = YouTubeTranscriptApi.get_transcript(vid, languages=langs)
        return [{"start": d["start"], "text": d["text"]} for d in data]
    data = YouTubeTranscriptApi().fetch(vid, languages=langs)  # 新版 >= 1.0
    return [{"start": s.start, "text": s.text} for s in data]


def parse_vtt(path: Path) -> list[dict]:
    out: list[dict] = []
    start = None
    last = ""
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"(\d+):(\d{2}):(\d{2})[.,]\d+\s+-->", line) or re.match(
            r"()(\d{2}):(\d{2})[.,]\d+\s+-->", line
        )
        if m:
            h = int(m.group(1) or 0)
            start = h * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            continue
        text = re.sub(r"<[^>]+>", "", line).strip()
        if not text or start is None or text == last or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        out.append({"start": start, "text": text})
        last = text
    return out


def via_ytdlp(vid: str, langs: list[str]) -> list[dict]:
    exe = shutil.which("yt-dlp")
    cmd = [exe] if exe else [sys.executable, "-m", "yt_dlp"]
    with tempfile.TemporaryDirectory() as tmp:
        cmd += [
            "--skip-download",  # 絕不下載影片／音訊
            "--write-subs",
            "--write-auto-subs",
            "--sub-langs", ",".join(langs),
            "--sub-format", "vtt",
            "-o", str(Path(tmp) / "%(id)s.%(ext)s"),
            f"https://www.youtube.com/watch?v={vid}",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        files = sorted(Path(tmp).glob("*.vtt"))
        if not files:
            raise RuntimeError((r.stderr or r.stdout).strip()[-500:] or "沒有可用字幕")
        for lang in langs:  # 依語言偏好挑檔案
            for f in files:
                if f.name.endswith(f".{lang}.vtt"):
                    return parse_vtt(f)
        return parse_vtt(files[0])


def main() -> int:
    ap = argparse.ArgumentParser(description="取得 YouTube 公開字幕（只拿文字）")
    ap.add_argument("url", nargs="?", help="YouTube 網址或 11 碼影片 ID")
    ap.add_argument("--lang", default="zh-Hant,zh-TW,zh-Hans,zh,en", help="語言偏好，逗號分隔")
    ap.add_argument("--timestamps", action="store_true", help="每行前面加時間點")
    ap.add_argument("--check", action="store_true", help="只檢查可用工具")
    ap.add_argument("--json", action="store_true", help="輸出 JSON")
    a = ap.parse_args()

    status = tools_status()
    if a.check:
        print(json.dumps(status, ensure_ascii=False, indent=2))
        if not any(status.values()):
            print("沒有找到免費字幕工具。可請使用者在 YouTube 點「顯示轉錄稿」複製貼上，"
                  "或在徵得同意後安裝：pip install youtube-transcript-api", file=sys.stderr)
        return 0

    if not a.url:
        ap.error("請提供 YouTube 網址或影片 ID")
    vid = video_id(a.url)
    if not vid:
        print("錯誤：看不懂這個網址，找不到影片 ID。", file=sys.stderr)
        return 2
    langs = [x.strip() for x in a.lang.split(",") if x.strip()]

    errors = []
    for name, fn in (("youtube-transcript-api", via_transcript_api), ("yt-dlp", via_ytdlp)):
        if not status[name]:
            errors.append(f"{name}: 未安裝")
            continue
        try:
            segs = fn(vid, langs)
            if segs:
                if a.json:
                    print(json.dumps({"video_id": vid, "source": name, "segments": segs},
                                     ensure_ascii=False))
                else:
                    print(f"# video_id={vid} source={name}")
                    for s in segs:
                        print(f"[{fmt_time(s['start'])}] {s['text']}" if a.timestamps else s["text"])
                return 0
        except Exception as e:  # noqa: BLE001
            errors.append(f"{name}: {type(e).__name__}: {str(e)[:300]}")

    print("無法取得字幕。原因：\n  " + "\n  ".join(errors), file=sys.stderr)
    print("替代方法：請使用者在 YouTube 影片下方點「…更多 → 顯示轉錄稿」，複製文字貼上。"
          "不要嘗試繞過私人、付費、會員或年齡限制。", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())

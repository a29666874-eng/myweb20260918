# 免費工具與查證參考

## 拿字幕／逐字稿的合法免費方法

| 方法 | 價格 | 需要安裝？ | 說明 |
|---|---|---|---|
| YouTube 內建「顯示轉錄稿」 | 🆓 | 不用 | 影片下方「…更多」→「顯示轉錄稿」，複製文字貼上。最安全、最簡單。 |
| `youtube-transcript-api`（Python 套件） | 🆓 開源 MIT | `pip install youtube-transcript-api`（需使用者同意） | 只讀取公開影片已有的字幕，不下載影片。 |
| `yt-dlp --skip-download --write-subs --write-auto-subs` | 🆓 開源 Unlicense | `pip install yt-dlp`（需使用者同意） | 加上 `--skip-download` 只拿字幕檔，不拿影片。 |
| YouTube Data API v3 `captions` | 🟡 免費額度 | 需要 Google 帳號、API 金鑰、OAuth | 下載字幕通常只限影片擁有者，一般不適合；不主動推薦。 |

**不使用**：付費逐字稿服務、付費語音轉文字 API、任何會繞過登入／付費牆／年齡驗證／地區限制的方法、下載影片或音訊再自行轉文字（除非使用者擁有該影片且明確要求，並使用本機免費工具）。

## 查證檢查表
對影片中每個工具或方法確認：
1. 官方網站還在嗎？名字有沒有改？
2. 影片中的版本與現在版本差多少？介面是否改版？
3. 價格方案：有沒有免費版？免費版限制是什麼？
4. 是否需要信用卡才能試用（需要的話要特別提醒）。
5. 安全性：是否來自官方下載點？是否要求過多權限？

查證來源優先順序：官方文件 > 官方部落格／更新紀錄 > GitHub 專案頁 > 可信媒體 > 論壇討論。

## 常見「付費 → 免費」替代思路
| 類型 | 免費／開源替代 |
|---|---|
| 影片剪輯 | DaVinci Resolve（免費版）、Shotcut、Kdenlive |
| 圖片編輯 | GIMP、Krita、Photopea（網頁） |
| 簡報設計 | Google 簡報、LibreOffice Impress、Canva 免費版 |
| 文書／試算表 | Google 文件／試算表、LibreOffice |
| 程式編輯器 | VS Code |
| 架網站 | GitHub Pages、Cloudflare Pages（免費方案） |
| 自動化 | n8n（自架開源）、Google Apps Script |
| 語音轉文字（本機） | Whisper（開源，在自己電腦執行） |

以上只是起點，推薦前仍要查證目前狀況與限制。

document.addEventListener('DOMContentLoaded', () => {
  const nav = document.querySelector('.navbar-collapse');
  const navLinks = document.querySelectorAll('.nav-link, .navbar-brand');
  const sections = document.querySelectorAll('main section[id]');
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => { if (entry.isIntersecting) entry.target.classList.add('visible'); });
  }, { threshold: 0.12 });

  document.querySelectorAll('.reveal').forEach((element) => revealObserver.observe(element));

  window.addEventListener('scroll', () => {
    let currentSection = 'home';
    sections.forEach((section) => {
      if (window.scrollY >= section.offsetTop - 160) currentSection = section.id;
    });
    document.querySelectorAll('.nav-link').forEach((link) => {
      link.classList.toggle('active', link.getAttribute('href') === `#${currentSection}`);
    });
  }, { passive: true });

  navLinks.forEach((link) => link.addEventListener('click', () => {
    const collapse = bootstrap.Collapse.getInstance(nav);
    if (collapse) collapse.hide();
  }));
});

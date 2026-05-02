// Sidebar-Inject für story-in-work
// Lädt sidebar.html, fügt sie ins DOM ein und initialisiert Hamburger + aktive Seite.

(function () {
  const SIDEBAR_URL = '/story-in-work/sidebar.html';

  function detectActivePage() {
    const path = window.location.pathname;
    // Mappe Pfade auf data-page-Werte in sidebar.html
    if (path === '/' || path === '/index.html') return 'home';
    if (path.startsWith('/architektur')) return 'architektur';
    if (path.startsWith('/canon')) return 'canon';
    if (path.startsWith('/status')) return 'status';
    if (path.startsWith('/story-in-work/charaktere')) return 'charaktere';
    if (path.startsWith('/story-in-work/zeitleiste')) return 'zeitleiste';
    if (path.startsWith('/story-in-work/leseproben')) return 'leseproben';
    if (path.startsWith('/story-in-work/moragh-karte')) return 'moragh-karte';
    if (path.startsWith('/story-in-work/kanon')) return 'kanon';
    if (path.startsWith('/story-in-work')) return 'siw-index';
    if (path.startsWith('/story')) return 'story-index';
    return '';
  }

  function init() {
    fetch(SIDEBAR_URL)
      .then(r => r.text())
      .then(html => {
        // Inject ans Anfang von <body>
        document.body.insertAdjacentHTML('afterbegin', html);
        document.body.classList.add('siw-with-sidebar');

        // Aktive Seite markieren
        const active = detectActivePage();
        document.querySelectorAll('.siw-link[data-page]').forEach(link => {
          if (link.dataset.page === active) {
            link.classList.add('siw-active');
          }
        });

        // Hamburger-Logik (Mobile)
        const sidebar = document.getElementById('siw-sidebar');
        const burger = document.getElementById('siw-burger');
        const overlay = document.getElementById('siw-overlay');

        function close() {
          sidebar.classList.remove('siw-open');
          burger.classList.remove('siw-open');
          overlay.classList.remove('siw-visible');
        }

        burger.addEventListener('click', () => {
          const open = sidebar.classList.toggle('siw-open');
          burger.classList.toggle('siw-open', open);
          overlay.classList.toggle('siw-visible', open);
        });

        overlay.addEventListener('click', close);

        // Klick auf einen Link auf Mobile schließt das Drawer
        sidebar.addEventListener('click', e => {
          if (e.target.closest('.siw-link') && window.innerWidth <= 900) {
            close();
          }
        });
      })
      .catch(err => {
        console.warn('Sidebar konnte nicht geladen werden:', err);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

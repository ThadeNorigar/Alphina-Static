// Sidebar-Inject für story-in-work + Schwester-Seiten.
// HTML inline (kein fetch) — robust, kein Race-Condition.

(function () {
  const SIDEBAR_HTML = `
<aside class="siw-sidebar" id="siw-sidebar">
  <div class="siw-sidebar-inner">
    <a href="/story-in-work/index.html" class="siw-brand">DER RISS</a>
    <nav class="siw-nav">
      <a href="/story-in-work/index.html" class="siw-link" data-page="siw-index">Trilogie</a>
      <a href="/story-in-work/zeitleiste.html" class="siw-link" data-page="zeitleiste">Zeitleiste</a>
      <a href="/architektur.html" class="siw-link" data-page="architektur">Architektur</a>
      <a href="/status/" class="siw-link" data-page="status">Kapitel-Status</a>

      <div class="siw-section">Layer 1 — Welt</div>
      <a href="/canon/?doc=00-welt" class="siw-link siw-sub">Weltbibel</a>
      <a href="/story-in-work/moragh-karte.html" class="siw-link siw-sub" data-page="moragh-karte">Moragh-Karte</a>
      <a href="/canon/?doc=00-canon-kompakt" class="siw-link siw-sub">Kanon kompakt</a>

      <div class="siw-section">Layer 2 — Regeln</div>
      <a href="/canon/?doc=01-autorin-stimme" class="siw-link siw-sub">Autorin-Stimme</a>
      <a href="/canon/?doc=02-stilregeln-v2" class="siw-link siw-sub">Stilregeln</a>
      <a href="/canon/?doc=01-referenz-konkretheit" class="siw-link siw-sub">Konkretheit</a>
      <a href="/canon/?doc=10-magie-system" class="siw-link siw-sub">Magie-System</a>
      <a href="/canon/?doc=20-moragh-talente" class="siw-link siw-sub">Moragh-Talente</a>
      <a href="/canon/?doc=18-thar-magitech" class="siw-link siw-sub">Thar-Magitech</a>

      <div class="siw-section">Layer 3 — Figuren</div>
      <a href="/story-in-work/charaktere.html" class="siw-link siw-sub" data-page="charaktere">Hauptfiguren</a>
      <a href="/canon/?doc=21-moragh-gesellschaft" class="siw-link siw-sub">Fraktionen</a>
      <a href="/canon/?doc=22-moragh-figuren" class="siw-link siw-sub">Nebenfiguren-Index</a>

      <div class="siw-section">Layer 4 — Story</div>
      <a href="/canon/?doc=00-storyline" class="siw-link siw-sub">Trilogie-Bogen</a>
      <a href="/canon/?doc=synopse-b1" class="siw-link siw-sub">Synopse Buch 1</a>
      <a href="/canon/?doc=synopse-b2" class="siw-link siw-sub">Synopse Buch 2</a>
      <a href="/canon/?doc=synopse-b3" class="siw-link siw-sub">Synopse Buch 3</a>
      <a href="/canon/?doc=12-buch3-konzept" class="siw-link siw-sub">Buch 3 — Konzept</a>

      <div class="siw-section">Layer 6 — Aktpläne</div>
      <a href="/canon/?doc=02-akt1" class="siw-link siw-sub">B1 Akt I–IV</a>
      <a href="/canon/?doc=06-buch2-akt1" class="siw-link siw-sub">B2 Akt I–IV</a>
      <a href="/canon/?doc=14-buch3-akt1" class="siw-link siw-sub">B3 Akt I–IV</a>

      <div class="siw-section">Material</div>
      <a href="/story-in-work/leseproben.html" class="siw-link siw-sub" data-page="leseproben">Leseproben</a>
      <a href="/story-in-work/kanon.html" class="siw-link siw-sub" data-page="kanon">Kanon-Index</a>
      <a href="/canon/" class="siw-link siw-sub" data-page="canon">Kanon-Leser</a>
    </nav>
  </div>
</aside>
<button class="siw-burger" id="siw-burger" aria-label="Menü öffnen"><span></span><span></span><span></span></button>
<div class="siw-overlay" id="siw-overlay"></div>
`;

  function detectActivePage() {
    const path = window.location.pathname;
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
    try {
      document.body.insertAdjacentHTML('afterbegin', SIDEBAR_HTML);
      document.body.classList.add('siw-with-sidebar');

      const active = detectActivePage();
      if (active) {
        document.querySelectorAll('.siw-link[data-page]').forEach(link => {
          if (link.dataset.page === active) {
            link.classList.add('siw-active');
          }
        });
      }

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

      sidebar.addEventListener('click', e => {
        if (e.target.closest('.siw-link') && window.innerWidth <= 900) {
          close();
        }
      });
    } catch (err) {
      console.warn('Sidebar-Init fehlgeschlagen:', err);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

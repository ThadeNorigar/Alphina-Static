// Sidebar — nur Hamburger-Toggle und Active-State.
// HTML ist statisch in jeder Page eingebaut.

(function () {
  function detectActivePage() {
    const path = window.location.pathname;
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
    const active = detectActivePage();
    if (active) {
      document.querySelectorAll('.siw-link[data-page="' + active + '"]').forEach(link => {
        link.classList.add('siw-active');
      });
    }

    const sidebar = document.getElementById('siw-sidebar');
    const burger = document.getElementById('siw-burger');
    const overlay = document.getElementById('siw-overlay');
    if (!sidebar || !burger || !overlay) return;

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
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

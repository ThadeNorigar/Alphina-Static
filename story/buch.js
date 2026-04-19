// Renderer für story/buch{1,2,3}.html
// Liest data/synopsen.json und rendert das Buch aus body[data-buch="N"].

(async function () {
  const root = document.getElementById('synopse-root');
  const buchNr = document.body.dataset.buch;
  if (!buchNr) {
    root.innerHTML = '<div class="error">Kein data-buch-Attribut gesetzt.</div>';
    return;
  }

  root.innerHTML = '<div class="loading">Lade Synopse…</div>';

  let data;
  try {
    const res = await fetch('data/synopsen.json', { cache: 'no-cache' });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    data = await res.json();
  } catch (e) {
    root.innerHTML = `<div class="error">Konnte synopsen.json nicht laden: ${e.message}</div>`;
    return;
  }

  const buch = data['b' + buchNr];
  if (!buch) {
    root.innerHTML = `<div class="error">Buch ${buchNr} nicht in den Daten gefunden.</div>`;
    return;
  }

  const meta = buch.meta || {};
  const numeral = { 1: 'I', 2: 'II', 3: 'III' }[buchNr] || buchNr;

  const metaRows = [];
  if (meta.pov) {
    const pov = Array.isArray(meta.pov) ? meta.pov.join(', ') : meta.pov;
    metaRows.push(['POV', pov + (meta.pov_verteilung ? ` · ${meta.pov_verteilung}` : '')]);
  }
  if (meta.zeitraum_tz)   metaRows.push(['Zeit (TZ)', meta.zeitraum_tz]);
  if (meta.zeitraum_mz)   metaRows.push(['Zeit (MZ)', meta.zeitraum_mz]);
  if (meta.wortumfang_ziel)
    metaRows.push(['Umfang-Ziel', meta.wortumfang_ziel.toLocaleString('de-DE') + ' Wörter']);
  if (meta.status) metaRows.push(['Status', meta.status]);

  const metaHtml = metaRows.length
    ? `<dl class="meta-grid">${metaRows.map(([k, v]) => `<dt>${k}</dt><dd>${escapeHtml(v)}</dd>`).join('')}</dl>`
    : '';

  const sections = (buch.sections || []).map(s => {
    const title = s.title ? `<h2>${escapeHtml(s.title)}</h2>` : '';
    return `<div class="section">${title}<div class="section-body">${s.html || ''}</div></div>`;
  }).join('');

  const updated = meta.last_update
    ? `<div class="status-note"><span class="dot"></span>Zuletzt aus buch/synopse-b${buchNr}.md gebaut — ${escapeHtml(meta.last_update)}</div>`
    : '';

  root.innerHTML = `
    <div class="book-card">
      <div class="card-header">
        <div class="buch-num">Buch ${numeral}</div>
        <h1>${escapeHtml(meta.titel || '')}</h1>
        ${meta.untertitel ? `<div class="untertitel">${escapeHtml(meta.untertitel)}</div>` : ''}
        ${metaHtml}
      </div>
      <div class="card-body">
        ${sections}
        ${updated}
      </div>
    </div>
  `;

  if (meta.titel) {
    document.title = `Buch ${numeral} — ${meta.titel}`;
  }
})();

function escapeHtml(str) {
  if (str == null) return '';
  return String(str)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

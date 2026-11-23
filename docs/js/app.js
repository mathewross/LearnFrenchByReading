import { initStore, get, set, exportAll, importAll, requestPersistence } from './store.js';
import * as tts from './tts.js';
import { Reader } from './reader.js';

const LEVELS = ['A1', 'A2', 'B1', 'B2', 'C1'];
const COLORS = ['#5f7f73', '#9b6f5a', '#5d7088', '#857550', '#8c5f6a', '#4f7c82'];
const THEME_COLORS = { light: '#f6f4ef', sepia: '#f1e7d0', dark: '#17181a' };
const DEFAULTS = { theme: 'light', font: 'serif', size: 20, lh: 1.6, margin: 22, rate: 0.9, pics: 'on' };
const POS = { NOUN: 'noun', VERB: 'verb', ADJ: 'adjective', ADV: 'adverb', PRON: 'pronoun', DET: 'determiner', PREP: 'preposition', CONJ: 'conjunction', INTJ: 'interjection', EXPR: 'expression', NUM: 'number', PROPN: 'name', AUX: 'auxiliary' };

const ICON = {
  back: '<svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg>',
  play: '<svg viewBox="0 0 24 24"><path d="M8 5l11 7-11 7z"/></svg>',
  pause: '<svg viewBox="0 0 24 24"><path d="M9 5v14M15 5v14"/></svg>',
  aa: '<span style="font:600 16px var(--serif)">Aa</span>',
  speaker: '<svg viewBox="0 0 24 24"><path d="M4 9v6h4l5 4V5L8 9H4z"/><path d="M16.5 8.5a5 5 0 010 7"/></svg>',
  star: '<svg viewBox="0 0 24 24"><path d="M12 4l2.4 5 5.4.7-4 3.8 1 5.4-4.8-2.6-4.8 2.6 1-5.4-4-3.8 5.4-.7z"/></svg>',
  book: '<svg viewBox="0 0 24 24"><path d="M4 5h6v14H4zM10 5h6v14h-6z"/><path d="M17 6l3 1-3 12"/></svg>',
  bookmark: '<svg viewBox="0 0 24 24"><path d="M7 4h10v16l-5-4-5 4z"/></svg>',
  chart: '<svg viewBox="0 0 24 24"><path d="M5 20V10M12 20V4M19 20v-7"/></svg>',
  gear: '<svg viewBox="0 0 24 24"><path d="M4 7h10M18 7h2M4 17h2M10 17h10"/><circle cx="16" cy="7" r="2"/><circle cx="8" cy="17" r="2"/></svg>',
  sentence: '<svg viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h9"/></svg>',
  more: '<svg viewBox="0 0 24 24"><path d="M5 7h14M5 12h14M5 17h14"/></svg>',
};

const $ = (s, r = document) => r.querySelector(s);
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const app = $('#app');
let lib = null;
let settings = { ...DEFAULTS };
let examples = null;
const storyCache = new Map();
const L = { q: '', level: 'All', sort: 'recommended' };

// ------------------------------------------------------------------ helpers
function hash(str) { let h = 0; for (const c of str) h = (h * 31 + c.charCodeAt(0)) >>> 0; return h; }
const colorFor = (e) => COLORS[hash(e.series || e.id) % COLORS.length];
const today = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`; };
let toastTimer;
function toast(msg) {
  const t = $('#toast'); t.textContent = msg; t.classList.add('show');
  clearTimeout(toastTimer); toastTimer = setTimeout(() => t.classList.remove('show'), 2600);
}
function applySettings() {
  const s = settings, r = document.documentElement.style;
  document.body.className = 'theme-' + s.theme + (s.pics === 'off' ? ' nopics' : '');
  r.setProperty('--fs', s.size + 'px'); r.setProperty('--lh', s.lh); r.setProperty('--margin', s.margin + 'px');
  r.setProperty('--rfont', s.font === 'sans' ? 'var(--ui)' : 'var(--serif)');
  $('#theme-color').content = THEME_COLORS[s.theme];
}
function saveSettings() { set('settings', settings); applySettings(); }

async function loadStory(id) {
  if (storyCache.has(id)) return storyCache.get(id);
  const res = await fetch(`data/stories/${id}.json`);
  if (!res.ok) throw new Error('story fetch failed');
  const s = await res.json();
  storyCache.set(id, s);
  return s;
}
async function loadExamples() {
  if (examples) return examples;
  try { examples = await (await fetch('data/examples.json')).json(); } catch (e) { examples = {}; }
  return examples;
}

const words = () => get('words', {});
const progress = () => get('progress', {});
function coverage(entry) {
  if (!entry.lx.length) return 1;
  const w = words();
  return entry.lx.filter((i) => w[lib.lemmas[i]] && w[lib.lemmas[i]].known).length / entry.lx.length;
}
const minutes = (w) => Math.max(1, Math.round(w / 120));
const artText = (info, lemma) => (info.a ? (info.a === "l'" ? "l'" : info.a + ' ') + lemma : lemma);

// ------------------------------------------------------------------ sheet (shared bottom sheet)
let sheetEl, scrimEl, sheetOpen = false, sheetClick = null, sheetClosed = null, sheetTapClose = true;
function ensureSheet() {
  scrimEl = document.createElement('div'); scrimEl.className = 'scrim';
  sheetEl = document.createElement('div'); sheetEl.className = 'sheet';
  document.body.append(scrimEl, sheetEl);
  scrimEl.addEventListener('click', closeSheet);
  sheetEl.addEventListener('click', (e) => {
    const b = e.target.closest('[data-a]');
    if (b) { if (sheetClick) sheetClick(b.dataset.a, b); return; }
    if (sheetTapClose && !e.target.closest('button,input,select,label,a')) closeSheet();
  });
}
function openSheet(html, { scrim = null, tapClose = true, onClick = null, onClose = null } = {}) {
  sheetEl.innerHTML = html; sheetClick = onClick; sheetClosed = onClose; sheetTapClose = tapClose;
  sheetEl.scrollTop = 0; sheetEl.classList.add('open'); sheetOpen = true;
  scrimEl.className = 'scrim' + (scrim ? ' on' : '');
  scrimEl.style.background = scrim === 'clear' ? 'transparent' : '';
}
function closeSheet() {
  if (!sheetEl) return;
  sheetEl.classList.remove('open'); scrimEl.className = 'scrim'; sheetOpen = false;
  const c = sheetClosed; sheetClosed = null; if (c) c();
}

// ------------------------------------------------------------------ router
let reader = null, story = null, readerCleanup = null;
function route() {
  if (readerCleanup) { readerCleanup(); readerCleanup = null; }
  closeSheet();
  const [a, b] = location.hash.replace(/^#\/?/, '').split('/');
  if (a === 'read' && b) return openReader(b);
  if (a === 'saved') return viewSaved();
  if (a === 'stats') return viewStats();
  if (a === 'settings') return viewSettings();
  viewLibrary();
}
function tabs(active) {
  const t = [['library', '', 'Library', ICON.book], ['saved', 'saved', 'Saved', ICON.bookmark], ['stats', 'stats', 'Progress', ICON.chart], ['settings', 'settings', 'Settings', ICON.gear]];
  return `<nav class="tabs">${t.map(([k, h, label, ic]) => `<a href="#/${h}" class="${active === k ? 'on' : ''}">${ic}<span>${label}</span></a>`).join('')}</nav>`;
}

// ------------------------------------------------------------------ library
function visibleStories() {
  const q = L.q.trim().toLowerCase();
  const P = progress();
  let list = lib.stories.filter((s) => {
    if (L.level !== 'All' && s.level !== L.level) return false;
    if (!q) return true;
    const ser = s.series && lib.series[s.series] ? lib.series[s.series].title : '';
    return [s.title, s.title_en, s.summary, ser, ...s.tags].join(' ').toLowerCase().includes(q);
  });
  const knownCount = Object.values(words()).filter((w) => w.known).length;
  const cmp = {
    difficulty: (a, b) => a.difficulty - b.difficulty,
    level: (a, b) => LEVELS.indexOf(a.level) - LEVELS.indexOf(b.level) || a.difficulty - b.difficulty,
    length: (a, b) => a.words - b.words,
    title: (a, b) => a.title.localeCompare(b.title, 'fr'),
    recommended: (a, b) => {
      const rank = (s) => (P[s.id] && P[s.id].done ? 2 : P[s.id] && P[s.id].pos > 0 ? 0 : 1);
      if (rank(a) !== rank(b)) return rank(a) - rank(b);
      if (knownCount < 20) return a.difficulty - b.difficulty; // not enough data yet: easiest first
      return Math.abs(coverage(a) - 0.965) - Math.abs(coverage(b) - 0.965); // aim for ~95-98% known
    },
  }[L.sort];
  // episodes of one series always read in order; other ties fall back to title
  const sameSeries = (a, b) => (a.series && a.series === b.series ? a.episode - b.episode : 0);
  return list.sort((a, b) => sameSeries(a, b) || cmp(a, b) || a.title.localeCompare(b.title, 'fr'));
}
function cardHtml(s) {
  const P = progress()[s.id] || {};
  const ser = s.series && lib.series[s.series] ? `${lib.series[s.series].title} · Ep. ${s.episode}` : '';
  const bg = s.cover ? `background-color:${colorFor(s)};background-image:linear-gradient(to bottom,rgba(0,0,0,0) 45%,rgba(0,0,0,.66)),url('${s.cover}')` : `background:${colorFor(s)}`;
  return `<button class="card" data-id="${s.id}"><div class="cover" style="${bg}">
    <span class="lvl">${s.level}</span>${P.done ? '<span class="done">✓</span>' : ''}
    ${ser ? `<div class="ser">${esc(ser)}</div>` : ''}<div class="ct">${esc(s.title)}</div></div>
    <div class="cmeta"><span>${minutes(s.words)} min · ${s.words} words</span>
    <span>You know ${Math.round(coverage(s) * 100)}% of the words</span>
    ${P.frac ? `<div class="bar-prog"><i style="width:${Math.round(P.frac * 100)}%"></i></div>` : ''}</div></button>`;
}
function viewLibrary() {
  app.innerHTML = `<div class="view"><h1>Lecture</h1>
    <input class="search" id="q" type="search" placeholder="Search title, topic or series" value="${esc(L.q)}" autocomplete="off">
    <div class="chips" id="chips">${['All', ...LEVELS].map((l) => `<button class="chip ${L.level === l ? 'on' : ''}" data-l="${l}">${l}</button>`).join('')}</div>
    <div class="toolbar"><span id="count"></span><label>Sort&nbsp;<select id="sort">${[['recommended', 'Recommended'], ['difficulty', 'Difficulty'], ['level', 'Level'], ['length', 'Length'], ['title', 'Title']].map(([v, t]) => `<option value="${v}" ${L.sort === v ? 'selected' : ''}>${t}</option>`).join('')}</select></label></div>
    <div class="grid" id="grid"></div></div>${tabs('library')}`;
  const paint = () => {
    const list = visibleStories();
    $('#count').textContent = `${list.length} ${list.length === 1 ? 'story' : 'stories'}`;
    $('#grid').innerHTML = list.length ? list.map(cardHtml).join('') : '<p class="empty" style="grid-column:1/-1">No stories match.</p>';
  };
  paint();
  $('#q').addEventListener('input', (e) => { L.q = e.target.value; paint(); });
  $('#sort').addEventListener('change', (e) => { L.sort = e.target.value; paint(); });
  $('#chips').addEventListener('click', (e) => {
    const b = e.target.closest('.chip'); if (!b) return;
    L.level = b.dataset.l; document.querySelectorAll('.chip').forEach((c) => c.classList.toggle('on', c === b)); paint();
  });
  $('#grid').addEventListener('click', (e) => { const c = e.target.closest('.card'); if (c) preview(c.dataset.id); });
}
function preview(id) {
  const s = lib.stories.find((x) => x.id === id);
  const P = progress()[id] || {};
  const w = words();
  const fresh = s.lx.filter((i) => !(w[lib.lemmas[i]] && w[lib.lemmas[i]].known)).length;
  const ser = s.series && lib.series[s.series] ? `${lib.series[s.series].title} · Episode ${s.episode}` : '';
  const label = P.done ? 'Read again' : P.pos > 0 ? 'Resume' : 'Start reading';
  openSheet(`<div class="pos">${esc(ser || 'Story')}</div><div class="sh-word">${esc(s.title)}</div>
    <div class="muted" style="font-style:italic">${esc(s.title_en)}</div>
    <p class="preview-sum">${esc(s.summary)}</p>
    <div class="facts"><span>${s.level}</span><span>${s.words} words</span><span>~${minutes(s.words)} min</span><span>${fresh} new words for you</span></div>
    <div class="actions"><button class="btn primary" data-a="go">${label}</button></div>`,
  { scrim: 'dim', tapClose: false, onClick: (a) => {
    if (a !== 'go') return;
    if (P.done) { const all = progress(); all[id] = { ...P, pos: 0, frac: 0 }; set('progress', all); }
    closeSheet(); location.hash = `#/read/${id}`;
  } });
}

// ------------------------------------------------------------------ display controls (shared by reader sheet + settings)
function displayControlsHtml() {
  const s = settings;
  return `<div class="row"><label>Theme</label><div class="seg" data-seg="theme">${['light', 'sepia', 'dark'].map((t) => `<button class="t-${t} ${s.theme === t ? 'on' : ''}" data-v="${t}">${t[0].toUpperCase() + t.slice(1)}</button>`).join('')}</div></div>
    <div class="row"><label>Pictures</label><div class="seg" data-seg="pics">${[['on', 'On'], ['off', 'Off']].map(([v, t]) => `<button class="${s.pics === v ? 'on' : ''}" data-v="${v}">${t}</button>`).join('')}</div></div>
    <div class="row"><label>Font</label><div class="seg" data-seg="font">${[['serif', 'Serif'], ['sans', 'Sans']].map(([v, t]) => `<button class="${s.font === v ? 'on' : ''}" data-v="${v}">${t}</button>`).join('')}</div></div>
    <div class="row"><label>Text size</label><input type="range" data-k="size" min="15" max="32" step="1" value="${s.size}"></div>
    <div class="row"><label>Line spacing</label><input type="range" data-k="lh" min="1.3" max="2.1" step="0.05" value="${s.lh}"></div>
    <div class="row"><label>Margins</label><input type="range" data-k="margin" min="8" max="56" step="2" value="${s.margin}"></div>`;
}
function bindDisplayControls(root, onChange) {
  root.querySelectorAll('[data-seg]').forEach((seg) => seg.addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    settings[seg.dataset.seg] = b.dataset.v; saveSettings();
    seg.querySelectorAll('button').forEach((x) => x.classList.toggle('on', x === b)); onChange && onChange();
  }));
  root.querySelectorAll('input[type=range][data-k]').forEach((inp) => inp.addEventListener('input', () => {
    settings[inp.dataset.k] = parseFloat(inp.value); saveSettings(); onChange && onChange();
  }));
}

// ------------------------------------------------------------------ reader
async function openReader(id) {
  const entry = lib.stories.find((s) => s.id === id);
  if (!entry) { location.hash = '#/'; return; }
  app.innerHTML = `<div class="reader">
    <div class="rbar top" id="rtop"><button class="ibtn" id="back" aria-label="Back to library">${ICON.back}</button>
      <div class="rtitle">${esc(entry.title)}</div>
      <button class="ibtn" id="listen" aria-label="Read aloud">${ICON.play}</button>
      <button class="ibtn" id="aa" aria-label="Display settings">${ICON.aa}</button></div>
    <div class="stage" id="stage"><div class="vp" id="vp"></div></div>
    <div class="rbar bottom"><span>${entry.level}</span><div class="bar-prog rprog"><i id="pfill" style="width:0"></i></div><span class="pg" id="pg"></span></div></div>`;
  try { story = await loadStory(id); } catch (e) { toast('Could not load this story. Are you offline?'); location.hash = '#/'; return; }
  if (location.hash !== `#/read/${id}`) return; // navigated away while loading

  let listening = false, timer = null, relayoutT = null, ro = null;
  const P0 = progress()[id] || {};
  const vp = $('#vp');
  const updateBottom = () => {
    $('#pg').textContent = `${reader.page + 1} / ${reader.count}`;
    $('#pfill').style.width = `${Math.round(((reader.page + 1) / reader.count) * 100)}%`;
  };
  const markKnown = () => {
    const W = words();
    for (const [lemma, info] of Object.entries(story.lemmas)) {
      if (info.p === 'PROPN') continue;
      const rec = W[lemma] || (W[lemma] = {});
      if (!rec.looked && !rec.saved) rec.known = true;
    }
    set('words', W);
  };
  const savePos = (info) => {
    const P = progress(); const p = P[id] || { secs: 0 };
    p.pos = info.pos; p.last = Date.now();
    p.frac = reader.atEnd() ? 1 : info.pos / Math.max(1, info.total);
    if (reader.atEnd() && !p.done) { p.done = true; markKnown(); toast('Story finished. Words you didn’t look up are now counted as known.'); }
    P[id] = p; set('progress', P);
  };
  const hideBars = () => $('#rtop').classList.add('hide');

  reader = new Reader(vp, story, {
    onPage: (info) => { updateBottom(); savePos(info); },
    onWord: (i) => showWord(i),
    onSentence: (si) => showSentence(si),
    onCenterTap: () => $('#rtop').classList.toggle('hide'),
    onTapAway: (swiped) => {
      if (sheetOpen) { closeSheet(); return true; }
      if (swiped) hideBars();
      return false;
    },
  });
  reader.pos = P0.pos || 0;
  await new Promise((r) => requestAnimationFrame(r));
  try { await document.fonts.ready; } catch (e) { /* fine */ }
  reader.layout(); updateBottom();
  if (!(P0.pos > 0)) setTimeout(hideBars, 2600);

  ro = new ResizeObserver(() => { clearTimeout(relayoutT); relayoutT = setTimeout(() => { reader.layout(); updateBottom(); }, 80); });
  ro.observe($('#stage'));

  // reading time + streak
  timer = setInterval(() => {
    if (document.visibilityState !== 'visible') return;
    const P = progress(); const p = P[id] || (P[id] = { secs: 0 }); p.secs = (p.secs || 0) + 5; set('progress', P);
    const S = get('stats', { days: {} }); S.days[today()] = (S.days[today()] || 0) + 5; set('stats', S);
  }, 5000);

  const onKey = (e) => {
    if (e.key === 'ArrowRight' || e.key === 'PageDown') reader.next();
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') reader.prev();
    else if (e.key === 'Escape') { if (sheetOpen) { closeSheet(); } }
  };
  document.addEventListener('keydown', onKey);

  // ---- word sheet
  function showWord(i) {
    const t = reader.tokens[i]; const tk = t.tk; const info = story.lemmas[tk.l]; const sent = reader.sents[t.si];
    const pos = tk.p || info.p; const gloss = tk.g || info.g;
    reader.highlightWord(i);
    const W = words(); const rec = W[tk.l] || (W[tk.l] = {});
    if (pos !== 'PROPN') { rec.looked = (rec.looked || 0) + 1; rec.known = false; set('words', W); }
    const surface = t.text;
    const differs = tk.l.toLowerCase() !== surface.toLowerCase().replace(/’/g, "'");
    let lemmaLine = '';
    if (info.p === 'NOUN' && info.a) lemmaLine = `<span class="gender-${info.x}">${esc(artText(info, tk.l))}</span> · ${info.x === 'm' ? 'masculine' : 'feminine'} noun`;
    else if (differs && pos !== 'PROPN') lemmaLine = `Dictionary form: ${esc(tk.l)}`;
    const saved = !!rec.saved;
    openSheet(`<div class="sh-head"><span class="sh-word">${esc(surface)}</span><span class="pos">${POS[pos] || pos.toLowerCase()}</span></div>
      <div class="gloss">${esc(gloss)}</div>
      ${tk.m ? `<div class="note">${esc(tk.m)}</div>` : ''}
      ${lemmaLine ? `<div class="lemma-line">${lemmaLine}</div>` : ''}
      <div class="actions">
        <button class="btn" data-a="say">${ICON.speaker} Listen</button>
        <button class="btn" data-a="sent">${ICON.sentence} Sentence</button>
        <button class="btn" data-a="more">${ICON.more} Examples</button>
        <button class="btn ${saved ? 'on' : ''}" data-a="save">${ICON.star} <span>${saved ? 'Saved' : 'Save'}</span></button></div>
      <div class="extra" id="extra"></div>`,
    { onClose: () => reader && reader.clearHighlights(), onClick: async (a, btn) => {
      const extra = $('#extra', sheetEl);
      if (a === 'say') { if (!tts.speak(surface, { rate: settings.rate })) toast(tts.status().text); else if (!tts.status().ok) toast(tts.status().text); }
      if (a === 'sent') extra.innerHTML = `<div class="ex"><div class="fr">${esc(sent.fr)}</div><div class="en">${esc(sent.en)}</div></div>`;
      if (a === 'more') {
        const ex = await loadExamples();
        const list = (ex[tk.l] || []).filter((x) => x.fr !== sent.fr).slice(0, 4);
        extra.innerHTML = list.length ? list.map((x) => `<div class="ex"><div class="fr">${esc(x.fr)}</div><div class="en">${esc(x.en)}</div></div>`).join('')
          : '<div class="muted">No other sentences with this word in the library yet.</div>';
      }
      if (a === 'save') {
        const W2 = words(); const r = W2[tk.l] || (W2[tk.l] = {});
        if (r.saved) { delete r.saved; delete r.ctx; btn.classList.remove('on'); $('span', btn).textContent = 'Save'; }
        else {
          r.saved = Date.now(); r.known = false;
          r.ctx = { form: surface, g: gloss, p: pos, a: info.a ? artText(info, tk.l) : '', fr: sent.fr, en: sent.en, story: id };
          btn.classList.add('on'); $('span', btn).textContent = 'Saved';
        }
        set('words', W2);
      }
    } });
  }

  // ---- sentence sheet (long-press)
  function showSentence(si) {
    const s = reader.sents[si];
    reader.highlightSentence(si);
    const saved = (get('sentences', [])).some((x) => x.fr === s.fr);
    openSheet(`<div class="pos">Sentence</div><div class="sent-fr">${esc(s.fr)}</div><div class="sent-en">${esc(s.en)}</div>
      <div class="actions"><button class="btn" data-a="say">${ICON.speaker} Listen</button>
      <button class="btn ${saved ? 'on' : ''}" data-a="save">${ICON.star} <span>${saved ? 'Saved' : 'Save'}</span></button></div>`,
    { onClose: () => reader && reader.clearHighlights(), onClick: (a, btn) => {
      if (a === 'say') { if (!tts.speak(s.fr, { rate: settings.rate })) toast(tts.status().text); }
      if (a === 'save') {
        let list = get('sentences', []);
        if (list.some((x) => x.fr === s.fr)) { list = list.filter((x) => x.fr !== s.fr); btn.classList.remove('on'); $('span', btn).textContent = 'Save'; }
        else { list.push({ fr: s.fr, en: s.en, story: id, ts: Date.now() }); btn.classList.add('on'); $('span', btn).textContent = 'Saved'; }
        set('sentences', list);
      }
    } });
  }

  // ---- read aloud (sentence by sentence, turns pages, highlights the sentence)
  const setListenUi = () => { const b = $('#listen'); if (!b) return; b.innerHTML = listening ? ICON.pause : ICON.play; b.classList.toggle('on', listening); };
  function stopListen() { listening = false; tts.stop(); if (reader) reader.clearHighlights(); setListenUi(); }
  function startListen() {
    if (!tts.supported()) { toast(tts.status().text); return; }
    if (!tts.status().ok) toast(tts.status().text);
    listening = true; setListenUi(); closeSheet();
    let si = reader.currentSentence();
    const step = () => {
      if (!listening || si >= reader.sents.length) { stopListen(); return; }
      reader.ensureSentenceVisible(si); reader.highlightSentence(si);
      if (!tts.speak(reader.sents[si].fr, { rate: settings.rate, onend: () => { si++; step(); } })) stopListen();
    };
    step();
  }
  $('#listen').addEventListener('click', () => (listening ? stopListen() : startListen()));
  $('#back').addEventListener('click', () => { location.hash = '#/'; });
  $('#aa').addEventListener('click', () => {
    openSheet(`<div class="pos">Display</div>${displayControlsHtml()}`, { scrim: 'clear', tapClose: false });
    bindDisplayControls(sheetEl, () => { reader.layout(); updateBottom(); });
  });

  readerCleanup = () => {
    stopListen(); clearInterval(timer); clearTimeout(relayoutT); if (ro) ro.disconnect();
    document.removeEventListener('keydown', onKey); reader = null; story = null;
  };
}

// ------------------------------------------------------------------ saved
function viewSaved() {
  const W = words();
  const items = Object.entries(W).filter(([, r]) => r.saved).sort((a, b) => b[1].saved - a[1].saved);
  const sents = get('sentences', []).slice().reverse();
  app.innerHTML = `<div class="view"><h1>Saved</h1>
    <p class="muted" style="margin-top:-6px">${items.length} word${items.length === 1 ? '' : 's'} · ${sents.length} sentence${sents.length === 1 ? '' : 's'}. Spaced-repetition review arrives in the next milestone.</p>
    ${items.length ? items.map(([lemma, r]) => `<div class="list-item"><div class="li-top"><span class="li-w">${esc(r.ctx && r.ctx.a ? r.ctx.a : lemma)}</span><button class="x" data-w="${esc(lemma)}" aria-label="Remove">×</button></div>
      <div class="li-g">${esc(r.ctx ? r.ctx.g : '')}</div><div class="li-ctx">${esc(r.ctx ? r.ctx.fr : '')}</div></div>`).join('') : '<p class="empty">Tap a word while reading, then Save, and it will appear here.</p>'}
    ${sents.length ? '<h3 class="muted" style="font-size:13px;text-transform:uppercase;letter-spacing:.06em;margin:22px 0 10px">Sentences</h3>' : ''}
    ${sents.map((s) => `<div class="list-item"><div class="li-top"><span class="li-ctx" style="margin:0;color:var(--fg)">${esc(s.fr)}</span><button class="x" data-s="${esc(s.fr)}" aria-label="Remove">×</button></div><div class="li-g muted">${esc(s.en)}</div></div>`).join('')}
    </div>${tabs('saved')}`;
  app.querySelector('.view').addEventListener('click', (e) => {
    const x = e.target.closest('.x'); if (!x) return;
    if (x.dataset.w) { const w = words(); delete w[x.dataset.w].saved; delete w[x.dataset.w].ctx; set('words', w); }
    if (x.dataset.s) set('sentences', get('sentences', []).filter((s) => s.fr !== x.dataset.s));
    viewSaved();
  });
}

// ------------------------------------------------------------------ stats
function streak(days) {
  let n = 0; const d = new Date();
  const key = (dt) => `${dt.getFullYear()}-${String(dt.getMonth() + 1).padStart(2, '0')}-${String(dt.getDate()).padStart(2, '0')}`;
  if ((days[key(d)] || 0) < 60) d.setDate(d.getDate() - 1);
  while ((days[key(d)] || 0) >= 60) { n++; d.setDate(d.getDate() - 1); }
  return n;
}
function viewStats() {
  const P = progress(); const W = words(); const S = get('stats', { days: {} });
  const totalSecs = Object.values(P).reduce((a, p) => a + (p.secs || 0), 0);
  const met = new Set();
  lib.stories.forEach((s) => { if (P[s.id] && P[s.id].pos > 0) s.lx.forEach((i) => met.add(lib.lemmas[i])); });
  Object.keys(W).forEach((l) => { if (W[l].looked) met.add(l); });
  const known = Object.values(W).filter((w) => w.known).length;
  const finished = Object.values(P).filter((p) => p.done).length;
  const tile = (n, label) => `<div class="stat"><b>${n}</b><span>${label}</span></div>`;
  app.innerHTML = `<div class="view"><h1>Progress</h1><div class="stats">
    ${tile(Math.round(totalSecs / 60), 'minutes read')}${tile(Math.round((S.days[today()] || 0) / 60), 'minutes today')}
    ${tile(finished, 'stories finished')}${tile(streak(S.days), 'day streak')}
    ${tile(met.size, 'words met')}${tile(known, 'words known')}</div>
    <p class="muted" style="line-height:1.45">A word counts as <b>known</b> when you finish a story without looking it up. Looking a word up (or saving it) moves it back to learning.</p></div>${tabs('stats')}`;
}

// ------------------------------------------------------------------ settings
function viewSettings() {
  const v = tts.status();
  app.innerHTML = `<div class="view"><h1>Settings</h1>
    <div class="panel"><h3>Reading</h3>${displayControlsHtml()}<div class="sample" id="sample">Il fait beau à Paris. Léa mange un croissant.</div></div>
    <div class="panel"><h3>Listening</h3>
      <div class="row"><label>Speech speed</label><input type="range" id="rate" min="0.5" max="1.2" step="0.05" value="${settings.rate}"></div>
      <div class="hint" id="voice">${esc(v.text)}</div>
      <div class="setting-btns"><button class="btn" id="test">${ICON.speaker} Test voice</button></div></div>
    <div class="panel"><h3>Offline</h3>
      <div class="hint">The app itself works offline after the first load. Stories you open are cached automatically; this downloads all of them.</div>
      <div class="setting-btns"><button class="btn" id="dl">Download all stories</button></div></div>
    <div class="panel"><h3>Backup</h3>
      <div class="hint">Browsers can clear site data. Export your progress regularly and keep the file somewhere safe.</div>
      <div class="setting-btns"><button class="btn" id="exp">Export progress</button><button class="btn" id="imp">Import…</button><button class="btn" id="persist">Keep my data</button></div>
      <input type="file" id="file" accept="application/json,.json" hidden></div>
    <p class="muted" style="font-size:13px">Lecture · milestone M3 preview · ${lib.stories.length} stories</p></div>${tabs('settings')}`;
  bindDisplayControls(app, () => {});
  $('#rate').addEventListener('input', (e) => { settings.rate = parseFloat(e.target.value); saveSettings(); });
  $('#test').addEventListener('click', () => { if (!tts.speak('Bonjour ! Il fait beau à Paris aujourd’hui.', { rate: settings.rate })) toast(tts.status().text); setTimeout(() => { const s = tts.status(); const el = $('#voice'); if (el) el.textContent = s.text; }, 400); });
  $('#dl').addEventListener('click', async (e) => {
    const btn = e.currentTarget;
    if (!('caches' in window)) { toast('Offline storage is not available here.'); return; }
    try {
      const cache = await caches.open('lecture-data'); let n = 0;
      for (const s of lib.stories) {
        const url = `data/stories/${s.id}.json`;
        const res = await fetch(url);
        if (res.ok) {
          const story = await res.clone().json();
          await cache.put(url, res.clone()); n++;
          for (const pic of Object.values(story.pics || {})) { const r = await fetch(pic.src); if (r.ok) await cache.put(pic.src, r); }
        }
        btn.textContent = `Downloading… ${n}/${lib.stories.length}`;
      }
      btn.textContent = 'Download all stories'; toast(`${n} stories saved for offline.`);
    } catch (err) { btn.textContent = 'Download all stories'; toast('Download failed. Check your connection.'); }
  });
  $('#exp').addEventListener('click', () => {
    const blob = new Blob([exportAll()], { type: 'application/json' });
    const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = `lecture-backup-${today()}.json`; a.click();
    setTimeout(() => URL.revokeObjectURL(a.href), 2000);
  });
  $('#imp').addEventListener('click', () => $('#file').click());
  $('#file').addEventListener('change', async (e) => {
    const f = e.target.files[0]; if (!f) return;
    try { importAll(await f.text()); settings = { ...DEFAULTS, ...get('settings', {}) }; applySettings(); toast('Progress imported.'); viewSettings(); }
    catch (err) { toast(err.message || 'Could not read that file.'); }
  });
  $('#persist').addEventListener('click', async () => toast((await requestPersistence()) ? 'Storage will be kept.' : 'The browser did not grant persistent storage.'));
}

// ------------------------------------------------------------------ boot
(async function main() {
  await initStore();
  settings = { ...DEFAULTS, ...get('settings', {}) };
  applySettings();
  ensureSheet();
  try { lib = await (await fetch('data/library.json')).json(); }
  catch (e) { app.innerHTML = '<div class="view"><p class="empty">Couldn’t load the library. Check your connection and reload.</p></div>'; return; }
  window.addEventListener('hashchange', route);
  route();
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }
})();

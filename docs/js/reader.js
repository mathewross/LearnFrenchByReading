// Paginated reader. Renders a story as token spans, paginates with CSS columns,
// and keeps position as a TOKEN INDEX so it survives any reflow (font, margins, rotation).
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

export class Reader {
  /**
   * @param {HTMLElement} viewport  clipping element (overflow hidden, exact page size)
   * @param {object} story          enriched story JSON
   * @param {object} hooks          { onPage, onWord(tokenIdx), onSentence(sentIdx), onCenterTap(), onTapAway() }
   */
  constructor(viewport, story, hooks) {
    this.vp = viewport;
    this.story = story;
    this.hooks = hooks;
    this.page = 0;
    this.count = 1;
    this.pos = 0; // first token index on the current page
    this.tokens = []; // {si, ti, tk}
    this.sents = []; // {fr, en, first, last}
    this.tokenPage = [];
    this.pages = document.createElement('div');
    this.pages.className = 'pages';
    this.pages.innerHTML = this.buildHtml();
    this.vp.appendChild(this.pages);
    this.bind();
  }

  buildHtml() {
    const st = this.story;
    let html = `<header class="story-head"><div class="eyebrow">${esc(st.level)}${st.series_id && st.episode ? ' · Episode ' + st.episode : ''}</div>`
      + `<h1>${esc(st.title)}</h1><div class="sub">${esc(st.title_en)}</div></header>`;
    st.chapters.forEach((ch, ci) => {
      if (ch.title) html += `<h2 class="ch">${esc(ch.title)}</h2>`;
      ch.paragraphs.forEach((para, pi) => {
        const pic = (st.pics || {})[`${ci}.${pi}`];
        if (pic) html += `<figure class="pic"><img src="${esc(pic.src)}" alt="${esc(pic.alt)}" width="640" height="400" decoding="async" draggable="false"><figcaption>${esc(pic.alt)}</figcaption></figure>`;
        html += '<p>';
        para.forEach((s) => {
          const si = this.sents.length;
          const sent = { fr: s.fr, en: s.en, first: this.tokens.length, last: this.tokens.length + s.tk.length - 1 };
          this.sents.push(sent);
          html += `<span class="sn" data-s="${si}">`;
          let pos = 0;
          s.tk.forEach((t) => {
            html += esc(s.fr.slice(pos, t.s));
            html += `<span class="w" data-t="${this.tokens.length}">${esc(s.fr.slice(t.s, t.e))}</span>`;
            this.tokens.push({ si, tk: t, text: s.fr.slice(t.s, t.e) });
            pos = t.e;
          });
          html += esc(s.fr.slice(pos)) + '</span> ';
        });
        html += '</p>';
      });
    });
    return html + '<div class="the-end">Fin</div>';
  }

  /** Re-measure after any size/typography change; keeps the reader on the same token. */
  layout() {
    const keep = this.pos;
    const W = this.vp.clientWidth;
    const H = this.vp.clientHeight;
    if (!W || !H) return;
    this.W = W;
    const p = this.pages;
    p.style.transform = 'none';
    p.style.setProperty('--pic-h', Math.round(Math.max(110, Math.min(H * 0.3, W * 0.62))) + 'px'); // fixed height: pages don't jump as images load
    p.style.width = W + 'px';
    p.style.height = H + 'px';
    p.style.columnWidth = W + 'px';
    p.style.columnGap = '0px';
    this.count = Math.max(1, Math.round(p.scrollWidth / W));
    const base = p.getBoundingClientRect().left;
    const spans = p.querySelectorAll('.w');
    this.tokenPage = new Array(spans.length);
    spans.forEach((el, i) => {
      const r = el.getClientRects()[0];
      this.tokenPage[i] = r ? Math.min(this.count - 1, Math.max(0, Math.floor((r.left - base + 2) / W))) : 0;
    });
    this.goToToken(keep, false);
  }

  pageOfToken(i) {
    return this.tokenPage[Math.max(0, Math.min(i, this.tokenPage.length - 1))] || 0;
  }

  firstTokenOnPage(p) {
    const i = this.tokenPage.findIndex((tp) => tp >= p);
    return i < 0 ? Math.max(0, this.tokens.length - 1) : i;
  }

  setPage(p, notify = true) {
    this.page = Math.max(0, Math.min(p, this.count - 1));
    this.pages.style.transform = `translateX(${-this.page * this.W}px)`;
    this.pos = this.page === 0 ? 0 : this.firstTokenOnPage(this.page);
    if (notify && this.hooks.onPage) this.hooks.onPage({ page: this.page, count: this.count, pos: this.pos, total: this.tokens.length });
  }

  goToToken(i, notify = true) { this.setPage(this.pageOfToken(i), notify); }
  next() { if (this.page < this.count - 1) { this.setPage(this.page + 1); return true; } return false; }
  prev() { if (this.page > 0) { this.setPage(this.page - 1); return true; } return false; }
  atEnd() { return this.page >= this.count - 1; }

  sentenceOfToken(i) { return (this.tokens[i] || this.tokens[0] || { si: 0 }).si; }
  currentSentence() { return this.sentenceOfToken(this.pos); }

  ensureSentenceVisible(si) {
    const first = this.sents[si] && this.sents[si].first;
    if (first == null) return;
    const p = this.pageOfToken(first);
    if (p !== this.page) this.setPage(p);
  }

  // ---- highlights
  clearHighlights() {
    this.pages.querySelectorAll('.w.hl, .sn.hl').forEach((el) => el.classList.remove('hl'));
  }
  highlightWord(i) {
    this.clearHighlights();
    const el = this.pages.querySelector(`.w[data-t="${i}"]`);
    if (el) el.classList.add('hl');
  }
  highlightSentence(si) {
    this.clearHighlights();
    const el = this.pages.querySelector(`.sn[data-s="${si}"]`);
    if (el) el.classList.add('hl');
  }

  // ---- input: own tap / long-press / swipe handling (native selection is unreliable on mobile)
  bind() {
    const stage = this.vp.parentElement;
    let down = null;
    let timer = null;
    const clear = () => { clearTimeout(timer); timer = null; };
    stage.addEventListener('contextmenu', (e) => e.preventDefault());
    stage.addEventListener('pointerdown', (e) => {
      if (e.button > 0) return;
      down = { x: e.clientX, y: e.clientY, target: e.target, moved: false, long: false };
      clear();
      timer = setTimeout(() => {
        if (!down || down.moved) return;
        const sn = down.target.closest && down.target.closest('.sn');
        if (sn) { down.long = true; this.hooks.onSentence && this.hooks.onSentence(+sn.dataset.s); }
      }, 480);
    });
    stage.addEventListener('pointermove', (e) => {
      if (down && (Math.abs(e.clientX - down.x) > 10 || Math.abs(e.clientY - down.y) > 10)) { down.moved = true; clear(); }
    });
    stage.addEventListener('pointercancel', () => { clear(); down = null; });
    stage.addEventListener('pointerup', (e) => {
      clear();
      const d = down;
      down = null;
      if (!d || d.long) return;
      const dx = e.clientX - d.x;
      const dy = e.clientY - d.y;
      if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy) * 1.5) {
        dx < 0 ? this.next() : this.prev();
        this.hooks.onTapAway && this.hooks.onTapAway(true);
        return;
      }
      if (d.moved) return;
      const w = e.target.closest && e.target.closest('.w');
      if (w) { this.hooks.onWord && this.hooks.onWord(+w.dataset.t); return; }
      if (this.hooks.onTapAway && this.hooks.onTapAway(false)) return; // a sheet was open: that tap just closed it
      const rect = stage.getBoundingClientRect();
      if (e.clientY - rect.top < 56) { this.hooks.onCenterTap && this.hooks.onCenterTap(); return; } // top strip always toggles the menu
      const f = (e.clientX - rect.left) / rect.width;
      if (f < 0.28) this.prev();
      else if (f > 0.72) this.next();
      else this.hooks.onCenterTap && this.hooks.onCenterTap();
    });
  }
}

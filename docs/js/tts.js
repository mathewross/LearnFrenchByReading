// Speech via the browser's speechSynthesis (fr-FR). Voices load asynchronously.
let voices = [];
let gen = 0; // bumps on every speak/stop so a cancelled utterance can't trigger the next one

function loadVoices() {
  try { voices = speechSynthesis.getVoices() || []; } catch (e) { voices = []; }
}

if ('speechSynthesis' in window) {
  loadVoices();
  try { speechSynthesis.addEventListener('voiceschanged', loadVoices); } catch (e) { /* old browsers */ }
}

export const supported = () => 'speechSynthesis' in window;

export function frenchVoice() {
  return voices.find((v) => v.lang === 'fr-FR')
    || voices.find((v) => v.lang && v.lang.toLowerCase().replace('_', '-').startsWith('fr'))
    || null;
}

export function status() {
  if (!supported()) return { ok: false, text: 'This browser has no speech synthesis.' };
  const v = frenchVoice();
  if (v) return { ok: true, text: `French voice: ${v.name}` };
  return {
    ok: false,
    text: 'No French voice found. On Android: Settings → System → Languages → Text-to-speech → install French voice data.',
  };
}

export function speak(text, { rate = 0.9, onstart, onend } = {}) {
  if (!supported()) return false;
  const my = ++gen;
  try {
    speechSynthesis.cancel();
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'fr-FR';
    const v = frenchVoice();
    if (v) u.voice = v;
    u.rate = rate;
    u.onstart = () => { if (my === gen && onstart) onstart(); };
    const done = () => { if (my === gen && onend) onend(); };
    u.onend = done;
    u.onerror = done;
    speechSynthesis.speak(u);
    return true;
  } catch (e) { return false; }
}

export function stop() {
  gen++;
  try { speechSynthesis.cancel(); } catch (e) { /* ignore */ }
}

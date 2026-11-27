// Service worker. VERSION is stamped by tools/build.py (hash of shipped files).
const VERSION = '226f384d28';
const SHELL_CACHE = 'lecture-shell-' + VERSION;
const DATA_CACHE = 'lecture-data'; // library, examples and stories: stale-while-revalidate
const SHELL = [
  './', 'index.html', 'css/style.css',
  'js/app.js', 'js/store.js', 'js/tts.js', 'js/reader.js',
  'manifest.webmanifest', 'icons/icon-192.png', 'icons/icon-512.png',
  'data/library.json', 'data/examples.json',
];

self.addEventListener('install', (e) => {
  e.waitUntil(caches.open(SHELL_CACHE).then((c) => c.addAll(SHELL)).then(() => self.skipWaiting()));
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k.startsWith('lecture-shell-') && k !== SHELL_CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== location.origin) return;

  if (url.pathname.includes('/data/') || url.pathname.includes('/img/')) {
    e.respondWith((async () => {
      const cache = await caches.open(DATA_CACHE);
      // newest copy first (data cache), then the precached shell copy
      const hit = (await cache.match(req)) || (await caches.match(req));
      const net = fetch(req).then((res) => { if (res.ok) cache.put(req, res.clone()); return res; }).catch(() => null);
      if (hit) { e.waitUntil(net); return hit; }
      return (await net) || new Response('{}', { status: 503, headers: { 'Content-Type': 'application/json' } });
    })());
    return;
  }

  e.respondWith(
    caches.match(req, { ignoreSearch: true }).then((hit) => {
      if (hit) return hit;
      return fetch(req).catch(() => (req.mode === 'navigate' ? caches.match('index.html') : Response.error()));
    })
  );
});

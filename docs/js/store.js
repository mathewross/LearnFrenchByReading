// Tiny key-value store: IndexedDB with an in-memory cache, localStorage fallback,
// and silent degradation if both are unavailable (state then lasts for the session).
const DB = 'lecture';
const STORE = 'kv';
const LS_KEY = 'lecture-kv';
let db = null;
const cache = new Map();

function openDb() {
  return new Promise((resolve) => {
    try {
      const req = indexedDB.open(DB, 1);
      req.onupgradeneeded = () => req.result.createObjectStore(STORE);
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => resolve(null);
      req.onblocked = () => resolve(null);
    } catch (e) { resolve(null); }
  });
}

export async function initStore() {
  db = await openDb();
  if (db) {
    await new Promise((resolve) => {
      try {
        const cur = db.transaction(STORE).objectStore(STORE).openCursor();
        cur.onsuccess = () => {
          const c = cur.result;
          if (c) { cache.set(c.key, c.value); c.continue(); } else resolve();
        };
        cur.onerror = () => resolve();
      } catch (e) { resolve(); }
    });
  } else {
    try {
      const raw = localStorage.getItem(LS_KEY);
      if (raw) for (const [k, v] of Object.entries(JSON.parse(raw))) cache.set(k, v);
    } catch (e) { /* storage unavailable: in-memory only */ }
  }
}

export function get(key, fallback) {
  return cache.has(key) ? cache.get(key) : fallback;
}

export function set(key, value) {
  cache.set(key, value);
  try {
    if (db) db.transaction(STORE, 'readwrite').objectStore(STORE).put(value, key);
    else localStorage.setItem(LS_KEY, JSON.stringify(Object.fromEntries(cache)));
  } catch (e) { /* ignore storage failures */ }
}

export function exportAll() {
  return JSON.stringify({ app: 'lecture', version: 1, exported: new Date().toISOString(), data: Object.fromEntries(cache) }, null, 1);
}

export function importAll(text) {
  const o = JSON.parse(text);
  if (o.app !== 'lecture' || !o.data) throw new Error('This is not a Lecture backup file.');
  for (const [k, v] of Object.entries(o.data)) set(k, v);
}

export async function requestPersistence() {
  try { return navigator.storage && navigator.storage.persist ? await navigator.storage.persist() : false; }
  catch (e) { return false; }
}

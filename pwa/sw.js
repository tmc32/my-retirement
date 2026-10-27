const CACHE = "countdown-v2";
const FILES = ["./", "index.html", "app.js", "holidays.js", "manifest.json", "icon.svg"];

self.addEventListener("install", (e) => e.waitUntil(caches.open(CACHE).then((c) => c.addAll(FILES))));

self.addEventListener("activate", (e) =>
  e.waitUntil(caches.keys().then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k)))))
);

// Network first so updates arrive, falling back to cache when offline
self.addEventListener("fetch", (e) =>
  e.respondWith(fetch(e.request).catch(() => caches.match(e.request)))
);

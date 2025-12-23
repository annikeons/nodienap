const CACHE_NAME = 'nodie-cache-v1';
const urlsToCache = [
  '/',
  '/mainx.html',
  '/stylex.css',
  '/sleeper duck.png'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request)
      .then(response => response || fetch(e.request))
  );
});

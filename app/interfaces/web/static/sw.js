// Exists solely to satisfy browser installability criteria for "Add to Home
// Screen" / desktop install. No caching — this is a live dashboard, and
// serving stale data or auth state from a cache would be worse than no
// offline support at all.
self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(self.clients.claim());
});

self.addEventListener("fetch", (event) => {
  event.respondWith(fetch(event.request));
});

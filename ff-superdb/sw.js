/* FF SuperDB service worker — offline shell caching.
   API data (Sleeper/ESPN) is intentionally NETWORK-FIRST so scores stay fresh;
   the app shell is cache-first so it opens instantly and works offline. */
const SHELL = "ffsuperdb-shell-v3";
const SHELL_FILES = ["./", "./index.html", "./manifest.json"];

self.addEventListener("install", e => {
  self.skipWaiting();
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(SHELL_FILES)).catch(() => {}));
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.filter(k => k !== SHELL).map(k => caches.delete(k))
    )).then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET") return;

  // Never cache API calls — always go to network so league data is live.
  if (url.hostname.includes("api.sleeper.app") ||
      url.hostname.includes("fantasy.espn.com") ||
      url.hostname.includes("sleepercdn.com")) {
    return; // default browser network handling
  }

  // App shell: network-first so live edits show on the next refresh; fall back
  // to cache only when offline. Keeps the cache warm for offline use.
  e.respondWith(
    fetch(e.request).then(res => {
      if (res && res.ok) {
        const copy = res.clone();
        caches.open(SHELL).then(c => c.put(e.request, copy)).catch(() => {});
      }
      return res;
    }).catch(() => caches.match(e.request))
  );
});

/*
 * Cross-origin isolation shim.
 *
 * input() has to block until the user types a line. The Python worker does that
 * with Atomics.wait on a SharedArrayBuffer, and SharedArrayBuffer is only handed
 * out to cross-origin isolated pages - which needs COOP/COEP response headers.
 * GitHub Pages cannot send custom headers, but a service worker can add them to
 * our own responses, so the page becomes isolated after one reload.
 *
 * Nothing is cached: every request is passed straight to the network and only the
 * headers of same-origin responses are rewritten. Cross-origin requests are left
 * alone - jsDelivr already sends Cross-Origin-Resource-Policy, and the Skulpt
 * scripts are loaded CORS-mode (crossorigin="anonymous"), which also satisfies
 * require-corp.
 */
if (typeof window === "undefined") {
  // ---------------- service worker side ----------------
  self.addEventListener("install", () => self.skipWaiting());
  self.addEventListener("activate", (event) => event.waitUntil(self.clients.claim()));

  self.addEventListener("fetch", (event) => {
    const request = event.request;
    // Range requests must be passed through untouched or media/wasm streaming breaks.
    if (request.cache === "only-if-cached" && request.mode !== "same-origin") return;

    let sameOrigin = false;
    try { sameOrigin = new URL(request.url).origin === self.location.origin; } catch (e) { /* opaque */ }
    if (!sameOrigin) return;   // let the browser fetch it normally

    event.respondWith(
      fetch(request)
        .then((response) => {
          // An opaque/!ok body cannot be re-wrapped; hand it back as-is.
          if (!response || response.status === 0 || response.type === "opaque") return response;
          const headers = new Headers(response.headers);
          headers.set("Cross-Origin-Embedder-Policy", "require-corp");
          headers.set("Cross-Origin-Opener-Policy", "same-origin");
          return new Response(response.body, {
            status: response.status,
            statusText: response.statusText,
            headers
          });
        })
        .catch(() => fetch(request))
    );
  });
} else {
  // ---------------- page side ----------------
  (function registerCoi() {
    const FLAG = "coiReloaded";

    if (window.crossOriginIsolated) {
      // Already isolated - clear the guard so a future failure can retry.
      try { sessionStorage.removeItem(FLAG); } catch (e) { /* private mode */ }
      return;
    }
    if (!window.isSecureContext || !navigator.serviceWorker) return;

    // Only ever reload once per tab, so a browser that refuses isolation
    // (or private mode without storage) can never get stuck in a loop.
    function reloadOnce() {
      let already = "1";
      try { already = sessionStorage.getItem(FLAG); } catch (e) { return; }
      if (already === "1") return;
      try { sessionStorage.setItem(FLAG, "1"); } catch (e) { return; }
      window.location.reload();
    }

    navigator.serviceWorker
      .register(new URL("coi-serviceworker.js", window.location.href), {
        scope: "./",
        updateViaCache: "none"
      })
      .then((registration) => {
        if (navigator.serviceWorker.controller) {
          // Controlled but still not isolated: the headers arrive on the next load.
          reloadOnce();
        } else {
          navigator.serviceWorker.addEventListener("controllerchange", reloadOnce, { once: true });
          if (registration.active && !navigator.serviceWorker.controller) reloadOnce();
        }
      })
      .catch(() => { /* no isolation; run.html falls back to a prompt dialog */ });
  })();
}

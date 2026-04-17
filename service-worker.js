// F.R.I.D.A.Y. Service Worker - Offline Support & Caching
const CACHE_NAME = 'friday-ai-v1';
const urlsToCache = [
  '/',
  '/index.html',
  '/manifest.json',
  '/api/health',
  '/api/info'
];

// Install Service Worker
self.addEventListener('install', (event) => {
  console.log('[Service Worker] Installing...');
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      console.log('[Service Worker] Caching assets');
      return cache.addAll(urlsToCache);
    })
  );
  self.skipWaiting();
});

// Activate Service Worker
self.addEventListener('activate', (event) => {
  console.log('[Service Worker] Activating...');
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[Service Worker] Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
  self.clients.claim();
});

// Fetch Event - Network First, Cache Fallback
self.addEventListener('fetch', (event) => {
  const { request } = event;
  const url = new URL(request.url);

  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }

  // Handle API requests (Network First, then Cache)
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(
      fetch(request)
        .then((response) => {
          // Cache successful API responses
          if (response.ok) {
            const cacheCopy = response.clone();
            caches.open(CACHE_NAME).then((cache) => {
              cache.put(request, cacheCopy);
            });
          }
          return response;
        })
        .catch(() => {
          // Return cached version if network fails
          return caches.match(request).then((response) => {
            return response || new Response(
              JSON.stringify({
                success: false,
                error: 'Offline - Unable to reach server',
                cached: true
              }),
              { status: 503, headers: { 'Content-Type': 'application/json' } }
            );
          });
        })
    );
    return;
  }

  // Handle HTML, CSS, JS (Cache First, then Network)
  event.respondWith(
    caches.match(request)
      .then((response) => {
        if (response) {
          console.log('[Service Worker] Serving from cache:', request.url);
          return response;
        }

        return fetch(request).then((response) => {
          // Cache successful responses
          if (!response || response.status !== 200 || response.type === 'error') {
            return response;
          }

          const responseCopy = response.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseCopy);
          });

          return response;
        });
      })
      .catch(() => {
        // Offline fallback
        return new Response(
          '<h1>F.R.I.D.A.Y. Offline</h1><p>You\'re offline, but your conversations are saved locally!</p>',
          { headers: { 'Content-Type': 'text/html' } }
        );
      })
  );
});

// Background Sync (Future: Sync messages when back online)
self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-messages') {
    event.waitUntil(
      // Future: Sync pending messages with server
      Promise.resolve()
    );
  }
});

// Push Notifications
self.addEventListener('push', (event) => {
  const options = {
    body: event.data ? event.data.text() : 'F.R.I.D.A.Y. has a message for you!',
    icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><rect fill="%2300d4ff" width="96" height="96"/><text x="48" y="65" font-size="60" font-weight="bold" text-anchor="middle" fill="%231a1a2e">F</text></svg>',
    badge: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96"><circle cx="48" cy="48" r="48" fill="%2300d4ff"/></svg>',
    tag: 'friday-notification',
    requireInteraction: false,
    actions: [
      {
        action: 'open',
        title: 'Open Chat'
      },
      {
        action: 'close',
        title: 'Dismiss'
      }
    ]
  };

  event.waitUntil(
    self.registration.showNotification('F.R.I.D.A.Y.', options)
  );
});

// Notification Click Handler
self.addEventListener('notificationclick', (event) => {
  event.notification.close();

  if (event.action === 'open' || !event.action) {
    event.waitUntil(
      clients.matchAll({ type: 'window' }).then((clientList) => {
        for (let i = 0; i < clientList.length; i++) {
          const client = clientList[i];
          if (client.url === '/' && 'focus' in client) {
            return client.focus();
          }
        }
        if (clients.openWindow) {
          return clients.openWindow('/');
        }
      })
    );
  }
});

console.log('[Service Worker] F.R.I.D.A.Y. Service Worker Ready!');

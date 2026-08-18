const CACHE_NAME = 'carecap-cache-v2'; // อัปเดตเลขเวอร์ชันทุกครั้งที่แก้ webapp เพื่อบังคับให้ browser ดึงไฟล์ใหม่ (แก้ปัญหา cache ค้าง)
const APP_SHELL = ['./', './index.html', './manifest.json', './icon-192.png', './icon-512.png'];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(APP_SHELL))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_NAME).map((k) => caches.delete(k)))
    )
  );
  self.clients.claim();
});

// Cache-first สำหรับไฟล์ app shell, ปล่อยผ่านตรงสำหรับ request ไป Google Apps Script (ข้อมูล real-time ต้องสดเสมอ)
self.addEventListener('fetch', (event) => {
  const url = event.request.url;
  if (url.includes('script.google.com')) {
    return; // ไม่ cache ข้อมูล real-time
  }
  event.respondWith(
    caches.match(event.request).then((cached) => cached || fetch(event.request))
  );
});

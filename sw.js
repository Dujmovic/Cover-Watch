/* Cover Watch service worker: shows lock-screen alerts sent by the Cloudflare helper. */
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>e.waitUntil(self.clients.claim()));
self.addEventListener('push',e=>{
  let d={};
  try{d=e.data?e.data.json():{}}catch(x){try{d={body:e.data.text()}}catch(y){}}
  /* iPhone requires every push to show a notification, so this always shows one. */
  e.waitUntil(self.registration.showNotification(d.title||'Cover Watch',{
    body:d.body||'Open Cover Watch to see the latest.',
    tag:d.tag||undefined,
    icon:'icon-192.png',
    timestamp:d.t||Date.now(),
    data:{url:'./'}
  }));
});
self.addEventListener('notificationclick',e=>{
  e.notification.close();
  e.waitUntil(self.clients.matchAll({type:'window',includeUncontrolled:true}).then(list=>{
    for(const c of list){if('focus' in c)return c.focus()}
    return self.clients.openWindow('./');
  }));
});

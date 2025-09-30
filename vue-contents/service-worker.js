self.addEventListener('push', event => {
    const data = event.data ? event.data.text() : '運動しよう！';
    event.waitUntil(
      self.registration.showNotification('FitSpin', {
        body: data,
        icon: '/icons/icon-192.png'
      })
    );
  });
  
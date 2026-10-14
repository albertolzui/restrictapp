fetch('/api/privacy').then(response => response.json()).then(data => {
  document.getElementById('operator').textContent = data.operator;
  const contact = document.getElementById('contact');
  contact.textContent = data.contact;
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.contact)) contact.href = 'mailto:' + data.contact;
}).catch(() => {});

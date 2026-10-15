fetch('/api/privacy').then(response => { if(!response.ok)throw new Error('Contact details unavailable');return response.json(); }).then(data => {
  if(typeof data.operator!=='string' || typeof data.contact!=='string')throw new Error('Invalid contact response');
  document.getElementById('operator').textContent = data.operator;
  const contact = document.getElementById('contact');
  contact.textContent = data.contact;
  if (/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.contact)) contact.href = 'mailto:' + data.contact;
}).catch(() => {
  const notice=document.createElement('p');notice.className='error';notice.setAttribute('role','status');
  notice.textContent=t('Live contact details could not be loaded. The contact details printed above are still available.');
  document.querySelector('main').append(notice);
});

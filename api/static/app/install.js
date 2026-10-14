(() => {
  const button = document.getElementById('install-app');
  const dialog = document.getElementById('install-dialog');
  const promptButton = document.getElementById('install-confirm');
  const status = document.getElementById('install-status');
  let installPrompt = null;
  const standalone = window.matchMedia('(display-mode: standalone)');
  const update = () => { button.hidden = standalone.matches || navigator.standalone === true; };
  update();
  standalone.addEventListener('change', update);
  window.addEventListener('beforeinstallprompt', event => {
    event.preventDefault(); installPrompt = event; promptButton.hidden = false;
  });
  window.addEventListener('appinstalled', () => {
    installPrompt = null; promptButton.hidden = true; button.hidden = true;
    if (dialog.open) dialog.close();
  });
  button.onclick = () => { status.textContent = ''; dialog.showModal(); };
  document.getElementById('close-install').onclick = () => dialog.close();
  promptButton.onclick = async () => {
    if (!installPrompt) return;
    const pending = installPrompt; installPrompt = null; promptButton.hidden = true;
    try {
      await pending.prompt();
      const choice = await pending.userChoice;
      status.textContent = choice.outcome === 'accepted' ? 'Installation requested. Follow your browser’s instructions to finish.' : 'No problem. You can install later from your browser menu.';
    } catch { status.textContent = 'Use your browser menu to install Restrictapp, or follow the steps below.'; }
  };
  if ('serviceWorker' in navigator && window.isSecureContext) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js', {scope:'/', updateViaCache:'none'}).catch(() => {});
    });
  }
})();

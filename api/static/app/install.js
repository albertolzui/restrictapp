(() => {
  const buttons = document.querySelectorAll('[data-install-app]');
  const dialog = document.getElementById('install-dialog');
  const promptButton = document.getElementById('install-confirm');
  const status = document.getElementById('install-status');
  const isAppleMobile = /iPhone|iPad|iPod/i.test(navigator.userAgent) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
  const isAndroid = /Android/i.test(navigator.userAgent);
  const isDesktop = !isAppleMobile && !isAndroid;
  document.getElementById('install-ios').hidden = !isAppleMobile;
  document.getElementById('install-android').hidden = !isAndroid;
  document.getElementById('install-desktop').hidden = !isDesktop;
  if (isDesktop) {
    document.getElementById('install-title').textContent = 'Your travel space. One click away.';
    document.getElementById('install-description').textContent = 'Install Restrictapp on your computer and open your travel workspace in its own app window.';
  }
  let installPrompt = null;
  let prompting = false;
  const showHelp = (message = '') => {
    status.textContent = message;
    if (!dialog.open) dialog.showModal();
  };
  const standalone = window.matchMedia('(display-mode: standalone)');
  const update = () => { buttons.forEach(button => { button.hidden = standalone.matches || navigator.standalone === true; }); };
  update();
  standalone.addEventListener('change', update);
  window.addEventListener('beforeinstallprompt', event => {
    event.preventDefault();
    if (!isAppleMobile) { installPrompt = event; promptButton.hidden = false; }
  });
  window.addEventListener('appinstalled', () => {
    installPrompt = null; promptButton.hidden = true; buttons.forEach(button => { button.hidden = true; });
    if (dialog.open) dialog.close();
  });
  document.getElementById('close-install').onclick = () => dialog.close();
  const install = async () => {
    if (prompting) return;
    if (isAppleMobile) return showHelp();
    if (!installPrompt) return showHelp(isAndroid ? 'If the install prompt is unavailable, use Chrome’s menu as described below.' : 'Use your browser’s installation option, or follow the steps below.');
    const pending = installPrompt; installPrompt = null; promptButton.hidden = true; prompting = true;
    buttons.forEach(button => { button.disabled = true; });
    try {
      // Call during this click's user activation; no extra dialog or async work first.
      await pending.prompt();
      const choice = await pending.userChoice;
      status.textContent = choice.outcome === 'accepted' ? 'Installation requested. Follow your browser’s instructions to finish.' : 'No problem. You can install later from your browser menu.';
    } catch { showHelp('Use your browser menu to install Restrictapp, or follow the steps below.'); }
    finally { prompting = false; buttons.forEach(button => { button.disabled = false; }); }
  };
  buttons.forEach(button => { button.onclick = install; });
  promptButton.onclick = install;
  if ('serviceWorker' in navigator && window.isSecureContext) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/sw.js', {scope:'/', updateViaCache:'none'}).catch(() => {});
    });
  }
})();

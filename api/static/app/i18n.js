/* English source messages are stable catalogue keys; identifiers stay unchanged. */
(() => {
  const german = window.RestrictappLocales.de;
  const codes = window.RestrictappCountryCodes;
  const englishByGerman = new Map(Object.entries(german).map(([english,de])=>[de,english]));
  let language = 'en';
  try {
    const requested = new URL(location.href).searchParams.get('lang');
    const saved = localStorage.getItem('restrictapp_language');
    language = ['en','de'].includes(requested) ? requested : ['en','de'].includes(saved) ? saved : navigator.language?.startsWith('de') ? 'de' : 'en';
  } catch { language = navigator.language?.startsWith('de') ? 'de' : 'en'; }
  const names = {en:new Intl.DisplayNames(['en'],{type:'region'}),de:new Intl.DisplayNames(['de'],{type:'region'})};
  function country(id, lang = language) {
    if (!id) return '';
    if (lang === 'en') return id.replaceAll('-',' ');
    try { return codes[id] ? names.de.of(codes[id]) : id.replaceAll('-',' '); } catch { return id.replaceAll('-',' '); }
  }
  const normalize = value => value.normalize('NFC').trim().toLocaleLowerCase();
  function countryId(value) {
    const key = normalize(value);
    return Object.keys(codes).find(id => [id,country(id,'en'),country(id,'de')].some(label => normalize(label) === key));
  }
  function dynamic(message) {
    let match = message.match(/^Your (.+) passport is separate from your departure country\. Official requirements must match your traveler details\.$/);
    if (match) return `Dein Pass (${country(countryId(match[1]) || match[1])}) ist unabhängig vom Abreiseland zu betrachten. Offizielle Anforderungen müssen zu deinen persönlichen Reiseangaben passen.`;
    match = message.match(/^Review transit requirements in (.+), including whether you pass border control or change airports\.$/);
    if (match) return `Prüfe die Transitregeln in ${country(countryId(match[1]) || match[1])}, insbesondere bei Grenzkontrollen oder einem Flughafenwechsel.`;
    if (message.startsWith('Category withheld: publisher flags ')) {
      const flags = message.slice('Category withheld: publisher flags '.length).replace(/\.$/,'').split(', ').map(flag => ({'source could not be re-read':'Quelle konnte nicht erneut abgerufen werden','conflicting source information':'widersprüchliche Quellenangaben','portal-only evidence':'nur Portalbelege'})[flag] || flag);
      return 'Keine Kategorie angezeigt. Hinweise des Herausgebers: ' + flags.join(', ') + '.';
    }
    return message;
  }
  function translate(message, values = []) {
    if (typeof message !== 'string') return message;
    const [,before,core,after] = message.match(/^(\s*)([\s\S]*?)(\s*)$/);
    let translated = language === 'de' ? (german[core] ?? dynamic(core)) : core;
    if (core === '({0} days ago)' && Number(values[0]) === 1) translated = language === 'de' ? '(vor {0} Tag)' : '({0} day ago)';
    return before + translated.replace(/\{(\d+)\}/g,(whole,index) => values[index] ?? whole) + after;
  }
  const bindings = [];
  function collect() {
    const walker = document.createTreeWalker(document.documentElement, NodeFilter.SHOW_TEXT);
    while (walker.nextNode()) {
      const node=walker.currentNode;
      if (!node.parentElement.closest('script,style,code,[data-no-translate],#operator,#contact') && node.textContent.trim()) bindings.push({node,value:node.textContent});
    }
    document.querySelectorAll('[placeholder],[aria-label],[alt],meta[name="description"]').forEach(node => {
      for (const attribute of ['placeholder','aria-label','alt',...(node.tagName === 'META' ? ['content'] : [])]) {
        if (node.hasAttribute(attribute)) bindings.push({node,attribute,value:node.getAttribute(attribute)});
      }
    });
  }
  function apply() {
    try{document.cookie='restrictapp_language='+language+'; Path=/; Max-Age=31536000; SameSite=Lax'+(location.protocol==='https:'?'; Secure':'');}catch{}
    document.documentElement.lang=language;
    const manifest=document.querySelector('link[rel="manifest"]');
    if (manifest) manifest.setAttribute('href','/manifest.webmanifest?lang='+language);
    for (const {node,attribute,value} of bindings) {
      if (!node.isConnected) continue;
      if (attribute) node.setAttribute(attribute,translate(value)); else node.textContent=translate(value);
    }
    document.querySelectorAll('[data-language-select]').forEach(select => { select.value=language; });
    document.querySelectorAll('a[href]').forEach(link => {
      const url=new URL(link.getAttribute('href'),location.href);
      if (url.origin === location.origin && ['/','/privacy','/cookies'].includes(url.pathname) && !link.getAttribute('href').startsWith('#')) {
        url.searchParams.set('lang',language); link.setAttribute('href',url.pathname+url.search+url.hash);
      }
    });
  }
  function setLanguage(next, source='user') {
    if (!['en','de'].includes(next) || next === language) return;
    const fields = ['origin','destination','nationality','residence','transit'].map(id => document.getElementById(id)).filter(Boolean).map(node => ({node,id:countryId(node.value)}));
    language=next;
    try { localStorage.setItem('restrictapp_language',language); } catch {}
    const url=new URL(location.href); url.searchParams.set('lang',language); history.replaceState(null,'',url);
    apply();
    document.querySelectorAll('.error,.toast').forEach(node => { node.textContent=translate(englishByGerman.get(node.textContent) || node.textContent); });
    document.querySelectorAll('input').forEach(input => input.setCustomValidity(''));
    for (const field of fields) if (field.id) field.node.value=country(field.id);
    window.dispatchEvent(new CustomEvent('restrictapp:languagechange',{detail:{source}}));
  }
  function localizeData(value) {
    if (typeof value === 'string') return translate(value);
    if (Array.isArray(value)) return value.map(localizeData);
    if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key,item]) => [key,['source','sources','links'].includes(key) ? item : ['notes','limitations','title','detail','scope','message','reason','category_label','attribution','role'].includes(key) ? localizeData(item) : typeof item === 'object' ? localizeData(item) : item]));
    return value;
  }
  window.I18n = {t:translate,country,countryId,setLanguage,localizeData,get language(){return language;},date:(value,time=false)=>new Date(value)[time?'toLocaleString':'toLocaleDateString'](language === 'de'?'de-DE':'en-GB')};
  window.t=translate;
  collect(); apply();
  document.querySelectorAll('[data-language-select]').forEach(select => select.addEventListener('change',()=>setLanguage(select.value)));
  document.querySelectorAll('input').forEach(input => {
    input.addEventListener('input',()=>input.setCustomValidity(''));
    input.addEventListener('invalid',()=>{
      input.setCustomValidity('');
      if (input.validity.valueMissing) input.setCustomValidity(translate(input.type === 'checkbox' ? 'Please check this box to continue.' : 'Please fill out this field.'));
      else if (input.validity.typeMismatch) input.setCustomValidity(translate('Please enter a valid email address.'));
      else if (input.validity.tooShort) input.setCustomValidity(translate('Please use at least 10 characters.'));
      else if (!input.validity.valid) input.setCustomValidity(translate('Please check your entries and try again.'));
    });
  });
})();

const $ = id => document.getElementById(id);
let countries = [], user = null, currentRoute = null, authMode = 'login', pendingSave = false;
let currentPlan = null, savedTripId = null, checkedTasks = new Set(), searchVersion = 0;
const display = value => value.replaceAll('-', ' ');
async function api(path, options = {}) {
  const response = await fetch(path, {...options, headers: {'Content-Type': 'application/json', 'X-Restrictapp': '1', ...options.headers}});
  const data = await response.json();
  if (!response.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Please check your entries and try again.');
  return data;
}
function toast(message) { $('toast').textContent = message; $('toast').hidden = false; clearTimeout(toast.timer); toast.timer = setTimeout(() => $('toast').hidden = true, 4500); }
function accountUI() { $('account-button').textContent = user ? 'Sign out ↗' : 'Sign in ↗'; $('account-side').textContent = user ? 'View your saved trips ↗' : 'Create your travel account ↗'; }
function openAuth(mode = 'login') { authMode = mode; $('auth-title').textContent = mode === 'login' ? 'Welcome back.' : 'Your next chapter starts here.'; $('auth-submit').textContent = mode === 'login' ? 'Sign in ↗' : 'Create account ↗'; $('toggle-auth').textContent = mode === 'login' ? 'New here? Create an account' : 'Already have an account? Sign in'; $('password').autocomplete = mode === 'login' ? 'current-password' : 'new-password'; $('auth-error').textContent = ''; if (!$('auth-dialog').open) $('auth-dialog').showModal(); }
function view(name) { $('explore-view').hidden = name !== 'explore'; $('trips-view').hidden = name !== 'trips'; $('explore-nav').classList.toggle('active', name === 'explore'); $('trips-nav').classList.toggle('active', name === 'trips'); $('page-name').textContent = name === 'trips' ? 'My saved trips' : 'Explore'; }
function countryValue(value) { return countries.find(country => display(country).toLowerCase() === value.trim().toLowerCase()); }
function travelerContext() {
  const nationality = countryValue($('nationality').value), residence = countryValue($('residence').value);
  const transitText = $('transit').value.trim(), transit = transitText ? countryValue(transitText) : '';
  if (!nationality || !residence || (transitText && !transit)) throw new Error('Choose your passport, residence, and any transit country from the list.');
  return {nationality, residence, transit, passport_expiry:$('passport-expiry').value || null, departure_date:$('departure-date').value || null, return_date:$('return-date').value || null, purpose:$('purpose').value};
}
function applyContext(context) {
  for (const field of ['nationality', 'residence', 'transit']) $(field).value = context[field] ? display(context[field]) : '';
  for (const field of ['passport_expiry','departure_date','return_date']) $(field.replaceAll('_','-')).value = context[field] || '';
  $('purpose').value = context.purpose || 'tourism';
}
async function loadProfile() {
  if (!user) return;
  try { const profile = await api('/api/profile'); if (!currentRoute && profile.nationality) applyContext(profile); }
  catch (error) { toast(error.message); }
}
function taskElement(task, done, onChange) {
  const label = document.createElement('label'); label.className = 'checklist-item';
  const input = document.createElement('input'); input.type = 'checkbox'; input.checked = done;
  const text = document.createElement('span'); const title = document.createElement('b'); title.textContent = task.title;
  const detail = document.createElement('small'); detail.textContent = task.detail; text.append(title,detail);
  input.onchange = async () => { input.disabled = true; try { await onChange(input.checked); } catch (error) { input.checked = !input.checked; toast(error.message); } finally { input.disabled = false; } };
  label.append(input,text); return label;
}
function renderChecklist(tasks) {
  $('plan-checklist').replaceChildren();
  const updateCount = () => $('checklist-count').textContent = `${checkedTasks.size} of ${tasks.length} checks completed`;
  for (const task of tasks) $('plan-checklist').append(taskElement(task, checkedTasks.has(task.id), async done => {
    if (savedTripId && user) await api(`/api/trips/${savedTripId}/checklist/${task.id}`, {method:'PUT', body:JSON.stringify({done})});
    if (done) checkedTasks.add(task.id); else checkedTasks.delete(task.id); updateCount();
    if (savedTripId) await loadTrips();
  }));
  updateCount(); $('checklist-saving').textContent = savedTripId ? 'Checklist changes are saved to this trip.' : 'Save this trip to keep your checklist between visits.';
}
function renderPlan(result) {
  $('traveler-summary').replaceChildren();
  const context = result.traveler;
  for (const text of [`${display(context.nationality)} passport`, `Resident in ${display(context.residence)}`, `${context.purpose} trip`, ...(context.departure_date ? [context.departure_date + (context.return_date ? ' → '+context.return_date : '')] : [])]) {
    const chip = document.createElement('span'); chip.textContent = text; $('traveler-summary').append(chip);
  }
  $('planning-notes').replaceChildren();
  result.notes.forEach(note => { const p = document.createElement('p'); p.className = 'plan-note'; p.textContent = note; $('planning-notes').append(p); });
  $('result-scope').textContent = result.scope; renderChecklist(result.checklist);
  renderEntryReference(result.entry_reference, result.status);
  for (const source of result.authority_links || []) { const link = document.createElement('a'); link.textContent = source.role + ': ' + source.title + ' ↗'; link.href = source.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.className = 'outline source-link'; $('result-sources').append(link); }
  $('official-guidance').replaceChildren(); $('load-guidance').disabled = false; $('load-guidance').textContent = 'Load official guidance ↗';
}
function renderEntryReference(reference, routeStatus) {
  let section = $('entry-reference');
  if (!section) { section = document.createElement('section'); section.id = 'entry-reference'; section.className = 'entry-reference'; $('requirements').before(section); }
  section.replaceChildren();
  if (!reference) return;
  const heading = document.createElement('h2'); heading.textContent = 'Passport-based visa reference'; section.append(heading);
  const badge = document.createElement('span'); badge.className = 'status-chip'; badge.textContent = reference.status === 'dataset_reported' ? 'Dataset-reported · confirm with authority' : 'Official links · category withheld'; section.append(badge);
  if (reference.category_label) { const category = document.createElement('h3'); category.textContent = 'Publisher baseline: ' + reference.category_label; section.append(category); }
  const reason = document.createElement('p'); reason.textContent = reference.reason; section.append(reason);
  const scope = document.createElement('p'); scope.className = 'scope-note'; scope.textContent = 'Short-stay tourism only. Residence-permit and existing-visa exceptions have not been applied. Your country of residence alone does not establish an exemption. Transit must be checked separately.'; section.append(scope);
  const dates = document.createElement('p'); dates.className = 'search-note'; dates.textContent = `Publisher check: ${reference.publisher_checked_at || 'not available'}${reference.check_age_days != null ? ` (${reference.check_age_days} days ago)` : ''}. Snapshot imported: ${reference.imported_at ? new Date(reference.imported_at).toLocaleDateString() : 'not available'}. These are different dates; Restrictapp has not independently verified this result.`; section.append(dates);
  if (reference.evidence_level) { const evidence = document.createElement('p'); evidence.className = 'search-note'; evidence.textContent = reference.evidence_level === 'passport-row' ? 'Supporting text is recorded for the passport row by the publisher.' : 'Citation scope: destination policy; not an individually evidenced passport row.'; section.append(evidence); }
  const links = document.createElement('div');
  for (const source of reference.links || []) { const wrapper = document.createElement('div'); const link = document.createElement('a'); link.href = source.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.className = 'outline source-link'; link.textContent = source.title+' ↗'; const meta = document.createElement('p'); meta.className = 'search-note'; meta.textContent = `Publisher source label: ${source.type}; publisher check: ${source.publisher_checked_at || 'not supplied'}.`; wrapper.append(link,meta); links.append(wrapper); }
  section.append(links);
  const details = document.createElement('details'); details.className = 'guidance-section'; const summary = document.createElement('summary'); summary.textContent = 'Scope and limitations'; details.append(summary);
  for (const limitation of reference.limitations || []) { const p = document.createElement('p'); p.textContent = limitation; details.append(p); } section.append(details);
  const credit = document.createElement('p'); credit.className = 'guidance-attribution'; credit.textContent = reference.attribution || 'Independent reference data; no eligibility decision.';
  for (const [title,url] of [[' Dataset and methodology',reference.dataset_url],[' Licence',reference.license_url]]) { if (url) { const link = document.createElement('a'); link.textContent = title; link.href = url; link.target = '_blank'; link.rel = 'noopener noreferrer'; credit.append(link); } } section.append(credit);
  if (reference.version) { const meta = document.createElement('p'); meta.className = 'search-note'; meta.textContent = `Dataset version ${reference.version}; snapshot ${reference.commit?.slice(0,12) || 'unknown'}. Independent compilation; some sources describe another country's rules.`; section.append(meta); }
  if (routeStatus === 'unverified') { $('result-status').textContent = 'Personalized eligibility not checked'; $('result-message').textContent = reference.status === 'dataset_reported' ? 'The passport-based reference below is a starting point for short-stay tourism. Check the cited authority for your residence permits, document type, dates, and itinerary.' : 'A reference category could not be responsibly shown for these details. Use the source links below to check the official rules.'; $('result-freshness').textContent = 'Reference check dates are shown per source below. No personalized immigration check has been performed.'; }
}
function renderData(result) {
  $('result-status').textContent = {unverified:'Not yet verified', stale:'Source needs a fresh check', sourced:'Sourced information'}[result.status];
  $('result-freshness').textContent = result.checked_at ? `Last checked: ${new Date(result.checked_at).toLocaleString()}. ${result.status === 'stale' ? 'This information is older than 24 hours. ' : ''}Confirm requirements for your passport and dates with the official authority.` : 'No verified source or check date is available yet. This result does not confirm permission to enter.';
  const items = result.requirements.length ? result.requirements : [{title:'Passport & visa',detail:'Confirm eligibility with the destination’s immigration authority.'},{title:'Entry & health',detail:'Check official entry conditions and health requirements for your dates.'},{title:'Before departure',detail:'Review transit rules and your airline’s document checklist.'}];
  $('requirements').replaceChildren();
  $('requirements').hidden = !result.requirements.length;
  items.forEach((item,index) => { const article = document.createElement('article'); const number = document.createElement('span'); number.textContent = String(index+1).padStart(2,'0'); const title = document.createElement('h3'); title.textContent = item.title; const detail = document.createElement('p'); detail.textContent = item.detail; article.append(number,title,detail); $('requirements').append(article); });
  $('result-sources').replaceChildren();
  (result.sources || []).forEach(source => { const link = document.createElement('a'); link.textContent = source.title + ' ↗'; link.href = source.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.className = 'outline source-link'; $('result-sources').append(link); });
}
async function search(event) {
  event?.preventDefault(); $('search-error').textContent = ''; $('results').hidden = true; currentRoute = null;
  const version = ++searchVersion; savedTripId = null; checkedTasks = new Set(); currentPlan = null;
  const origin = countryValue($('origin').value), destination = countryValue($('destination').value);
  if (!origin || !destination) { $('search-error').textContent = 'Choose an origin and destination from the country list.'; return; }
  $('search-button').disabled = true;
  try { const context = travelerContext(); const result = await api('/api/plan', {method:'POST',body:JSON.stringify({origin, destination,...context})}); if (version !== searchVersion) return; currentRoute = {origin, destination,...context}; currentPlan = result; $('result-title').textContent = `${display(origin)} → ${display(destination)}`; $('result-message').textContent = result.message; renderData(result); renderPlan(result); $('results').hidden = false; $('results').scrollIntoView({behavior:'smooth', block:'start'}); }
  catch (error) { $('search-error').textContent = error.message; }
  finally { $('search-button').disabled = false; }
}
async function saveRoute() {
  if (!currentRoute) return;
  if (!user) { pendingSave = true; openAuth('signup'); return; }
  $('save-route').disabled = true;
  try { const response = await api('/api/trips', {method:'POST', body:JSON.stringify(currentRoute)}); savedTripId = response.id; for (const id of checkedTasks) await api(`/api/trips/${savedTripId}/checklist/${id}`, {method:'PUT',body:JSON.stringify({done:true})}); const stored = (await api('/api/trips')).find(trip => trip.id === savedTripId); checkedTasks = new Set(stored.checklist.filter(task => task.done).map(task => task.id)); renderChecklist(currentPlan.checklist); toast('Trip and preparation plan saved.'); await loadTrips(); }
  catch (error) { toast(error.message); }
  finally { $('save-route').disabled = false; }
}
function emptyTrips(title, message) { $('trip-list').replaceChildren(); const box = document.createElement('div'); box.className = 'empty'; const h = document.createElement('h2'); h.textContent = title; const p = document.createElement('p'); p.className = 'subtle'; p.textContent = message; box.append(h,p); $('trip-list').append(box); }
async function loadTrips() {
  if (!user) { $('trip-count').textContent = '0'; emptyTrips('Make room for your next journey.', 'Sign in to save and revisit your travel plans.'); return; }
  try {
    const trips = await api('/api/trips'); $('trip-count').textContent = trips.length; $('trip-list').replaceChildren();
    if (!trips.length) { emptyTrips('A world of possibility awaits.', 'Explore a route and save your first trip.'); return; }
    for (const trip of trips) {
      const row = document.createElement('article'); row.className = 'trip-row';
      const info = document.createElement('div'); const title = document.createElement('h3'); title.textContent = `${display(trip.origin)} → ${display(trip.destination)}`;
      const note = document.createElement('span'); note.className = 'subtle'; note.textContent = trip.context.nationality ? `${display(trip.context.nationality)} passport · ${trip.context.departure_date || 'Dates to be decided'}` : 'Add traveler details to create your plan'; info.append(title,note);
      const actions = document.createElement('div'); actions.className = 'trip-actions'; const open = document.createElement('button'); open.className = 'outline'; open.textContent = 'View plan ↗';
      open.onclick = async () => { view('explore'); $('origin').value = display(trip.origin); $('destination').value = display(trip.destination); applyContext(trip.context); if (!trip.context.nationality || !trip.context.residence) { $('nationality').focus(); toast('Add your passport country and residence to plan this trip.'); return; } await search(); if (currentPlan) { savedTripId = trip.id; checkedTasks = new Set(trip.checklist.filter(task => task.done).map(task => task.id)); renderChecklist(currentPlan.checklist); } };
      const remove = document.createElement('button'); remove.className = 'outline'; remove.textContent = 'Remove'; remove.setAttribute('aria-label', `Remove trip to ${display(trip.destination)}`);
      remove.onclick = async () => { remove.disabled = true; try { await api(`/api/trips/${trip.id}`, {method:'DELETE'}); if (savedTripId === trip.id) { savedTripId = null; if (currentPlan) renderChecklist(currentPlan.checklist); } await loadTrips(); toast('Trip removed.'); } catch (error) { toast(error.message); remove.disabled = false; } };
      actions.append(open,remove); row.append(info,actions);
      const details = document.createElement('details'); details.className = 'trip-checklist'; const summary = document.createElement('summary');
      const completed = trip.checklist.filter(task => task.done).length; summary.textContent = `Preparation checklist · ${completed}/${trip.checklist.length} completed`; details.append(summary);
      for (const task of trip.checklist) details.append(taskElement(task, task.done, async done => { await api(`/api/trips/${trip.id}/checklist/${task.id}`, {method:'PUT',body:JSON.stringify({done})}); task.done = done; summary.textContent = `Preparation checklist · ${trip.checklist.filter(t => t.done).length}/${trip.checklist.length} completed`; if (savedTripId === trip.id && currentPlan) { if (done) checkedTasks.add(task.id); else checkedTasks.delete(task.id); renderChecklist(currentPlan.checklist); } }));
      row.append(details); $('trip-list').append(row);
    }
  } catch (error) { emptyTrips('Could not load your trips.', error.message); }
}
$('search-form').onsubmit = search;
function invalidatePlan() { searchVersion++; currentRoute = null; currentPlan = null; savedTripId = null; checkedTasks = new Set(); $('results').hidden = true; }
for (const id of ['origin','destination','nationality','residence','passport-expiry','departure-date','return-date','purpose','transit']) $(id).addEventListener('input', invalidatePlan);
$('swap').onclick = () => { const origin = $('origin').value; $('origin').value = $('destination').value; $('destination').value = origin; invalidatePlan(); };
$('save-route').onclick = saveRoute;
$('explore-nav').onclick = () => view('explore');
$('trips-nav').onclick = () => { view('trips'); loadTrips(); };
$('new-trip').onclick = () => { view('explore'); $('origin').focus(); };
$('account-button').onclick = async () => { if (!user) return openAuth(); try { await api('/api/logout', {method:'POST'}); user = null; savedTripId = null; currentRoute = null; currentPlan = null; checkedTasks.clear(); $('results').hidden = true; $('search-form').reset(); accountUI(); await loadTrips(); toast('You are signed out.'); } catch (error) { toast(error.message); } };
$('account-side').onclick = () => { if (user) { view('trips'); loadTrips(); } else openAuth('signup'); };
$('close-auth').onclick = () => { pendingSave = false; $('auth-dialog').close(); };
$('auth-dialog').addEventListener('cancel', () => pendingSave = false);
$('toggle-auth').onclick = () => openAuth(authMode === 'login' ? 'signup' : 'login');
$('auth-form').onsubmit = async event => { event.preventDefault(); $('auth-submit').disabled = true; $('auth-error').textContent = ''; try { user = await api(`/api/auth/${authMode}`, {method:'POST', body:JSON.stringify({email:$('email').value, password:$('password').value})}); $('auth-dialog').close(); $('auth-form').reset(); accountUI(); await loadTrips(); await loadProfile(); toast('Welcome to your travel space.'); if (pendingSave) { pendingSave = false; await saveRoute(); } } catch (error) { $('auth-error').textContent = error.message; } finally { $('auth-submit').disabled = false; } };
document.querySelectorAll('[data-country]').forEach(card => card.onclick = () => { $('destination').value = card.dataset.country; $('search-form').scrollIntoView({behavior:'smooth', block:'center'}); if (!$('origin').value) $('origin').focus(); else search(); });
async function init() { $('year').textContent = new Date().getFullYear(); try { countries = await api('/api/countries'); for (const country of countries) { const option = document.createElement('option'); option.value = display(country); $('country-options').append(option); } } catch (error) { $('search-error').textContent = 'The country list could not load. Refresh to try again.'; } try { user = await api('/api/me'); } catch { user = null; } accountUI(); await loadTrips(); await loadProfile(); }
$('save-profile').onclick = async () => {
  if (!user) { openAuth(); toast('Sign in, then save your traveler profile.'); return; }
  $('save-profile').disabled = true;
  try { const context = travelerContext(); await api('/api/profile', {method:'PUT', body:JSON.stringify({nationality:context.nationality,residence:context.residence,passport_expiry:context.passport_expiry})}); toast('Traveler profile saved for future plans.'); }
  catch (error) { toast(error.message); } finally { $('save-profile').disabled = false; }
};
$('load-guidance').onclick = async () => {
  if (!currentRoute) return;
  const version = searchVersion, destination = currentRoute.destination; $('load-guidance').disabled = true; $('load-guidance').textContent = 'Loading guidance…';
  try {
    const guidance = await api('/api/guidance/' + encodeURIComponent(destination)); if (version !== searchVersion) return;
    $('official-guidance').replaceChildren(); const scope = document.createElement('p'); scope.className = 'scope-note'; scope.textContent = guidance.scope; $('official-guidance').append(scope);
    for (const section of guidance.sections) { const details = document.createElement('details'); details.className = 'guidance-section'; const summary = document.createElement('summary'); summary.textContent = section.title; const body = document.createElement('p'); body.textContent = section.text; const link = document.createElement('a'); link.href = section.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = 'Read the full official section ↗'; details.append(summary,body,link); $('official-guidance').append(details); }
    const attribution = document.createElement('p'); attribution.className = 'guidance-attribution'; const link = document.createElement('a'); link.href = guidance.url; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.textContent = 'Open GOV.UK guidance ↗'; attribution.append(link, document.createTextNode(guidance.status === 'available' ? ` · Published update: ${guidance.updated_at ? new Date(guidance.updated_at).toLocaleString() : 'not supplied'} · Retrieved: ${new Date(guidance.retrieved_at).toLocaleString()}. Contains public sector information licensed under the Open Government Licence v3.0.` : ' · Live content could not be loaded or is not available for this destination. Use the official site to check.'));
    if (guidance.status === 'available') { const license = document.createElement('a'); license.href = 'https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/'; license.textContent = ' View licence'; license.target = '_blank'; license.rel = 'noopener noreferrer'; attribution.append(license); }
    $('official-guidance').append(attribution);
  } catch (error) { if (version === searchVersion) { $('official-guidance').textContent = 'Official guidance could not load. Please try again.'; } }
  finally { if (version === searchVersion) { $('load-guidance').disabled = false; $('load-guidance').textContent = 'Refresh official guidance ↗'; } }
};
$('download-plan').onclick = () => {
  if (!currentPlan) return;
  const lines = ['RESTRICTAPP — PREPARATION PLAN', `${display(currentRoute.origin)} → ${display(currentRoute.destination)}`, `Passport: ${display(currentRoute.nationality)}; residence: ${display(currentRoute.residence)}`, `Dates: ${currentRoute.departure_date || 'Undecided'} → ${currentRoute.return_date || 'Undecided'}; purpose: ${currentRoute.purpose}`, `Transit: ${currentRoute.transit ? display(currentRoute.transit) : 'None specified'}`, '', ...currentPlan.notes, '', 'CHECKLIST — self-reported preparation, not entry clearance', ...currentPlan.checklist.map(task => `[${checkedTasks.has(task.id) ? 'x' : ' '}] ${task.title}\n    ${task.detail}`), '', currentPlan.message, currentPlan.scope, '', 'Official guidance: https://www.gov.uk/foreign-travel-advice', 'Recheck official requirements for your passport and dates before departure.'];
  lines.push('', 'DESTINATION AND TRANSIT AUTHORITIES', ...(currentPlan.authority_links || []).map(source => `${source.role}: ${source.title}\n${source.url}`));
  const reference = currentPlan.entry_reference;
  if (reference) lines.push('', 'PASSPORT-BASED REFERENCE', reference.category_label || 'Category withheld — use official links', reference.reason, `Publisher check: ${reference.publisher_checked_at || 'Unavailable'}; snapshot imported: ${reference.imported_at || 'Unavailable'}`, `Citation scope: ${reference.evidence_level || 'Unavailable'}`, ...reference.limitations, ...(reference.links || []).map(source => `${source.title}\n${source.url}`), reference.attribution || '', reference.license_url || '', 'This is not an entry eligibility or boarding decision.');
  const url = URL.createObjectURL(new Blob([lines.join('\n')], {type:'text/plain;charset=utf-8'})); const link = document.createElement('a'); link.href = url; link.download = 'restrictapp-preparation-plan.txt'; link.click(); setTimeout(() => URL.revokeObjectURL(url),1000);
};
init();

const noticeKey = 'restrictapp_cookie_notice_v1';
try { $('cookie-notice').hidden = sessionStorage.getItem(noticeKey) === 'closed'; } catch { $('cookie-notice').hidden = false; }
$('close-cookie').onclick = () => { $('cookie-notice').hidden = true; try { sessionStorage.setItem(noticeKey, 'closed'); } catch {} };
$('cookie-settings').onclick = () => { $('cookie-notice').hidden = false; $('close-cookie').focus(); };
$('privacy-account').onclick = () => { if (!user) { openAuth(); toast('Sign in to export or delete your account data.'); return; } $('data-error').textContent = ''; $('delete-account-form').reset(); $('data-dialog').showModal(); };
$('close-data').onclick = () => $('data-dialog').close();
$('export-account').onclick = async () => {
  try { const data = await api('/api/account/export'); const url = URL.createObjectURL(new Blob([JSON.stringify(data,null,2)], {type:'application/json'})); const link = document.createElement('a'); link.href = url; link.download = 'restrictapp-account.json'; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000); }
  catch (error) { $('data-error').textContent = error.message; }
};
$('delete-account-form').onsubmit = async event => {
  event.preventDefault(); const button = event.submitter; button.disabled = true; $('data-error').textContent = '';
  try { await api('/api/account', {method:'DELETE',body:JSON.stringify({email:user.email,password:$('delete-password').value})}); location.reload(); }
  catch (error) { $('data-error').textContent = error.message; button.disabled = false; }
};

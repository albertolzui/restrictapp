// Exercise the service-worker privacy boundary without a browser or user data.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const handlers = {}, deleted = [], stored = [];
let offline = false;
const fallback = {kind:'public-reconnect'};
const context = {
  URL,
  self: {location:{origin:'https://restrictapp.example'},clients:{claim:async()=>{}},addEventListener:(name,handler)=>handlers[name]=handler},
  caches: {
    open: async()=>({addAll:async urls=>stored.push(...urls),match:async()=>fallback}),
    keys:async()=>['restrictapp-offline-v0','unrelated-app-cache','restrictapp-offline-v2'],
    delete:async key=>deleted.push(key)
  },
  fetch:async()=>{if(offline) throw Error('offline');return {kind:'network'};}
};
vm.runInNewContext(fs.readFileSync('api/static/app/sw.js','utf8'),context);
async function lifecycle(name) {let work;handlers[name]({waitUntil:p=>work=p});await work;}
function request(path,mode='cors',method='GET') {
  let response;
  handlers.fetch({request:{url:new URL(path,'https://restrictapp.example').href,mode,method},respondWith:p=>response=p});
  return response;
}
(async()=>{
  await lifecycle('install');
  assert.deepEqual(stored,['/static/app/offline.html','/static/images/restrictapp-mark.svg','/static/app/locale-data.js','/static/app/i18n.js']);
  await lifecycle('activate');
  assert.deepEqual(deleted,['restrictapp-offline-v0']);
  for(const path of ['/api/me','/api/trips','/api/account/export','/api/guidance/Japan','/api/plan']) {
    assert.equal(request(path),undefined);
    assert.equal(request(path,'navigate'),undefined);
    assert.equal(request(path,'cors','POST'),undefined);
  }
  assert.equal(request('https://external.example/'),undefined);
  assert.equal((await request('/','navigate')).kind,'network');
  offline=true;
  assert.equal(await request('/','navigate'),fallback);
  assert.equal(await request('/static/images/restrictapp-mark.svg'),fallback);
  assert.equal(request('/static/app/app.js'),undefined);
  assert.deepEqual(stored,['/static/app/offline.html','/static/images/restrictapp-mark.svg','/static/app/locale-data.js','/static/app/i18n.js']);
  console.log('Service worker tests passed: APIs bypassed; only public reconnect resources cached.');
})().catch(error=>{console.error(error);process.exitCode=1;});

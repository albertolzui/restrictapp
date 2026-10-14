const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
function setup(userAgent, platform='', maxTouchPoints=0, standalone=false) {
  const elements = {}, handlers = {}, buttons = [{},{}];
  for (const id of ['install-dialog','install-confirm','install-status','install-ios','install-android','install-desktop','install-title','install-description','close-install']) elements[id] = {hidden:false};
  elements['install-dialog'].showModal = function () { this.open=true; };
  elements['install-dialog'].close = function () { this.open=false; };
  vm.runInNewContext(fs.readFileSync('api/static/app/install.js','utf8'),{
    document:{querySelectorAll:()=>buttons,getElementById:id=>elements[id]},
    navigator:{userAgent,platform,maxTouchPoints},
    window:{matchMedia:()=>({matches:standalone,addEventListener:()=>{}}),addEventListener:(name,handler)=>handlers[name]=handler}
  });
  return {elements,handlers,buttons};
}
(async()=>{
  const android=setup('Android Chrome');
  let prompts=0;
  android.handlers.beforeinstallprompt({preventDefault(){},prompt:async()=>{prompts++;},userChoice:Promise.resolve({outcome:'accepted'})});
  const pending=android.buttons[0].onclick();
  assert.equal(prompts,1,'Native prompt must start in the initial button click');
  assert.equal(android.elements['install-dialog'].open,undefined,'No extra confirmation dialog first');
  await android.buttons[1].onclick();
  assert.equal(prompts,1,'Ignore double taps while the prompt is active');
  await pending;
  android.handlers.appinstalled();
  assert.ok(android.buttons.every(button=>button.hidden));
  const fallback=setup('Android Chrome');
  await fallback.buttons[0].onclick();
  assert.ok(fallback.elements['install-dialog'].open);
  assert.ok(fallback.elements['install-ios'].hidden);
  assert.equal(fallback.elements['install-android'].hidden,false);
  assert.ok(fallback.elements['install-desktop'].hidden);
  for (const browser of ['Windows Chrome','Windows Edg','Macintosh Safari','Linux Firefox']) {
    const desktop = setup(browser);
    await desktop.buttons[0].onclick();
    assert.ok(desktop.elements['install-dialog'].open);
    assert.equal(desktop.elements['install-desktop'].hidden,false);
    assert.ok(desktop.elements['install-ios'].hidden);
    assert.ok(desktop.elements['install-android'].hidden);
    assert.match(desktop.elements['install-description'].textContent,/computer/);
  }
  for (const device of [setup('iPhone Safari'),setup('Macintosh Safari','MacIntel',5)]) {
    device.handlers.beforeinstallprompt({preventDefault(){},prompt:()=>assert.fail('iOS must show Safari steps')});
    await device.buttons[0].onclick();
    assert.ok(device.elements['install-dialog'].open);
    assert.equal(device.elements['install-ios'].hidden,false);
    assert.ok(device.elements['install-android'].hidden);
    assert.ok(device.elements['install-desktop'].hidden);
  }
  const failed=setup('Android Chrome');
  failed.handlers.beforeinstallprompt({preventDefault(){},prompt:async()=>{throw Error('unsupported');}});
  await failed.buttons[0].onclick();
  assert.ok(failed.elements['install-dialog'].open);
  assert.ok(failed.buttons.every(button=>!button.disabled));
  assert.ok(setup('Android Chrome','',0,true).buttons.every(button=>button.hidden));
  console.log('Install flow tests passed: direct native prompt, double-tap protection, Android fallback, iPhone/iPad instructions, and installed state.');
})().catch(error=>{console.error(error);process.exitCode=1;});

'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const root = path.join(__dirname,'..');
const context = {Uint8Array,DataView,Int32Array,Error,Number,fetch:async()=>{throw Error('unexpected network');},document:{getElementById:()=>null}};
context.window=context;
context.download_fw=async()=>new Uint8Array([1,2,3]);
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(root,'web-ui/js/bh-sha256.js'),'utf8'),context);
for (const size of [0,1,3,55,56,63,64,65,1024,1000000]) {
  const bytes=Buffer.alloc(size);for(let i=0;i<size;i++)bytes[i]=i%251;
  assert.equal(context.bhSHA256(new Uint8Array(bytes)),crypto.createHash('sha256').update(bytes).digest('hex'));
}
vm.runInContext(fs.readFileSync(path.join(root,'web-ui/js/bh-update.js'),'utf8'),context);
const updater=context.BHUpdater;
assert.equal(updater.compare('0.5.10','0.5.9'),1);
assert.equal(updater.compare('0.5.0','0.5.0'),0);
assert.throws(()=>updater.compare('0.5','0.5.0'));
const config=JSON.parse(fs.readFileSync(path.join(root,'web-ui/js/bh-update-config.json'),'utf8'));
const manifest=JSON.parse(fs.readFileSync(path.join(root,'ota/5234/version.json'),'utf8'));
assert.equal(updater.validate(manifest,config),manifest);
assert.throws(()=>updater.validate({...manifest,platform:'other'},config));
assert.throws(()=>updater.validate({...manifest,enabled:true,url:'http://untrusted/update.img',sha256:'0'.repeat(64),size:6000000},config));
const valid={...manifest,enabled:true,url:'https://raw.githubusercontent.com/kamohy/smartbox-carplay/main/ota/5234/firmware-0.5.1.img',sha256:'0'.repeat(64),size:6000000};
assert.equal(updater.validate(valid,config),valid);
(async()=>{
  await assert.rejects(context.download_fw(valid.url),/Kein freigegebenes/);
  let updated=false;context.update_fw=()=>{updated=true;};context.onUpdate();assert.equal(updated,false);
  // Exercise the real download guard after an enabled manifest was fetched.
  context.fetch=async(url)=>({ok:true,json:async()=>url.startsWith('/')?config:{...valid,version:'0.5.1'}});
  context.showNewVer=()=>{};await context.queryNewVer();
  await assert.rejects(context.download_fw(valid.url),/Firmwareprüfung/);
  await assert.rejects(context.download_fw('https://example.com/wrong.img'),/Kein freigegebenes/);
  console.log('PASS: SHA-256 matches Node crypto; numeric versions, channel guards, disabled updates and corrupt downloads verified');
})().catch(error=>{console.error(error);process.exitCode=1;});

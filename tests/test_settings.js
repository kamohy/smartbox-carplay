'use strict';
const assert=require('node:assert/strict');const fs=require('node:fs');const vm=require('node:vm');const path=require('node:path');
const context={};vm.createContext(context);vm.runInContext(fs.readFileSync(path.join(__dirname,'../web-ui/js/bh-settings.js'),'utf8'),context);
const s=context.BHSettings;
assert.equal(s.ledValue(true),0);assert.equal(s.ledValue(false),1);
assert.equal(s.delayLabels[0],'Normal starten');assert.match(s.delayLabels[2],/20 Sekunden/);
assert.match(s.delayLabels[1],/ungeklärt/);
assert.equal(s.audioLabels.length,4);assert.match(s.audioLabels[0],/Standardpuffer/);
console.log('PASS: documented LED mapping, delay choices and honest audio profile labels');

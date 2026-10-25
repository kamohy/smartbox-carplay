/* Minimal maintenance step: filesystem capacity, local errors, own log deletion. */
(function(){
  'use strict';
  var panel=document.createElement('section');panel.className='cells bh-diagnostics';
  panel.innerHTML='<h2 class="title">Speicher und Fehlerprotokoll</h2><p class="bh-diag-note">Wartungsstand 0.8.3 · Messwerte direkt vom Adapter</p><button type="button" id="bh_space_refresh">Speicher auslesen</button> <button type="button" id="bh_error_refresh">Fehlerprotokoll lesen</button> <button type="button" id="bh_logs_clear">Gespeicherte Logs löschen</button><pre id="bh_space_output" style="white-space:pre-wrap">Noch nicht gelesen.</pre><p class="bh-diag-note" id="bh_maintenance_result"></p><details class="bh-raw"><summary>Fehlerprotokoll anzeigen</summary><pre id="bh_error_output" style="white-space:pre-wrap">Noch nicht gelesen.</pre></details><p class="bh-diag-note">Fehlerauszug aus den vorhandenen RAM-Puffern und verfügbaren Updateprotokollen. Gespeicherte Systemlogs enthalten ebenfalls Fehler. Nach dem Löschen zeichnet der begrenzte Logring weiter auf.</p>';
  var anchor=document.getElementById('bh_diag_title');if(!anchor)return;
  anchor.closest('section').insertAdjacentElement('afterend',panel);
  function el(id){return document.getElementById(id);}
  var localErrors=[];
  function record(message){localErrors.push(new Date().toISOString()+' '+String(message).slice(0,500));localErrors=localErrors.slice(-40);el('bh_maintenance_result').textContent=localErrors[localErrors.length-1];}
  window.addEventListener('error',function(e){record(e.message||'Unbekannter Browserfehler');});
  window.addEventListener('unhandledrejection',function(e){record(e.reason&&e.reason.message||e.reason||'Unbehandelte Anfrage');});
  async function request(id,method){var r=await fetch('/cgi-bin/bh-diagnostics.cgi?id='+id,{method:method||'GET',cache:'no-store'});if(!r.ok)throw Error(id+': HTTP '+r.status);return r;}
  function kib(v){return typeof v==='number'?(v/1024).toFixed(2)+' MiB ('+v+' KiB)':'unbekannt';}
  async function space(){try{var j=await (await request('space')).json();el('bh_space_output').textContent='RAM verfügbar: '+kib(j.memory_available_kib)+'\n'+j.filesystems.map(function(f){return f.path+': '+kib(f.available_kib)+' frei / '+kib(f.total_kib)+' gesamt'+(f.writable===false?' · nur lesbar':f.writable===true?' · beschreibbar':'');}).join('\n')+'\nNur lesbare Systempartitionen dürfen 0 freien Platz melden. Zum Entpacken ist der temporäre Bereich /tmp entscheidend.';}catch(e){record(e.message);}}
  el('bh_space_refresh').onclick=space;
  el('bh_error_refresh').onclick=async function(){try{el('bh_error_output').textContent=await (await request('errors')).text()+'\n=== Browserfehler dieser Seite ===\n'+(localErrors.join('\n')||'Keine erfasst.');el('bh_error_output').parentElement.open=true;}catch(e){record(e.message);}};
  el('bh_logs_clear').onclick=async function(){if(!confirm('Alle gespeicherten Diagnose-Logs auf diesem Adapter löschen? Vorher lokal sichern. Neue Aufzeichnungen laufen anschließend weiter.'))return;var button=this;button.disabled=true;try{await request('clear','POST');el('bh_maintenance_result').textContent='Löschung angefordert. Nach wenigen Sekunden Speicher erneut auslesen.';}catch(e){record(e.message);}finally{button.disabled=false;}};
  space();
})();

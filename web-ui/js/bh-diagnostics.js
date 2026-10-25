/* Device diagnostics: automatic live display and bounded on-device log storage. */
(function(root){
  'use strict';
  function cpuPercent(previous,current){
    if(!previous || !current || !previous.cpu || !current.cpu) return null;
    var count=current.cpu.count;
    if(!Number.isInteger(count)||count<1||count!==previous.cpu.count) return null;
    if(!Number.isFinite(current.uptime_seconds)||!Number.isFinite(previous.uptime_seconds)||
       !Number.isFinite(current.idle_seconds)||!Number.isFinite(previous.idle_seconds)) return null;
    var elapsed=(current.uptime_seconds-previous.uptime_seconds)*count;
    var idle=current.idle_seconds-previous.idle_seconds;
    if(elapsed<=0||idle<0||idle>elapsed+0.02*count) return null;
    return Math.max(0,Math.min(100,100*(elapsed-idle)/elapsed));
  }
  function parseAudio(text){
    var result={phone_output:null,phone_request:null,microphone_conversion:null,buffer_warning_lines:0};
    text.split(/\r?\n/).forEach(function(line){
      var m=line.match(/phone call rate\s*=\s*(\d+)\s*,\s*sz\s*=\s*(\d+)/i);
      if(m) result.phone_output={rate_hz:Number(m[1]),bits:Number(m[2])};
      m=line.match(/AudioPlayerCreate sampleRate:\s*(\d+)\s*,\s*sampleSize:\s*(\d+)\s*,\s*channels\s*(\d+)\s*,\s*audioType\s*:\s*(\d+)\s*,\s*hasInput\s*(\d+)/i);
      if(m && Number(m[4])===8) result.phone_request={rate_hz:Number(m[1]),bits:Number(m[2]),channels:Number(m[3]),has_input:Number(m[5])};
      m=line.match(/mic times\s*=\s*\d+\s*,\s*rate\s*=\s*(\d+)kHz\s*->\s*(\d+)kHz/i);
      if(m){var from=Number(m[1]),to=Number(m[2]);result.microphone_conversion={from_khz:from>=1000?from/1000:from,to_khz:to>=1000?to/1000:to};}
      if(/\b(?:underrun|overrun|xrun)\b/i.test(line)) result.buffer_warning_lines++;
    });
    return result;
  }
  root.BHDiagnostics={cpuPercent:cpuPercent,parseAudio:parseAudio};
  if(!root.document) return;
  var state={previous:null,recording:false,timer:null,samples:[],host:null,busy:false,audio:null,polls:0};
  function el(id){return document.getElementById(id);}
  function put(id,text){var element=el(id);if(element) element.textContent=text;}
  function uptime(seconds){
    if(!Number.isFinite(seconds)) return 'Unbekannt';
    var n=Math.floor(seconds);return Math.floor(n/3600)+'h '+Math.floor(n%3600/60)+'m '+n%60+'s';
  }
  function save(data,type,name){
    var url=URL.createObjectURL(new Blob([data],{type:type}));var a=document.createElement('a');
    a.href=url;a.download=name;document.body.appendChild(a);a.click();a.remove();
    setTimeout(function(){URL.revokeObjectURL(url);},1000);
  }
  async function get(path,json){
    var response=await fetch(path,{cache:'no-store'});
    if(!response.ok) throw Error('HTTP '+response.status);
    return json?response.json():response.text();
  }
  async function host(){
    var j=await get('/cgi-bin/index.cgi?id=host',true);
    state.host={base_appver:j.sys&&j.sys.appver,audio_mode:j.aud,microphone_mode:j.mic,wifi_channel:j.sig,connection_mode:j.conn};
    var mode=j.aud===0?'Standardpuffer':j.aud==null?'Unbekannt':'Puffer aktiv · Profil '+j.aud;
    put('bh_diag_mode',mode);
    put('bh_diag_mode_note',j.aud===0?'Telefon-Puffersonderpfad im untersuchten Code aus.':
      j.aud>=1&&j.aud<=3?'Telefon-Puffersonderpfad aktiv. Weitere Unterschiede zwischen 1–3 sind noch nicht vollständig belegt.':'Keine belegte Moduszuordnung.');
  }
  function stop(){
    state.recording=false;
    put('bh_diag_record','Aufzeichnung starten');
    put('bh_diag_recording',state.samples.length+' Messpunkte im Browser gespeichert');
  }
  function pauseLive(){if(state.timer)clearInterval(state.timer);state.timer=null;}
  function startLive(){if(!state.timer&&!document.hidden&&el('bh_diag_refresh'))state.timer=setInterval(refresh,2000);}
  async function storage(){
    try{
      var j=await get('/cgi-bin/bh-diagnostics.cgi?id=storage',true);
      var labels={cleared:'Gespeicherte Logs gelöscht. Neue Aufzeichnung läuft weiter.',saved:'Automatische Speicherung aktiv',collecting:'Protokoll wird gespeichert',ready:'Speicher bereit',initializing:'Aufzeichnung startet',no_space:'Zu wenig freier Speicher – alte Logs bleiben erhalten',mount_unavailable:'Keine beschreibbare Datenpartition',storage_probe_failed:'Speicherprüfung fehlgeschlagen',not_running:'Aufzeichnung läuft nicht',write_failed:'Speichern fehlgeschlagen',snapshot_too_large:'Protokoll überschreitet Speicherlimit'};
      put('bh_store_status',labels[j.state]||(j.running?'Aufzeichnung aktiv':'Aufzeichnung nicht verfügbar'));
      put('bh_store_space',j.supported?j.available_kib+' / '+j.total_kib+' KiB frei':'Unbekannt');
      var list=el('bh_store_files'),select=el('bh_diag_source'),selected=select?select.value:'';
      if(list)list.replaceChildren();
      if(select){select.replaceChildren();var live=document.createElement('option');live.value='';live.textContent='Aktueller RAM-Log';select.appendChild(live);}
      var files=Array.isArray(j.files)?j.files.slice().sort(function(a,b){return (b.boot||0)-(a.boot||0)||(b.saved_uptime||0)-(a.saved_uptime||0);}):[];
      files.forEach(function(file){
        if(!/^[012][ab]$/.test(file.id))return;
        var name='Start '+(file.boot==null?'?':file.boot)+' · '+file.id+' · '+Math.ceil(file.bytes/1024)+' KiB';
        if(list){var a=document.createElement('a');a.className='bh-log-link';a.href='/cgi-bin/bh-diagnostics.cgi?id=stored'+file.id;a.download='smartbox-log-'+file.id+'.gz';a.textContent=name;list.appendChild(a);}
        if(select){var option=document.createElement('option');option.value=file.id;option.textContent=name;select.appendChild(option);}
      });
      if(select&&Array.from(select.options).some(function(o){return o.value===selected;}))select.value=selected;
      if(list&&!files.length)list.textContent='Noch kein gespeichertes Protokoll.';
    }catch(error){put('bh_store_status','Speicherstatus nicht erreichbar: '+error.message);}
  }
  async function refresh(){
    if(state.busy) return;state.busy=true;
    try{
      var j=await get('/cgi-bin/bh-diagnostics.cgi?id=status',true);
      if(j.schema!==1||!j.memory_kib||!j.cpu||!j.network) throw Error('Unbekannte Diagnoseantwort');
      var cpu=cpuPercent(state.previous,j);state.previous=j;
      put('bh_diag_cpu',cpu===null?'—':cpu.toFixed(1)+' %');
      var total=j.memory_kib.total,available=j.memory_kib.available;
      put('bh_diag_ram',Number.isFinite(total)&&Number.isFinite(available)?((total-available)/1024).toFixed(1)+' / '+(total/1024).toFixed(1)+' MiB':'Unbekannt');
      put('bh_diag_uptime',uptime(j.uptime_seconds));
      put('bh_diag_usb',j.usb_state==='configured'?'Konfiguriert':j.usb_state==='not attached'?'Nicht verbunden':j.usb_state||'Unbekannt');
      var networks=Array.isArray(j.networks)?j.networks:[j.network];
      put('bh_diag_net',networks.map(function(n){return n.interface;}).join(' / ')||'Unbekannt');
      put('bh_diag_drops',networks.map(function(n){return n.interface+': '+(n.rx_dropped==null?'?':n.rx_dropped)+' / '+(n.tx_dropped==null?'?':n.tx_dropped);}).join(' · '));
      put('bh_diag_status','Letzte Abfrage: '+new Date().toLocaleTimeString()+' · CPU über Messintervall');
      state.polls++;if(state.polls%5===0)storage();
      if(state.recording){
        state.samples.push({browser_time:new Date().toISOString(),cpu_percent:cpu,device:j});
        put('bh_diag_recording','Aufzeichnung läuft · '+state.samples.length+' Messpunkte');
        if(state.samples.length>=900) stop();
      }
    }catch(error){put('bh_diag_status','Diagnose nicht erreichbar: '+error.message);}
    finally{state.busy=false;}
  }
  async function analyze(){
    var button=el('bh_diag_audio');if(button)button.disabled=true;
    put('bh_diag_audio_summary','Audio-Log wird gelesen …');
    try{
      var source=el('bh_diag_source')?el('bh_diag_source').value:'';
      var text=await get('/cgi-bin/bh-diagnostics.cgi?id=audio'+(source?'&source='+encodeURIComponent(source):''),false);
      var parsed=parseAudio(text);state.audio={captured_at:new Date().toISOString(),source:source||'live',analysis:parsed,raw:text};
      put('bh_diag_phone',parsed.phone_output?parsed.phone_output.rate_hz+' Hz / '+parsed.phone_output.bits+' Bit':'Noch keine Telefon-Ausgaberate im Log');
      var request=parsed.phone_request;
      put('bh_diag_phone_request',request?request.rate_hz+' Hz / '+request.bits+' Bit / '+request.channels+' Kanal/Kanäle':'Keine Telefon-Audioanfrage im Log');
      var mic=parsed.microphone_conversion;
      put('bh_diag_mic',mic?mic.from_khz+' → '+mic.to_khz+' kHz':'Keine Mikrofon-Umwandlung im Log belegt');
      put('bh_diag_warnings',String(parsed.buffer_warning_lines));
      put('bh_diag_audio_raw',text);
      put('bh_diag_audio_summary','Auswertung der letzten 200 passenden Logzeilen. Keine Messung der hörbaren Klangqualität.');
    }catch(error){put('bh_diag_audio_summary','Audio-Log nicht erreichbar: '+error.message);}
    finally{if(button)button.disabled=false;}
  }
  function initialize(){
    if(!el('bh_diag_refresh')) return;
    pauseLive();stop();state.previous=null;
    el('bh_diag_refresh').onclick=function(){refresh().then(function(){setTimeout(refresh,1000);});host().catch(function(){});};
    el('bh_diag_record').onclick=function(){
      if(state.recording){stop();return;}
      state.samples=[];state.recording=true;put('bh_diag_record','Aufzeichnung stoppen');
      host().catch(function(){});refresh();startLive();
    };
    el('bh_diag_export').onclick=function(){
      save(JSON.stringify({schema:1,ui_version:'0.9.0',cpu_source:'uptime-idle',host:state.host,samples:state.samples,audio:state.audio},null,2),'application/json','smartbox-session.json');
    };
    el('bh_diag_audio').onclick=analyze;
    el('bh_store_save').onclick=async function(){
      try{var response=await fetch('/cgi-bin/bh-diagnostics.cgi?id=save',{method:'POST'});if(!response.ok)throw Error('HTTP '+response.status);put('bh_store_status','Speichern angefordert …');setTimeout(storage,6000);}
      catch(error){put('bh_store_status','Speichern nicht möglich: '+error.message);}
    };
    el('bh_store_clear').onclick=async function(){
      if(!root.confirm('Gespeicherte Logs auf dem Adapter löschen? Vorher wichtige Dateien herunterladen. Neue Logs werden anschließend weiter aufgezeichnet.'))return;
      try{var r=await fetch('/cgi-bin/bh-diagnostics.cgi?id=clear',{method:'POST'});if(!r.ok)throw Error('HTTP '+r.status);put('bh_store_status','Löschen angefordert …');setTimeout(storage,6000);}catch(e){put('bh_store_status','Löschen nicht möglich: '+e.message);}
    };
    el('bh_diag_refresh').onclick();
    storage();startLive();
  }
  var originalGo=root.go_tpl;
  root.go_tpl=function(name){pauseLive();stop();originalGo(name);if(name==='tpl_home')initialize();};
  root.addEventListener('pagehide',function(){pauseLive();stop();});
  document.addEventListener('visibilitychange',function(){if(document.hidden)pauseLive();else startLive();});
})(typeof window==='undefined'?globalThis:window);

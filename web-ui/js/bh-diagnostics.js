/* Device diagnostics: fixed read-only CGI, local browser recording and export. */
(function(root){
  'use strict';
  function cpuPercent(previous,current){
    if(!previous || !current || !previous.cpu || !current.cpu) return null;
    var total=current.cpu.total_jiffies-previous.cpu.total_jiffies;
    var idle=current.cpu.idle_jiffies-previous.cpu.idle_jiffies;
    if(!Number.isFinite(total)||!Number.isFinite(idle)||total<=0||idle<0||idle>total) return null;
    return Math.max(0,Math.min(100,100*(total-idle)/total));
  }
  function parseAudio(text){
    var result={phone_output:null,phone_request:null,microphone_conversion:null,buffer_warning_lines:0};
    text.split(/\r?\n/).forEach(function(line){
      var m=line.match(/phone call rate\s*=\s*(\d+)\s*,\s*sz\s*=\s*(\d+)/i);
      if(m) result.phone_output={rate_hz:Number(m[1]),bits:Number(m[2])};
      m=line.match(/AudioPlayerCreate sampleRate:\s*(\d+)\s*,\s*sampleSize:\s*(\d+)\s*,\s*channels\s*(\d+)\s*,\s*audioType\s*:\s*(\d+)\s*,\s*hasInput\s*(\d+)/i);
      if(m && Number(m[4])===8) result.phone_request={rate_hz:Number(m[1]),bits:Number(m[2]),channels:Number(m[3]),has_input:Number(m[5])};
      m=line.match(/mic times\s*=\s*\d+\s*,\s*rate\s*=\s*(\d+)kHz\s*->\s*(\d+)kHz/i);
      if(m) result.microphone_conversion={from_khz:Number(m[1]),to_khz:Number(m[2])};
      if(/\b(?:underrun|overrun|xrun)\b/i.test(line)) result.buffer_warning_lines++;
    });
    return result;
  }
  root.BHDiagnostics={cpuPercent:cpuPercent,parseAudio:parseAudio};
  if(!root.document) return;
  var state={previous:null,recording:false,timer:null,samples:[],host:null,busy:false,audio:null};
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
    var mode=j.aud===0?'Default (0)':j.aud==null?'Unbekannt':'Mode '+j.aud;
    put('bh_diag_mode',mode);
    put('bh_diag_mode_note',j.aud===0?'Telefon-Puffersonderpfad im untersuchten Code aus.':
      j.aud>=1&&j.aud<=3?'Telefon-Puffersonderpfad aktiv. Weitere Unterschiede zwischen 1–3 sind noch nicht vollständig belegt.':'Keine belegte Moduszuordnung.');
  }
  function stop(){
    state.recording=false;if(state.timer) clearInterval(state.timer);state.timer=null;
    put('bh_diag_record','Aufzeichnung starten');
    put('bh_diag_recording',state.samples.length+' Messpunkte im Browser gespeichert');
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
      put('bh_diag_net',j.network.interface||'Unbekannt');
      put('bh_diag_drops',j.network.rx_dropped==null||j.network.tx_dropped==null?'Unbekannt':j.network.rx_dropped+' / '+j.network.tx_dropped);
      put('bh_diag_status','Letzte Abfrage: '+new Date().toLocaleTimeString()+' · CPU über Messintervall');
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
      var text=await get('/cgi-bin/bh-diagnostics.cgi?id=audio',false);
      var parsed=parseAudio(text);state.audio={captured_at:new Date().toISOString(),analysis:parsed,raw:text};
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
    stop();state.previous=null;
    el('bh_diag_refresh').onclick=function(){refresh().then(function(){setTimeout(refresh,1000);});host().catch(function(){});};
    el('bh_diag_record').onclick=function(){
      if(state.recording){stop();return;}
      state.samples=[];state.recording=true;put('bh_diag_record','Aufzeichnung stoppen');
      host().catch(function(){});refresh();state.timer=setInterval(refresh,2000);
    };
    el('bh_diag_export').onclick=function(){
      save(JSON.stringify({schema:1,ui_version:'0.6.0',host:state.host,samples:state.samples,audio:state.audio},null,2),'application/json','smartbox-session.json');
    };
    el('bh_diag_audio').onclick=analyze;
    el('bh_diag_refresh').onclick();
  }
  var originalGo=root.go_tpl;
  root.go_tpl=function(name){stop();originalGo(name);if(name==='tpl_home')initialize();};
  root.addEventListener('pagehide',stop);
})(typeof window==='undefined'?globalThis:window);

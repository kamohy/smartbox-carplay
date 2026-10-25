/* Bad-Hippo update channel. Vendor audio/configuration handlers remain intact. */
(function () {
  'use strict';
  var config, manifest, pending, statusTimer=null;
  var originalDownload = window.download_fw;
  var prefix = 'https://raw.githubusercontent.com/kamohy/smartbox-carplay/main/ota/5234/';
  function message(text) {
    var status=document.getElementById('txt11');
    if (status) status.textContent=text;
    var spinner=document.getElementById('fw_sta');
    if (spinner) spinner.style.display='none';
  }
  function compare(a,b) {
    if (!/^\d+\.\d+\.\d+$/.test(a) || !/^\d+\.\d+\.\d+$/.test(b)) throw Error('Ungültige Projektversion');
    a=a.split('.').map(Number);b=b.split('.').map(Number);
    for (var i=0;i<3;i++) if(a[i]!==b[i]) return a[i]>b[i]?1:-1;
    return 0;
  }
  function validate(j,c) {
    if (j.schema!==1 || j.platform!==c.platform || j.base_appver!==c.base_appver) throw Error('Firmware passt nicht zur Plattform/Basis');
    compare(j.version,c.ui_version);
    if (typeof j.enabled!=='boolean') throw Error('Freigabestatus fehlt');
    if (j.enabled && (!/^https:\/\/raw\.githubusercontent\.com\/kamohy\/smartbox-carplay\/main\/ota\/5234\/firmware-[\d.]+\.img$/.test(j.url) || !/^[a-f0-9]{64}$/.test(j.sha256) || !Number.isInteger(j.size) || j.size<1000000 || j.size>10000000)) throw Error('Ungültiges Updatepaket');
    return j;
  }
  function escaped(text) { return String(text).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c];}); }
  function statusText(code){
    if(code===1)return 'Gerätestatus 1: Vorbereitung. Der Adapter meldet keinen messbaren Prozentfortschritt.';
    if(code===2)return 'Gerätestatus 2: Firmware wird verarbeitet/geschrieben. Eingeschaltet lassen.';
    if(code===3)return 'Gerät meldet Updateabschluss. Neustart und Kontrolle der installierten Version stehen noch aus.';
    if(code===0)return 'Gerät meldet kein aktives Update. Eine neue Installation ist damit noch nicht bestätigt.';
    return Number.isInteger(code)&&code>3?'Gerät meldet Updatefehler '+code+'.':'Unbekannter Updatezustand.';
  }
  async function readState(){var r=await fetch('/cgi-bin/index.cgi?id=host',{cache:'no-store'});if(!r.ok)throw Error('Gerätestatus HTTP '+r.status);var j=await r.json();if(!Number.isInteger(j.update))throw Error('Gerätestatus fehlt');return j;}
  function showState(j){
    // Hide the vendor's elapsed-time percentage: it is not flash progress.
    var bar=document.getElementById('fw_prog_bd');if(bar)bar.style.display='none';
    var button=document.getElementById('txt12');if(button){button.href='javascript:;';button.setAttribute('aria-disabled','true');}
    message(statusText(j.update));
  }
  function observe(j){
    if(statusTimer!==null){clearTimeout(statusTimer);statusTimer=null;}
    showState(j);
    if(j.update===1||j.update===2)statusTimer=setTimeout(pollState,3000);
  }
  async function pollState(){
    statusTimer=null;
    try{observe(await readState());}
    catch(e){message('Geräteverbindung unterbrochen: '+e.message+'. Updateabschluss noch nicht bestätigt.');statusTimer=setTimeout(pollState,3000);}
  }
  // Called by the existing upload handler; never turn elapsed time into success.
  window.timer_8min=function(){pollState();};
  window.queryNewVer = async function () {
    if (pending) return pending;
    pending=(async function(){
      try {
        var current=await readState();
        if(current.update!==0){observe(current);return;}
        var response=await fetch('/js/bh-update-config.json',{cache:'no-store'});
        if (!response.ok) throw Error('Updatekonfiguration nicht erreichbar');
        config=await response.json();
        if (config.provider!=='github-public' || config.api_url!==prefix+'version.json') throw Error('Unbekannter Updatekanal');
        response=await fetch(config.api_url+'?t='+Date.now(),{cache:'no-store'});
        if (!response.ok) throw Error('Updatearchiv nicht erreichbar (HTTP '+response.status+')');
        manifest=validate(await response.json(),config);
        if (!manifest.enabled) { message('Bad-Hippo '+manifest.version+' · Testpaket noch nicht zur Installation freigegeben'); return; }
        if (compare(manifest.version,config.ui_version)<=0) { message('Bad-Hippo '+config.ui_version+' · aktuell'); return; }
        showNewVer({url:manifest.url,appver:'Bad-Hippo '+manifest.version,msg:escaped(manifest.notes||'')});
      } catch(error) { manifest=null; message('Updateprüfung: '+error.message); }
      finally { pending=null; }
    })();
    return pending;
  };
  window.download_fw = async function(url) {
    if (!manifest || !manifest.enabled || url!==manifest.url) throw Error('Kein freigegebenes Update ausgewählt');
    var bytes=await originalDownload(url);
    if (!(bytes instanceof Uint8Array) || bytes.length!==manifest.size || bhSHA256(bytes)!==manifest.sha256) throw Error('Firmwareprüfung fehlgeschlagen');
    return bytes;
  };
  window.onUpdate=async function(){
    if (manifest && manifest.enabled && config && compare(manifest.version,config.ui_version)>0){
      try{var j=await readState();if(j.update!==0){observe(j);return;}update_fw(manifest.url);}
      catch(e){message('Update nicht gestartet: '+e.message);}
    }
  };
  window.BHUpdater={compare:compare,validate:validate,statusText:statusText};
})();

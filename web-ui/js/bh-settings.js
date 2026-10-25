/* Plain labels describe only behavior established for the pinned 5234 firmware. */
(function(root){
  'use strict';
  var audio=['Standardpuffer','Puffer aktiv · Profil 1','Puffer aktiv · Profil 2','Puffer aktiv · Profil 3'];
  var delays=['Normal starten','Hersteller-Alternative · ungeklärt','Start um 20 Sekunden verzögern'];
  function ledValue(enabled){return enabled?0:1;}
  root.BHSettings={ledValue:ledValue,audioLabels:audio,delayLabels:delays,apply:apply};
  function put(id,text){var e=document.getElementById(id);if(e)e.textContent=text;}
  function note(id,text){var row=document.getElementById(id);if(!row)return;var left=row.querySelector('.weui-cell__bd');if(!left)return;var p=left.querySelector('.bh-setting-note');if(!p){p=document.createElement('p');p.className='bh-setting-note';left.appendChild(p);}p.textContent=text;}
  function label(id,text){var row=document.getElementById(id);if(row){var p=row.querySelector('.weui-cell__bd > p');if(p)p.textContent=text;}}
  async function set(key,value){
    if(!({led:[0,1],aud:[0,1,2,3],delay:[0,1,2],gps:[0,1]})[key].includes(value))throw Error('Unbekannte Einstellung');
    var r=await fetch('/cgi-bin/index.cgi?id=set&'+key+'='+value,{cache:'no-store'});if(!r.ok)throw Error('HTTP '+r.status);var j=await r.json();if(j.code!==0)throw Error('Gerätecode '+j.code);
  }
  function picker(rowId,key,labels,current,target){
    var row=document.getElementById(rowId);if(!row)return;
    row.href='javascript:;';row.onclick=function(){
      weui.picker(labels.map(function(text,i){return {label:text,value:i};}),{defaultValue:[current],onConfirm:function(result){var v=result[0].value;set(key,v).then(function(){current=v;put(target,labels[v]);}).catch(function(e){put(target,'Fehler: '+e.message);});}});
    };
  }
  function apply(j){
    put('txt0','Geräteversion');put('txt1','Hersteller-Firmware');put('txt21','Herstellungsdatum');put('txt2','Verbindung und Start');
    put('txt4','Problem an den Hersteller melden');put('txt5','Fahrzeugmarke');put('txt6','Modell');put('txt7','Baujahr');put('txt8','Problembeschreibung');put('txt9','An Hersteller senden');put('txt10','Software aktualisieren');put('txt13','Änderungen');
    label('div_wif','WLAN-Kanal');note('div_wif','Funkkanal der Verbindung zum iPhone. 36/149/161: 5 GHz; 6: 2,4 GHz. Kanalwechsel ist kein Klangregler.');
    label('div_aud','Telefonpuffer');put('aud',audio[j.aud]||'Unbekannt');
    note('div_aud','Standard: besonderer Telefonpuffer aus. Profile 1–3: an. Weitere Unterschiede sind noch nicht vollständig belegt. Im Teams-Test nutzen Profil 2 und 3 beide 8 kHz zum Radio.');
    picker('div_aud','aud',audio,j.aud,'aud');
    label('div_delay','Verbindungsstart');put('delay',delays[j.delay]||'Unbekannt');
    note('div_delay','Hilft, wenn das Radio nach dem Einschalten noch nicht bereit ist. Die 20-Sekunden-Option ist im USB-Startcode belegt. Die genaue Wirkung der Hersteller-Alternative ist noch ungeklärt. Ändert nicht den Klang.');
    picker('div_delay','delay',delays,j.delay,'delay');
    label('div_gps','GPS-Kompatibilität');put('gps',j.gps===0?'Standard':j.gps===1?'Hersteller-Alternative':'Unbekannt');
    note('div_gps','Herstelleroption zur GPS-Kompatibilität. Ein eigener GPS-Empfänger ist auf diesem Adapter nicht nachgewiesen; die genaue Umschaltwirkung ist noch offen.');
    picker('div_gps','gps',['Standard','Hersteller-Alternative'],j.gps,'gps');
    label('div_rst','Werkseinstellungen');note('div_rst','Setzt die Herstellerkonfiguration zurück. Für einen normalen Neustart nicht verwenden.');
    var toggle=document.getElementById('bh_led_switch');
    if(toggle){toggle.checked=j.led===0;toggle.disabled=!(j.led===0||j.led===1);put('bh_led_state',j.led===0?'Ein':j.led===1?'Aus':'Unbekannt');
      toggle.onchange=async function(){var old=!toggle.checked;toggle.disabled=true;put('bh_led_state','Wird gespeichert …');try{await set('led',ledValue(toggle.checked));put('bh_led_state',toggle.checked?'Ein':'Aus');}catch(e){toggle.checked=old;put('bh_led_state','Speichern fehlgeschlagen: '+e.message);}finally{toggle.disabled=false;}};
    }
    var hardware=document.getElementById('bh_hardware_refresh');if(hardware)hardware.onclick=async function(){hardware.disabled=true;put('bh_hardware_raw','Wird vom Gerät gelesen …');try{var r=await fetch('/cgi-bin/bh-diagnostics.cgi?id=hardware',{cache:'no-store'});if(!r.ok)throw Error('HTTP '+r.status);put('bh_hardware_raw',await r.text());document.querySelector('#bh_hardware_raw').parentElement.open=true;}catch(e){put('bh_hardware_raw','Nicht erreichbar: '+e.message);}finally{hardware.disabled=false;}};
  }
})(typeof window==='undefined'?globalThis:window);

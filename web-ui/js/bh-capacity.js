/* Fixed filesystem reads. Flash capacity, persistent space and RAM stay separate. */
(function(root){
  'use strict';
  function size(kib){return Number.isFinite(kib)?(kib>=1024?(kib/1024).toFixed(2)+' MiB':kib+' KiB'):'unbekannt';}
  function describe(f){
    var names={'/mnt/UDISK':'Dauerhafter Datenspeicher · Logs und Kopplungen','/tmp':'Temporärer Speicher · Updates und Laufzeitdateien','/mnt/customer':'Firmware und Oberfläche','/':'Linux-System'};
    return {name:names[f.path]||f.path,total:size(f.total_kib),free:size(f.available_kib),used:size(f.used_kib),
      readonly:f.writable===false,percent:Number.isFinite(f.total_kib)&&f.total_kib>0&&Number.isFinite(f.used_kib)?Math.max(0,Math.min(100,100*f.used_kib/f.total_kib)):null};
  }
  root.BHCapacity={size:size,describe:describe};
  if(!root.document)return;
  function el(id){return document.getElementById(id);}
  function put(id,value){var node=el(id);if(node)node.textContent=value;}
  async function get(id){var r=await fetch('/cgi-bin/bh-diagnostics.cgi?id='+id,{cache:'no-store'});if(!r.ok)throw Error('HTTP '+r.status);return r;}
  async function refresh(){
    var button=el('bh_capacity_refresh');if(!button)return;button.disabled=true;
    try{
      var j=await (await get('space')).json();if(j.schema!==1||!Array.isArray(j.filesystems))throw Error('Unbekannte Speicherantwort');
      var list=el('bh_capacity_rows');list.replaceChildren();
      j.filesystems.forEach(function(f){
        var d=describe(f),card=document.createElement('div'),title=document.createElement('strong'),text=document.createElement('p');
        card.className='bh-capacity-card';title.textContent=d.name;
        text.textContent=d.readonly?d.total+' gesamt · schreibgeschützt':d.free+' frei / '+d.total+' gesamt · '+d.used+' belegt'+(f.writable===true?'':' · Schreibbarkeit unbekannt');
        card.appendChild(title);card.appendChild(text);
        if(d.percent!==null&&!d.readonly){var meter=document.createElement('meter');meter.min=0;meter.max=100;meter.value=d.percent;meter.setAttribute('aria-label',d.name+': '+d.percent.toFixed(1)+' Prozent belegt');card.appendChild(meter);}
        list.appendChild(card);
      });
      put('bh_capacity_status','RAM verfügbar: '+size(j.memory_available_kib)+' · Stand '+new Date().toLocaleTimeString()+'. /tmp kann denselben RAM nutzen; Kapazitäten nicht addieren. Freie Firmware-Bytes sind kein nutzbarer Logspeicher.');
    }catch(e){put('bh_capacity_status','Speicher nicht auslesbar: '+e.message+'. Die Zahlen oben stammen nur aus belegten Hardwaredaten.');}
    finally{button.disabled=false;}
  }
  function initialize(){
    var button=el('bh_capacity_refresh');if(!button)return;button.onclick=refresh;
    el('bh_errors_refresh').onclick=async function(){this.disabled=true;try{put('bh_errors_raw',await (await get('errors')).text());el('bh_errors_raw').parentElement.open=true;}catch(e){put('bh_errors_raw','Fehlerprotokoll nicht erreichbar: '+e.message);}finally{this.disabled=false;}};
    refresh();
  }
  var original=root.go_tpl;root.go_tpl=function(name){original(name);if(name==='tpl_home')initialize();};
})(typeof window==='undefined'?globalThis:window);

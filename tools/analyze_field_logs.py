#!/usr/bin/env python3
"""Offline analysis of persistent SmartBox snapshots; never contacts a device."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import re
import statistics

PHONE_REQUEST=re.compile(r'AudioPlayerCreate sampleRate:\s*(\d+)\s*,\s*sampleSize:\s*(\d+)\s*,\s*channels\s*(\d+)\s*,\s*audioType\s*:\s*(\d+)\s*,\s*hasInput\s*(\d+)')
USB_START=re.compile(r'AudioPlayerCreate \d+\s*:sampleRate:(\d+),sampleSize:(\d+),Channel:(\d+),audioType:(\d+),hasInput:(\d+)')
MIC=re.compile(r'mic times\s*=\s*\d+,\s*rate\s*=\s*(\d+)kHz\s*->\s*(\d+)kHz')

def analyze(paths: list[Path]) -> dict:
    boots={};sources=[]
    for path in paths:
        packed=path.read_bytes()
        raw=gzip.decompress(packed) if path.suffix=='.gz' else packed
        if len(raw)>2*1024*1024 or not raw.startswith(b'Bad-Hippo persistent system log '):
            raise ValueError('Not a bounded persistent SmartBox snapshot: '+path.name)
        match=re.search(rb'^Boot counter: (\d+)$',raw,re.M)
        if not match:raise ValueError('Missing boot counter')
        boot=int(match[1]);state=boots.setdefault(boot,{'lines':set(),'metrics':{}})
        for line in raw.decode('utf-8','replace').splitlines():
            state['lines'].add(line)
            if line.startswith('{"schema":1,'):
                item=json.loads(line);state['metrics'][item['uptime_seconds']]=item
        sources.append({'file':path.name,'boot':boot,'bytes':len(packed),'sha256':hashlib.sha256(packed).hexdigest(),'gzip_crc_valid':True if path.suffix=='.gz' else None})
    summaries=[]
    for boot,state in sorted(boots.items()):
        requests=[];outputs=[];usb=[];mics=[];modes=set();clocks=[];last_type=None
        warnings=0;metadata=set()
        for line in sorted(state['lines']):
            stamp=re.match(r'^\d\d-\d\d (\d\d:\d\d:\d\d\.\d{3})',line)
            at=stamp[1] if stamp else None
            m=PHONE_REQUEST.search(line)
            if m and int(m[4])==8:
                requests.append({'at':at,'rate_hz':int(m[1]),'bits':int(m[2]),'channels':int(m[3]),'has_input':int(m[5])})
            m=USB_START.search(line)
            if m:
                last_type=int(m[4])
                if last_type==8:usb.append({'at':at,'rate_hz':int(m[1]),'bits':int(m[2]),'channels':int(m[3]),'has_input':int(m[5])})
            m=re.search(r'phone call rate=(\d+), sz=(\d+)',line)
            if m:outputs.append({'at':at,'rate_hz':int(m[1]),'bits':int(m[2])})
            m=MIC.search(line)
            if m:
                # The pinned vendor code prints raw Hz with a literal "kHz" suffix.
                # Confirmed by its 16000-Hz converter setup and live 8000->16000 log.
                mics.append({'at':at,'from_hz':int(m[1]),'to_hz':int(m[2]),'vendor_khz_label_incorrect':True})
            m=re.search(r'playerType=8,audiomode=(\d+)',line)
            if m:modes.add(int(m[1]))
            m=re.search(r'_HUSampleRateCB, samplerate = ([\d.]+)',line)
            if m and last_type==8:clocks.append(float(m[1]))
            if re.search(r'\b(?:underrun|overrun|xrun)\b',line,re.I):warnings+=1
            for label in ('GetHUPluginVer','getAudioFormat support48=','media phone audio rate','huInfo name='):
                if label in line:metadata.add(label)
        samples=sorted(state['metrics'].values(),key=lambda j:j['uptime_seconds']);cpu=[]
        for a,b in zip(samples,samples[1:]):
            count=b.get('cpu',{}).get('count')
            if not count or a.get('cpu',{}).get('count')!=count:continue
            wall=(b['uptime_seconds']-a['uptime_seconds'])*count
            if wall<=0 or not all(isinstance(j.get('idle_seconds'),(float,int)) for j in (a,b)):continue
            idle=b['idle_seconds']-a['idle_seconds']
            if idle<0 or idle>wall+0.02*count:continue
            cpu.append(max(0,min(100,100*(wall-idle)/wall)))
        available=[j['memory_kib']['available'] for j in samples if isinstance(j.get('memory_kib',{}).get('available'),(float,int))]
        network=[j.get('network',{}) for j in samples]
        summaries.append({'boot':boot,'modes_observed':sorted(modes),'phone_request_events':requests,
            'phone_output_events':outputs,'usb_phone_start_events':usb,'microphone_conversions':mics,
            'clock_hz_after_phone_start_min_max':[min(clocks),max(clocks)] if clocks else None,
            'buffer_warning_lines':warnings,'headunit_metadata_labels_present':sorted(metadata),
            'metrics':{'samples':len(samples),'cpu_percent_min_median_max':[round(v,3) for v in (min(cpu),statistics.median(cpu),max(cpu))] if cpu else None,
                'memory_available_kib_min':min(available) if available else None,
                'interfaces_observed':sorted({j.get('interface','') for j in network}),
                'all_traffic_byte_counters_zero':bool(network) and all(j.get('rx_bytes')==0 and j.get('tx_bytes')==0 for j in network)}})
    return {'schema':1,'analyzer_version':'0.7.1','source_files':sources,'boots':summaries,
        'limits':['Overlapping snapshots deduplicated within each boot; audio starts are not call counts.',
                  'Vendor timestamps have no reliable calendar date.',
                  'No PCM recording, wired reference or subjective sound measurement.',
                  'Missing warnings do not prove glitch-free audio or Wi-Fi.']}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',type=Path)
    args=p.parse_args();paths=sorted(args.input.glob('boot-*.gz')) if args.input.is_dir() else [args.input]
    if not paths:p.error('No boot snapshots found')
    report=analyze(paths);text=json.dumps(report,indent=2)+'\n'
    if args.output:
        with args.output.open('x',encoding='utf-8',newline='\n') as f:f.write(text)
    else:print(text,end='')

if __name__=='__main__':main()

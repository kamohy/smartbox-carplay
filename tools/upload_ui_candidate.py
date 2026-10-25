#!/usr/bin/env python3
"""Upload the pinned UI-only candidate once; requires explicit risk opt-in.

This uses the real device updater and may make the adapter unbootable.
It never retries an upload or changes Windows drivers.
"""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
from urllib.request import Request,ProxyHandler,build_opener
import uuid
try:
    from .build_ui_firmware import ROOT,verify_candidate
except ImportError:
    from build_ui_firmware import ROOT,verify_candidate

DEVICE='http://192.168.1.101'
IMAGE_SHA='3b1d45b1ca75b9462bfc53974b5d34c6f28aef9b4f0761c746f1cb0923074581'
PAGE_SHA='d9960273e47c59ee9f594a77c78e6711ae2b41cc4a3b25a7c4511b9774b6bcc8'

def multipart(data: bytes,boundary: str) -> bytes:
    if not boundary.isalnum(): raise ValueError('boundary must be alphanumeric')
    return (f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="blob"\r\n'
            'Content-Type: application/octet-stream\r\n\r\n').encode()+data+f'\r\n--{boundary}--\r\n'.encode()

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--upload',action='store_true',help='actually submit one firmware upload')
    p.add_argument('--allow-unverified-recovery',action='store_true',help='explicitly accept possible device loss without a verified backup/recovery')
    args=p.parse_args()
    if args.upload and not args.allow_unverified_recovery: p.error('upload requires explicit unverified-recovery opt-in')
    image=(ROOT/'ota/5234/firmware-0.5.0.img').read_bytes()
    if hashlib.sha256(image).hexdigest()!=IMAGE_SHA: p.error('candidate hash differs from reviewed image')
    original=(ROOT/'evidence/firmware/26011517.5234.2/update.img').read_bytes()
    verify_candidate(original,image,ROOT/'web-ui')
    opener=build_opener(ProxyHandler({}))
    def read(path):
        with opener.open(DEVICE+path,timeout=8) as r:return r.read()
    try:
        host=json.loads(read('/cgi-bin/index.cgi?id=host'))
        page=read('/index.html')
    except (OSError,ValueError) as e:
        p.error(f'preflight could not read the adapter; no firmware submitted: {e}')
    if host.get('sys',{}).get('appver')!='26011517.5234.2': p.error('unexpected firmware/platform')
    if host.get('update')!=0: p.error('updater is not idle; no upload performed')
    if hashlib.sha256(page).hexdigest()!=PAGE_SHA: p.error('device page differs from pinned stock UI; refusing duplicate/unknown install')
    print('Preflight OK: stable ly5234, updater idle, stock page and complete candidate verified.',flush=True)
    if not args.upload: print('Inspection only. No device writes.');return 0
    folder=ROOT/'evidence/updates'/datetime.now().strftime('%Y-%m-%d-%H%M%S')
    folder.mkdir(parents=True,exist_ok=False)
    (folder/'host.before.json').write_text(json.dumps(host,indent=2),encoding='utf-8')
    (folder/'index.before.html').write_bytes(page)
    receipt={'created_at':datetime.now().astimezone().isoformat(),'image_sha256':IMAGE_SHA,
             'image_size':len(image),'full_backup_verified':False,'recovery_verified':False,
             'user_explicitly_accepted_device_loss':True,'upload_attempted':True,
             'device_installation_verified':False,'status':'sending'}
    target=folder/'upload-receipt.json'
    def save():target.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    save()
    boundary='SmartBox'+uuid.uuid4().hex
    body=multipart(image,boundary)
    request=Request(DEVICE+'/cgi-bin/index.cgi?id=upload',data=body,method='POST',headers={
        'Content-Type':'multipart/form-data; boundary='+boundary,'Content-Length':str(len(body)),
        'Accept-Language':'de-DE','Connection':'close'})
    print(f'Uploading {len(image)} bytes once. Receipt: {target}',flush=True)
    try:
        with opener.open(request,timeout=120) as response:
            raw=response.read();receipt['http_status']=response.status
        (folder/'upload-response.txt').write_bytes(raw)
        receipt['response']=json.loads(raw)
        receipt['status']='accepted' if receipt['response'].get('code')==0 else 'rejected'
        save();print(json.dumps(receipt,indent=2),flush=True)
        return 0 if receipt['status']=='accepted' else 2
    except Exception as e:
        receipt.update(status='delivery-uncertain-do-not-retry',error=str(e));save()
        print(f'Upload result uncertain: {e}. Inspect device state; do not retry automatically.',flush=True)
        return 2

if __name__=='__main__':raise SystemExit(main())

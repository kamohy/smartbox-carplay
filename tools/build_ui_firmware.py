#!/usr/bin/env python3
"""Build and independently verify an OFFLINE UI-only SmartBox 5234 candidate.

No network access, device upload or flashing is implemented by this tool.
"""
from __future__ import annotations
import argparse
from dataclasses import dataclass
import hashlib
import io
import json
from pathlib import Path
import stat
import subprocess
from dissect.squashfs import SquashFS
try:
    from .decrypt_firmware import HEADER, XOR_KEY
except ImportError:
    from decrypt_firmware import HEADER, XOR_KEY

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SHA = '7afff8e6a6387662aa10d84d5f8745e8406b91fb704aa4942f6e416393b10f63'
CUSTOMER_CAPACITY = 0x3A0000
BOOT_CAPACITY = 0x310000
OVERLAY = ('index.html', 'css/bad-hippo-dark.css', 'css/bad-hippo-logo.svg',
           'js/bh-sha256.js', 'js/bh-update.js', 'js/bh-update-config.json')

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def xor(data: bytes) -> bytes:
    return bytes(v ^ XOR_KEY[i & 255] for i,v in enumerate(data))

def unpack_image(image: bytes) -> bytes:
    plain = xor(image)
    header = HEADER.match(plain)
    if not header:
        raise ValueError('missing vendor MD5 header')
    archive = plain[header.end():]
    if hashlib.md5(archive).hexdigest().encode() != header[1].lower():
        raise ValueError('vendor MD5 mismatch')
    return archive

def pack_image(archive: bytes) -> bytes:
    return xor(hashlib.md5(archive).hexdigest().encode() + b'  update.swu\n' + archive)

@dataclass
class Member:
    name: str
    header: bytes
    payload: bytes

def read_cpio(data: bytes) -> list[Member]:
    entries, seen, offset = [], set(), 0
    while offset + 110 <= len(data):
        header = data[offset:offset+110]
        if header[:6] not in (b'070701', b'070702'):
            raise ValueError('unsupported/truncated CPIO header')
        fields = [int(header[6+8*i:14+8*i],16) for i in range(13)]
        size, name_size, checksum = fields[6], fields[11], fields[12]
        offset += 110
        raw_name = data[offset:offset+name_size]
        if not raw_name.endswith(b'\0') or len(raw_name) != name_size:
            raise ValueError('truncated CPIO filename')
        name = raw_name[:-1].decode('ascii')
        if name in seen or name not in ('sw-description','customer','kernel','TRAILER!!!'):
            raise ValueError('unexpected or duplicate archive member: '+name)
        seen.add(name)
        offset = (offset + name_size + 3) & ~3
        payload = data[offset:offset+size]
        if len(payload) != size:
            raise ValueError('truncated CPIO payload')
        if header[:6] == b'070702' and (sum(payload)&0xffffffff) != checksum:
            raise ValueError('CPIO CRC mismatch: '+name)
        entries.append(Member(name,header,payload))
        offset = (offset + size + 3) & ~3
        if name == 'TRAILER!!!':
            if size or any(data[offset:]):
                raise ValueError('nonzero CPIO trailer')
            if [m.name for m in entries] != ['sw-description','customer','kernel','TRAILER!!!']:
                raise ValueError('unexpected archive order/members')
            return entries
    raise ValueError('missing CPIO trailer')

def write_cpio(entries: list[Member], replacement: dict[str,bytes] | None = None) -> bytes:
    replacement = replacement or {}
    out = bytearray()
    for entry in entries:
        data = replacement.get(entry.name,entry.payload)
        header = bytearray(entry.header)
        if data != entry.payload:
            header[54:62] = f'{len(data):08X}'.encode()
            checksum = sum(data)&0xffffffff if header[:6] == b'070702' else 0
            header[102:110] = f'{checksum:08X}'.encode()
        out += header + entry.name.encode() + b'\0'
        out += b'\0' * (-len(out)%4)
        out += data
        out += b'\0' * (-len(out)%4)
    out += b'\0' * (-len(out)%512)
    return bytes(out)

def filesystem_snapshot(data: bytes) -> tuple[dict,dict]:
    fs = SquashFS(io.BytesIO(data))
    records = {}
    def walk(node, path):
        record = {'mode':node.mode,'uid':node.uid,'gid':node.gid,'mtime':node.mtime.isoformat()}
        if node.is_file():
            with node.open() as f: content=f.read()
            record.update(sha256=digest(content),size=len(content))
        elif node.is_device():
            record['rdev'] = node.header.rdev
        elif node.is_symlink():
            record['link'] = node.link
        records[path] = record
        if node.is_dir():
            for child in node.iterdir(): walk(child,path.rstrip('/')+'/'+child.name)
    walk(fs.root,'/')
    return records,{'version':f'{fs.major}.{fs.minor}','block_size':fs.block_size,
                    'compression':fs.sb.compression,'bytes_used':fs.size,
                    'mkfs_time':fs.mkfs_time.isoformat()}

def verify_candidate(source: bytes, candidate: bytes, overlay_root: Path) -> dict:
    old = {m.name:m.payload for m in read_cpio(unpack_image(source))}
    new = {m.name:m.payload for m in read_cpio(unpack_image(candidate))}
    if old['kernel'] != new['kernel'] or old['sw-description'] != new['sw-description']:
        raise ValueError('kernel or updater description changed')
    if len(new['kernel'])>BOOT_CAPACITY or len(new['customer'])>CUSTOMER_CAPACITY:
        raise ValueError('partition capacity exceeded')
    before, old_fs = filesystem_snapshot(old['customer'])
    after, new_fs = filesystem_snapshot(new['customer'])
    expected = {'/ota/www/'+p for p in OVERLAY}
    if set(before)-set(after): raise ValueError('original filesystem paths lost')
    changes=[]
    for path,record in before.items():
        other=after[path]
        if path not in expected and record != other: raise ValueError('unintended inode/data change: '+path)
        if path in expected:
            for key in ('mode','uid','gid','mtime'):
                if record[key] != other[key]: raise ValueError('original file metadata changed: '+path)
    for relative in OVERLAY:
        path='/ota/www/'+relative
        expected_data=(overlay_root/relative).read_bytes()
        if after.get(path,{}).get('sha256') != digest(expected_data):
            raise ValueError('overlay contents not reproduced: '+path)
        if path not in before and (after[path]['mode'] != stat.S_IFREG|0o644 or after[path]['uid'] or after[path]['gid']):
            raise ValueError('incorrect new file permissions: '+path)
        changes.append({'path':path,'action':'replace' if path in before else 'add','sha256':digest(expected_data)})
    if set(after)-set(before) != expected-set(before): raise ValueError('unexpected new filesystem entries')
    for key in ('version','block_size','compression','mkfs_time'):
        if old_fs[key] != new_fs[key]: raise ValueError('SquashFS property changed: '+key)
    return {'kernel_unchanged':True,'sw_description_unchanged':True,'original_inodes_preserved':len(before),
            'console_device_preserved':after['/dev/console'],'original_filesystem':old_fs,
            'candidate_filesystem':new_fs,'customer_size':len(new['customer']),
            'customer_partition_capacity':CUSTOMER_CAPACITY,'kernel_size':len(new['kernel']),
            'changes':changes,'source_sha256':digest(source),'candidate_sha256':digest(candidate),
            'candidate_size':len(candidate),'device_tested':False,'flashed':False,
            'updater_authentication_fully_verified':False}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=ROOT/'evidence/firmware/26011517.5234.2/update.img')
    p.add_argument('--output',type=Path,default=ROOT/'dist/0.5.0')
    args=p.parse_args()
    if args.output.exists(): p.error('output directory already exists; use a new directory')
    source=args.source.read_bytes()
    if digest(source)!=SOURCE_SHA: p.error('source is not the pinned stable 5234 image')
    archive=unpack_image(source); members=read_cpio(archive)
    if write_cpio(members)!=archive or pack_image(archive)!=source: p.error('source roundtrip was not byte-identical')
    args.output.mkdir(parents=True)
    original_customer=next(m.payload for m in members if m.name=='customer')
    base=args.output/'customer.original.squashfs'; base.write_bytes(original_customer)
    target=args.output/'customer.modified.squashfs'
    helper=ROOT/'tools/smartbox-squashfs/target/release/smartbox-squashfs.exe'
    if not helper.is_file(): p.error('build tools/smartbox-squashfs with cargo build --release --locked first')
    command=[str(helper),str(base),str(target)]
    for name in OVERLAY:
        command += ['replace' if name=='index.html' else 'add','/ota/www/'+name,str(ROOT/'web-ui'/name)]
    subprocess.run(command,check=True)
    candidate=pack_image(write_cpio(members,{'customer':target.read_bytes()}))
    report=verify_candidate(source,candidate,ROOT/'web-ui')
    report.update(source_roundtrip_byte_identical=True,version='0.5.0',squashfs_writer='backhand 0.25.5',
                  squashfs_writer_sha256=digest(helper.read_bytes()))
    (args.output/'firmware-0.5.0.candidate.img').write_bytes(candidate)
    (args.output/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__': main()

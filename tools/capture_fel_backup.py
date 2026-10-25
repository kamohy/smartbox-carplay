#!/usr/bin/env python3
"""Read-only V821 FEL probe and two-pass SPI-NOR backup. Never flashes."""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
XFEL = ROOT/'evidence/tools/xfel-v1.4.0/xfel-windows-v1.4.0/xfel.exe'
XFEL_SHA = '74b31e9a6fccf4c25a03c2f60f049e975a58c9d772720911fc5cd319e0bba3a7'
LIBUSB_SHA = 'd2c5526c7d4885a86a0094d06f118b462aa6302827dacb75fa8c79eac2c0a3a0'
CAPACITY = 0x1000000
PARTITIONS = (
    ('uboot',0,0x60000),('boot',0x60000,0x370000),('recovery',0x370000,0x680000),
    ('rootfs',0x680000,0xb00000),('customer',0xb00000,0xea0000),
    ('env',0xea0000,0xeb0000),('env-redund',0xeb0000,0xec0000),
    ('private',0xec0000,0xed0000),('logo',0xed0000,0xf80000),('UDISK',0xf80000,CAPACITY))

def sha(data: bytes) -> str: return hashlib.sha256(data).hexdigest()

def allowed_command(args: tuple[str,...]) -> bool:
    return args in (('version',),('spinor',)) or (
        len(args)==5 and args[:4]==('spinor','read','0','0x1000000')
        and Path(args[4]).suffix=='.bin')

def run_xfel(exe: Path, *args: str) -> str:
    if not allowed_command(args): raise ValueError('only version, SPI detection and full read commands are allowed')
    result=subprocess.run([str(exe),*args],cwd=exe.parent,capture_output=True,timeout=180)
    text=(result.stdout+result.stderr).decode('utf-8',errors='replace')
    # xfel can return exit code 0 even when no device was found.
    if result.returncode or any(x in text.lower() for x in ('error:', 'no fel device', "can't read", "can't detect")):
        raise RuntimeError(text.strip() or f'xfel failed ({result.returncode})')
    return text.strip()

def validate_pair(first: bytes,second: bytes) -> dict:
    if len(first)!=CAPACITY or len(second)!=CAPACITY: raise ValueError('both dumps must contain exactly 16 MiB')
    if first != second: raise ValueError('independent flash reads differ')
    if first[:256] in (b'\0'*256,b'\xff'*256): raise ValueError('empty/blank bootloader header')
    if first[0x60000:0x60008]!=b'ANDROID!': raise ValueError('boot partition is not the expected Android image')
    for offset in (0x680000,0xb00000):
        if first[offset:offset+4]!=b'hsqs': raise ValueError('expected SquashFS partition header missing')
    return {'size':CAPACITY,'sha256':sha(first),'two_reads_identical':True,
        'layout_headers_match_expected':True,
        'partitions':[{'name':n,'start':a,'end':b,'sha256':sha(first[a:b])} for n,a,b in PARTITIONS],
        'filesystem_contents_fully_validated':False,'recovery_write_verified':False,
        'flash_performed':False,'warning':'Header checks and matching reads do not prove a tested restore.'}

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--xfel',type=Path,default=XFEL)
    p.add_argument('--capture',action='store_true',help='two full flash reads after a valid V821/16-MiB probe')
    args=p.parse_args()
    try:
        exe=args.xfel.resolve()
        if sha(exe.read_bytes())!=XFEL_SHA or sha((exe.parent/'libusb-1.0.dll').read_bytes())!=LIBUSB_SHA:
            raise ValueError('xfel executable/DLL do not match the pinned upstream 1.4.0 build')
        version=run_xfel(exe,'version')
        if 'V821' not in version: raise ValueError('connected FEL device is not V821')
        print(version,flush=True)
        chip=run_xfel(exe,'spinor')
        if f'with {CAPACITY} bytes' not in chip: raise ValueError('SPI-NOR capacity is not the expected 16 MiB')
        print(chip,flush=True)
        if not args.capture:
            print('Probe only. No dump, flash, reset or driver change performed.');return 0
        folder=ROOT/'evidence/full-backups'/datetime.now().strftime('%Y-%m-%d-%H%M%S')
        folder.mkdir(parents=True,exist_ok=False)
        paths=[folder/'flash-pass1.bin',folder/'flash-pass2.bin']
        for i,path in enumerate(paths,1):
            print(f'Reading all 16 MiB, pass {i}/2...',flush=True)
            run_xfel(exe,'spinor','read','0','0x1000000',str(path))
            if not path.is_file() or path.stat().st_size!=CAPACITY: raise ValueError('incomplete flash read')
        result=validate_pair(*(x.read_bytes() for x in paths))
        result.update(created_at=datetime.now().astimezone().isoformat(),xfel_sha256=XFEL_SHA,
                      transport_probe=version,spi_probe=chip)
        (folder/'backup-validation.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
        print(f'Validated identical reads: {folder}\nSHA-256: {result["sha256"]}')
        return 0
    except (OSError,ValueError,RuntimeError,subprocess.TimeoutExpired) as e:
        print(f'STOP: {e}')
        return 2

if __name__=='__main__': raise SystemExit(main())

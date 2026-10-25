#!/usr/bin/env python3
"""Prepare an OFFLINE, pinned diagnostic ELF. No upload or execution support."""
from __future__ import annotations
import argparse
import hashlib
import io
import json
from pathlib import Path
from capstone import Cs,CS_ARCH_RISCV,CS_MODE_RISCV32,CS_MODE_RISCVC
from elftools.elf.elffile import ELFFile

ROOT=Path(__file__).resolve().parents[1]
SOURCE_SHA256='0d0d6c885dde39205074e7d9989f339561b69202182f26d33a5d1e71cbf37cc9'
OLD_FORMAT=b'getAudioFormat support48=%d  \n\0'
NEW_FORMAT=b'BH_HU mask=%08x gate=%u\n\0'

def sha(data):return hashlib.sha256(data).hexdigest()

def compressed_arguments(stack_offset: int) -> bytes:
    """c.lwsp a2, offset(sp); c.mv a3,s2, within one original 4-byte slot."""
    if stack_offset%4 or not 0<=stack_offset<=252:raise ValueError('Invalid c.lwsp offset')
    load=0x4002|(12<<7)|(((stack_offset>>5)&1)<<12)|(((stack_offset>>2)&7)<<4)|(((stack_offset>>6)&3)<<2)
    move=0x8002|(13<<7)|(18<<2)
    code=load.to_bytes(2,'little')+move.to_bytes(2,'little')
    decoder=Cs(CS_ARCH_RISCV,CS_MODE_RISCV32|CS_MODE_RISCVC)
    ops=list(decoder.disasm(code,0))
    if len(ops)!=2 or ops[0].mnemonic!='c.lwsp' or ops[1].mnemonic!='c.mv':raise ValueError('Independent decoder rejected probe instructions')
    if ops[0].op_str not in (f'a2, {stack_offset}(sp)',f'a2, {hex(stack_offset)}(sp)') or ops[1].op_str!='a3, s2':raise ValueError('Probe arguments decode differently')
    return code

def prepare(source: bytes) -> tuple[bytes,dict]:
    if sha(source)!=SOURCE_SHA256:raise ValueError('Source is not the pinned stable rcpservice')
    elf=ELFFile(io.BytesIO(source));segments=list(elf.iter_segments())
    def offset(address,size):
        for s in segments:
            if s['p_type']=='PT_LOAD' and s['p_vaddr']<=address and address+size<=s['p_vaddr']+s['p_filesz']:
                return s['p_offset']+address-s['p_vaddr']
        raise ValueError('Target outside a file-backed load segment')
    target=bytearray(source);changes=[]
    for address,old,stack_offset in [(0x2BF80,bytes.fromhex('13061000'),0x28),(0x2C088,bytes.fromhex('13060000'),4)]:
        at=offset(address,4)
        if source[at:at+4]!=old:raise ValueError('Original log argument instruction changed')
        new=compressed_arguments(stack_offset);target[at:at+4]=new
        changes.append({'virtual_address':hex(address),'file_offset':at,'before_hex':old.hex(),'after_hex':new.hex(),'effect':f'log mask from sp+{hex(stack_offset)}, gate version from s2'})
    at=offset(0x3EADC,len(OLD_FORMAT))
    if source[at:at+len(OLD_FORMAT)]!=OLD_FORMAT or len(NEW_FORMAT)>len(OLD_FORMAT):raise ValueError('Original log format changed or replacement too long')
    new=NEW_FORMAT.ljust(len(OLD_FORMAT),b'\0');target[at:at+len(new)]=new
    changes.append({'virtual_address':'0x3eadc','file_offset':at,'before_hex':OLD_FORMAT.hex(),'after_hex':new.hex(),'effect':'replace existing format string in place'})
    result=bytes(target)
    allowed={i for c in changes for i in range(c['file_offset'],c['file_offset']+len(bytes.fromhex(c['before_hex'])))}
    differing={i for i,(a,b) in enumerate(zip(source,result)) if a!=b}
    if len(result)!=len(source) or not differing.issubset(allowed):raise ValueError('Unexpected data change')
    # The call and format-pointer instructions are untouched at both log sites.
    for address in (0x2BF7C,0x2BF84,0x2BF88,0x2C084,0x2C08C,0x2C090):
        at=offset(address,4)
        if source[at:at+4]!=result[at:at+4]:raise ValueError('Logging control flow changed')
    return result,{'version':'0.8.1','source_sha256':sha(source),'candidate_sha256':sha(result),'size':len(result),
        'changed_byte_count':len(differing),'changes':changes,'audio_selection_code_unchanged':True,
        'log_call_sites_unchanged':True,'original_format_pointers_preserved':True,'device_tested':False,
        'integrated_in_firmware':False,'flashed':False,
        'interpretation':'mask is the capability word used by this branch; gate is the parsed first plugin version number or zero when that code did not parse it; not proof of successful 16 kHz playback'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--source',type=Path,default=ROOT/'evidence/firmware/26011517.5234.2/decrypted/lylink-unpacked/rcpservice')
    p.add_argument('--output',type=Path,default=ROOT/'dist/phone-probe-0.8.1')
    args=p.parse_args();binary,report=prepare(args.source.read_bytes());args.output.mkdir(parents=True,exist_ok=False)
    (args.output/'rcpservice.phone-probe').write_bytes(binary)
    (args.output/'probe-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()

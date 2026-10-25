"""Build the minimal 0.8.2 maintenance overlay on pinned, installed UI 0.7.0.

Only customer is included. The existing bootenv phase sequence is preserved;
only the kernel image descriptor and kernel member are omitted.
"""
from pathlib import Path
import argparse, json, re, subprocess
from tools.build_ui_firmware import ROOT, digest, unpack_image, pack_image, read_cpio, write_cpio, filesystem_snapshot, verify_candidate

VERSION='0.8.2'
BASE_SHA='32e395c7ff22fcf40eb019748126e554694786974d261f70ab4fe07171e6aeb4'
PATHS=('/ota/www/index.html','/ota/www/js/bh-update-config.json','/ota/www/js/bh-maintenance.js','/ota/www/cgi-bin/bh-diagnostics.cgi','/app/bh-log-recorder.sh')

def customer_only_description(source:bytes)->bytes:
    pattern=rb'\{\s*filename\s*=\s*"kernel";\s*device\s*=\s*"/dev/by-name/boot";\s*installed-directly\s*=\s*true;\s*\},'
    result,count=re.subn(pattern,b'',source)
    if count!=1 or b'filename = "kernel"' in result or b'"/dev/by-name/boot"' in result:
        raise ValueError('Descriptor does not contain exactly one known kernel image block')
    if b'ly_project_name = "ly5234"' not in result or b'filename = "customer"' not in result:
        raise ValueError('Unexpected project or missing customer image')
    return result

def verify_package(source:bytes,candidate:bytes,changes:list[dict])->dict:
    if digest(source)!=BASE_SHA:raise ValueError('Unreviewed maintenance baseline')
    original=read_cpio(unpack_image(source));by_name={m.name:m for m in original}
    members=read_cpio(unpack_image(candidate),customer_only=True)
    if members[0].payload!=customer_only_description(by_name['sw-description'].payload):
        raise ValueError('Unexpected bootenv/descriptor modification')
    if {x['path'] for x in changes}!=set(PATHS):raise ValueError('Unexpected maintenance overlay scope')
    # Independently verify all original inodes/data via the existing full-image verifier.
    synthetic=pack_image(write_cpio(original,{'customer':members[1].payload}))
    checked=verify_candidate(source,synthetic,None,expected_changes=changes)
    checked.update(version=VERSION,package_kind='customer-only-maintenance',baseline_ui='0.7.0',
        kernel_included=False,kernel_write_requested=False,bootenv_sequence_unchanged=True,
        descriptor_change='omit only the kernel image block',
        candidate_sha256=digest(candidate),candidate_size=len(candidate),
        device_tested=False,flashed=False,source_roundtrip_byte_identical=pack_image(write_cpio(original))==source)
    return checked

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'dist/maintenance-0.8.2')
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    source=(ROOT/'ota/5234/firmware-0.7.0.img').read_bytes()
    if digest(source)!=BASE_SHA:raise ValueError('Baseline hash mismatch')
    members=read_cpio(unpack_image(source));original=next(m.payload for m in members if m.name=='customer')
    before,_=filesystem_snapshot(original)
    base=args.output/'customer.original.squashfs';base.write_bytes(original)
    target=args.output/'customer.modified.squashfs'
    command=[str(ROOT/'tools/smartbox-squashfs/target/release/smartbox-squashfs.exe'),str(base),str(target)]
    changes=[]
    for path in PATHS:
        file=ROOT/'maintenance-overlay'/path.lstrip('/')
        command+=['replace' if path in before else 'add',path,str(file)]
        changes.append({'path':path,'sha256':digest(file.read_bytes())})
    subprocess.run(command,check=True)
    trimmed=[m for m in members if m.name!='kernel']
    descriptor=customer_only_description(members[0].payload)
    candidate=pack_image(write_cpio(trimmed,{'sw-description':descriptor,'customer':target.read_bytes()}))
    report=verify_package(source,candidate,changes)
    (args.output/f'firmware-{VERSION}.candidate.img').write_bytes(candidate)
    (args.output/'build-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:report[k] for k in ('version','candidate_size','candidate_sha256','customer_size','kernel_included','bootenv_sequence_unchanged')},indent=2))

if __name__=='__main__':main()

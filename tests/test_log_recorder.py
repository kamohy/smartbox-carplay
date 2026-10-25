"""Run the real recorder against controlled mounts, flash capacity and boot cycles."""
import gzip
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SHELL=shutil.which('sh') or ('C:/Program Files/Git/bin/sh.exe' if Path('C:/Program Files/Git/bin/sh.exe').exists() else None)

def shellpath(path):
    value=Path(path).as_posix()
    return '/'+value[0].lower()+value[2:] if os.name=='nt' else value

@unittest.skipUnless(SHELL,'POSIX shell required')
class PersistentRecorder(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.base=self.root/'data';self.proc=self.root/'proc';self.ram=self.root/'ram';self.bin=self.root/'bin'
        for p in (self.base,self.proc,self.bin):p.mkdir()
        (self.base/'unrelated').write_bytes(b'KEEP')
        self.mount()
        for name,data in {'uptime':'123.50 50.00\n','meminfo':'MemTotal: 60000 kB\nMemAvailable: 20000 kB\n','stat':'cpu 100 0 100 100 0 0 0 0\ncpu0 100 0 100 100 0 0 0 0\n','loadavg':'0.1 0.2 0.3 1/30 900\n'}.items():
            (self.proc/name).write_bytes(data.encode())
        self.executable('df',"#!/bin/sh\nprintf 'Filesystem 1024-blocks Used Available Capacity Mounted on\\nfixture 512 100 %s 20%% data\\n' \"${BH_TEST_FREE:-400}\"\n")
        self.executable('dmesg',"#!/bin/sh\nprintf 'kernel fixture\\n'\n")
        self.executable('logcat',"#!/bin/sh\nif [ -n \"$BH_TEST_LOG\" ]; then cat \"$BH_TEST_LOG\"; else printf 'phone call rate=16000, sz=16\\nUSB mic times = 10, rate = 48kHz -> 16kHz\\n'; fi\n")
        self.env={**os.environ,'BH_LOG_MOUNT':shellpath(self.base),'BH_PROC_ROOT':shellpath(self.proc),'BH_LOG_RAM':shellpath(self.ram),
            'BH_STATUS_CGI':shellpath(ROOT/'web-ui/cgi-bin/bh-diagnostics.cgi'),'BH_SYS_ROOT':shellpath(self.root/'absent'),
            'BH_RECORDER':shellpath(ROOT/'firmware-overlay/app/bh-log-recorder.sh'),'BH_TEST_BIN':shellpath(self.bin)}
    def executable(self,name,data):
        path=self.bin/name;path.write_bytes(data.encode());path.chmod(0o755)
    def mount(self,fs='jffs2',mode='rw'):
        (self.proc/'mounts').write_bytes(f'/dev/mtdblock9 {shellpath(self.base)} {fs} {mode},relatime 0 0\n'.encode())
    def run_script(self,command,extra=None,check=True):
        return subprocess.run([SHELL,'-c','PATH="$BH_TEST_BIN:$PATH"; export PATH; exec sh "$BH_RECORDER" "$@"','recorder',command],
            env={**self.env,**(extra or {})},capture_output=True,check=check)
    def status(self):return json.loads(self.run_script('status').stdout)
    def test_capacity_crc_boot_retention_and_unrelated_data(self):
        for boot in range(1,5):
            if self.ram.exists():shutil.rmtree(self.ram)
            self.run_script('once');self.run_script('once')
            status=self.status();self.assertTrue(status['supported']);self.assertEqual(status['state'],'saved')
            for item in status['files']:
                self.assertLessEqual(item['bytes'],24576)
                data=gzip.decompress((self.base/'bh-logs'/f"log-{item['id']}.gz").read_bytes())
                self.assertIn(b'phone call rate=16000, sz=16',data)
                self.assertIn(b'"idle_seconds":50.00',data)
            self.assertLessEqual(len(status['files']),6)
        self.assertEqual({x['boot'] for x in status['files']},{2,3,4})
        self.assertEqual((self.base/'unrelated').read_bytes(),b'KEEP')
        self.assertFalse(list((self.base/'bh-logs').glob('*.pending')))
    def test_low_space_preserves_complete_logs(self):
        self.run_script('once');before={p.name:p.read_bytes() for p in (self.base/'bh-logs').iterdir()}
        result=self.run_script('once',{'BH_TEST_FREE':'70'},check=False)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual(self.status()['state'],'no_space')
        self.assertEqual(before,{p.name:p.read_bytes() for p in (self.base/'bh-logs').iterdir()})
    def test_missing_readonly_or_ram_mount_never_creates_log_directory(self):
        for fs,mode in [('jffs2','ro'),('tmpfs','rw'),('rootfs','rw'),('squashfs','rw')]:
            self.mount(fs,mode);self.assertNotEqual(self.run_script('once',check=False).returncode,0)
            self.assertFalse((self.base/'bh-logs').exists())
        (self.proc/'mounts').unlink();self.assertFalse(self.status()['supported'])
    def test_oversized_compressed_log_is_not_written_to_flash(self):
        rng=random.Random(7)
        data=''.join(''.join(rng.choices('abcdefghijklmnopqrstuvwxyz0123456789',k=1200))+'\n' for _ in range(1400))
        source=self.root/'large.txt';source.write_bytes(data.encode())
        self.assertNotEqual(self.run_script('once',{'BH_TEST_LOG':shellpath(source)},check=False).returncode,0)
        self.assertEqual(self.status()['state'],'snapshot_too_large')
        self.assertFalse(list((self.base/'bh-logs').glob('log-*.gz')))
    def test_cgi_stored_audio_download_and_query_restrictions(self):
        self.run_script('once')
        def cgi(query,method='GET',origin=''):
            return subprocess.run([SHELL,str(ROOT/'web-ui/cgi-bin/bh-diagnostics.cgi')],env={**self.env,'QUERY_STRING':query,'REQUEST_METHOD':method,'HTTP_ORIGIN':origin},capture_output=True,check=True).stdout
        response=cgi('id=stored0a');header,data=response.split(b'\r\n\r\n',1)
        self.assertIn(b'application/gzip',header);self.assertIn(b'phone call rate=16000',gzip.decompress(data))
        self.assertIn(b'48kHz -> 16kHz',cgi('id=audio&source=0a'))
        self.assertTrue(cgi('id=stored../etc/passwd').startswith(b'Status: 400'))
        self.assertTrue(cgi('id=audio&source=0a&command=reboot').startswith(b'Status: 400'))
        self.assertTrue(cgi('id=save','POST','https://example.com').startswith(b'Status: 403'))
        self.assertTrue(cgi('id=save','POST').startswith(b'Status: 503')) # no daemon in fixture

if __name__=='__main__':unittest.main()

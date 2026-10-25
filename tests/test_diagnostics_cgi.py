"""Run the real shell CGI against controlled proc/sys fixtures without device writes."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
SHELL=shutil.which('sh') or ('C:/Program Files/Git/bin/sh.exe' if Path('C:/Program Files/Git/bin/sh.exe').exists() else None)

@unittest.skipUnless(SHELL,'POSIX shell required')
class DeviceCGI(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.proc=self.root/'proc';self.sys=self.root/'sys';self.proc.mkdir()
        for name,text in {'uptime':'123.50 50.00\n','loadavg':'0.10 0.20 0.30 1/30 900\n',
            'meminfo':'MemTotal: 60000 kB\nMemAvailable: 20000 kB\n',
            'stat':'cpu 100 20 30 500 25 3 2 0 0 0\ncpu0 100 20 30 500 25 3 2 0 0 0\n'}.items():
            (self.proc/name).write_bytes(text.encode('ascii'))
        stats=self.sys/'class/net/p2p-wlan0-0/statistics';stats.mkdir(parents=True)
        for metric in ('rx_bytes','tx_bytes','rx_dropped','tx_dropped','rx_errors','tx_errors'):
            (stats/metric).write_bytes(b'123\n')
        usb=self.sys/'class/udc/test';usb.mkdir(parents=True);(usb/'state').write_bytes(b'configured\n')
    def run_cgi(self,query,method='GET'):
        env={**os.environ,'BH_PROC_ROOT':self.proc.as_posix(),'BH_SYS_ROOT':self.sys.as_posix(),
             'QUERY_STRING':query,'REQUEST_METHOD':method}
        result=subprocess.run([SHELL,str(ROOT/'web-ui/cgi-bin/bh-diagnostics.cgi')],env=env,capture_output=True,check=True)
        return result.stdout.replace(b'\r\n',b'\n').decode('utf-8')
    def test_real_status_json_and_numeric_values(self):
        header,body=self.run_cgi('id=status').split('\n\n',1);j=json.loads(body)
        self.assertIn('Cache-Control: no-store',header)
        self.assertEqual(j['cpu'],{'total_jiffies':680,'idle_jiffies':525})
        self.assertEqual(j['memory_kib']['available'],20000)
        self.assertEqual(j['network']['rx_dropped'],123)
        self.assertEqual(j['uptime_seconds'],123.5);self.assertEqual(j['usb_state'],'configured')
    def test_missing_metrics_are_unknown_not_fabricated_zero(self):
        (self.proc/'uptime').unlink();(self.proc/'meminfo').unlink()
        j=json.loads(self.run_cgi('id=status').split('\n\n',1)[1])
        self.assertIsNone(j['uptime_seconds']);self.assertIsNone(j['memory_kib']['available'])
    def test_post_and_extra_query_arguments_rejected(self):
        self.assertTrue(self.run_cgi('id=status','POST').startswith('Status: 405'))
        self.assertTrue(self.run_cgi('id=status&command=reboot').startswith('Status: 400'))
        self.assertTrue(self.run_cgi('id=status;reboot').startswith('Status: 400'))
        self.assertTrue(self.run_cgi('id=/etc/passwd').startswith('Status: 400'))
        self.assertTrue(self.run_cgi('').startswith('Status: 400'))

if __name__=='__main__':unittest.main()

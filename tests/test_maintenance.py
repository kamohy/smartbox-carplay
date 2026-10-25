"""Maintenance-only descriptor, real CGI space/error output, and deletion scope."""
import json,os,subprocess,unittest
from pathlib import Path
from tools.build_maintenance_firmware import customer_only_description
from tools.build_ui_firmware import read_cpio,write_cpio
from tests.test_ui_firmware import member
from tests import test_log_recorder as recorder_tests
SHELL=recorder_tests.SHELL
shellpath=recorder_tests.shellpath
ROOT=recorder_tests.ROOT

class Maintenance(unittest.TestCase):
    def test_descriptor_omits_only_kernel_and_keeps_bootenv(self):
        source=b'ly_project_name = "ly5234"; images: ({ filename = "kernel"; device = "/dev/by-name/boot"; installed-directly = true; },{ filename = "customer"; device = "/dev/by-name/customer"; }); bootenv: ({name="boot_partition";value="recovery";});'
        result=customer_only_description(source)
        self.assertNotIn(b'filename = "kernel"',result)
        self.assertEqual(result,source.replace(b'{ filename = "kernel"; device = "/dev/by-name/boot"; installed-directly = true; },',b''))
        with self.assertRaises(ValueError):customer_only_description(result)
        with self.assertRaises(ValueError):customer_only_description(source.replace(b'ly5234',b'ly5190'))
        data=write_cpio([member('sw-description',result),member('customer',b'data'),member('TRAILER!!!',b'')])
        self.assertEqual(len(read_cpio(data,customer_only=True)),3)
        with self.assertRaises(ValueError):read_cpio(data)

    @unittest.skipUnless(SHELL,'POSIX shell required')
    def test_real_space_error_cgi_and_owned_log_clear(self):
        fixture=recorder_tests.PersistentRecorder();fixture.setUp();self.addCleanup(fixture.doCleanups)
        fixture.env['BH_RECORDER']=shellpath(ROOT/'maintenance-overlay/app/bh-log-recorder.sh')
        fixture.env['BH_STATUS_CGI']=shellpath(ROOT/'maintenance-overlay/ota/www/cgi-bin/bh-diagnostics.cgi')
        fixture.test_clear_only_removes_owned_logs_and_preserves_counter_and_other_data()
        fixture.executable('ps','#!/bin/sh\nprintf "100 root /sbin/update\\n"\n')
        fixture.executable('dmesg','#!/bin/sh\nprintf "normal boot\\nNo space left on device\\n"\n')
        fixture.executable('logcat','#!/bin/sh\nprintf "normal message\\nupdate: allocation failed\\n"\n')
        def query(value,method='GET',origin=''):
            env={**fixture.env,'QUERY_STRING':value,'REQUEST_METHOD':method,'HTTP_ORIGIN':origin}
            return subprocess.run([SHELL,'-c','PATH="$BH_TEST_BIN:$PATH"; export PATH; exec sh "$BH_STATUS_CGI"'],env=env,capture_output=True,check=True).stdout.replace(b'\r\n',b'\n').decode()
        space=json.loads(query('id=space').split('\n\n',1)[1]);self.assertEqual(space['memory_available_kib'],20000)
        self.assertEqual([x['path'] for x in space['filesystems']],['/tmp','/mnt/UDISK','/mnt/customer','/'])
        self.assertTrue(all(x['available_kib']==400 for x in space['filesystems']))
        errors=query('id=errors');self.assertIn('No space left on device',errors);self.assertIn('update: allocation failed',errors)
        self.assertNotIn('normal message',errors);self.assertIn('/sbin/update',errors)
        self.assertTrue(query('id=errors&command=reboot').startswith('Status: 400'))
        self.assertTrue(query('id=errors','POST').startswith('Status: 405'))
        self.assertTrue(query('id=clear','POST','https://example.com').startswith('Status: 403'))

if __name__=='__main__':unittest.main()

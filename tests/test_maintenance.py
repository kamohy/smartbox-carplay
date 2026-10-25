"""Maintenance-only descriptor, real CGI space/error output, and deletion scope."""
import json,os,subprocess,unittest,time
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
    def test_recorder_does_not_start_when_native_update_is_active(self):
        fixture=recorder_tests.PersistentRecorder();fixture.setUp();self.addCleanup(fixture.doCleanups)
        fixture.env['BH_RECORDER']=shellpath(ROOT/'maintenance-overlay/app/bh-log-recorder.sh')
        update=fixture.root/'absent/class/misc/ly_misc_dev/ly/update';update.parent.mkdir(parents=True)
        update.write_bytes(b'ly_update_status=1\n')
        fixture.run_script('run')
        self.assertEqual(fixture.status()['state'],'paused_for_update')
        self.assertFalse(fixture.status()['running'])
        self.assertFalse((fixture.base/'bh-logs').exists())

    @unittest.skipUnless(SHELL,'POSIX shell required')
    def test_running_recorder_exits_when_native_update_begins(self):
        fixture=recorder_tests.PersistentRecorder();fixture.setUp();self.addCleanup(fixture.doCleanups)
        fixture.env['BH_RECORDER']=shellpath(ROOT/'maintenance-overlay/app/bh-log-recorder.sh')
        fixture.env['BH_STATUS_CGI']=shellpath(ROOT/'maintenance-overlay/ota/www/cgi-bin/bh-diagnostics.cgi')
        update=fixture.root/'absent/class/misc/ly_misc_dev/ly/update';update.parent.mkdir(parents=True)
        update.write_bytes(b'ly_update_status=0\n')
        process=subprocess.Popen([SHELL,'-c','PATH="$BH_TEST_BIN:$PATH"; export PATH; exec sh "$BH_RECORDER" run'],env=fixture.env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        self.addCleanup(lambda:process.terminate() if process.poll() is None else None)
        until=time.monotonic()+8
        while not list((fixture.base/'bh-logs').glob('log-*.gz')) and time.monotonic()<until:time.sleep(.05)
        self.assertTrue(list((fixture.base/'bh-logs').glob('log-*.gz')))
        self.assertTrue((fixture.ram/'pid').exists())
        update.write_bytes(b'ly_update_status=1\n')
        self.assertEqual(process.wait(timeout=12),0)
        self.assertFalse((fixture.ram/'pid').exists())
        self.assertEqual(fixture.status()['state'],'paused_for_update')

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
        # The combined settings UI must retain the maintenance endpoints as well.
        fixture.env['BH_STATUS_CGI']=shellpath(ROOT/'web-ui/cgi-bin/bh-diagnostics.cgi')
        merged=json.loads(query('id=space').split('\n\n',1)[1])
        self.assertEqual(merged,space)
        self.assertIn('No space left on device',query('id=errors'))
        self.assertIn('=== /proc/meminfo ===',query('id=hardware'))
        self.assertTrue(query('id=hardware&command=reboot').startswith('Status: 400'))

if __name__=='__main__':unittest.main()

"""Data-integrity and command-scope checks; these do not simulate a real recovery."""
import unittest
from tools.capture_fel_backup import CAPACITY,allowed_command,validate_pair

class ReadOnlyScope(unittest.TestCase):
    def test_only_probe_and_full_read_commands_allowed(self):
        for args in (('version',),('spinor',),('spinor','read','0','0x1000000','dump.bin')):
            self.assertTrue(allowed_command(args))
        for args in (('reset',),('spinor','erase','0','0x1000000'),('spinor','write','0','file.bin'),
                     ('extra','efuse','write','0','x'),('exec','0x2000000'),('sid',),
                     ('spinor','read','0','0x100','partial.bin')):
            self.assertFalse(allowed_command(args))

class BackupIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Synthetic image: tests only the declared size/header/integrity checks.
        b=bytearray(b'\xff'*CAPACITY);b[:8]=b'eGON.BT0';b[0x60000:0x60008]=b'ANDROID!'
        b[0x680000:0x680004]=b'hsqs';b[0xb00000:0xb00004]=b'hsqs'
        cls.image=bytes(b)
    def test_matching_reads_report_untested_restore_explicitly(self):
        result=validate_pair(self.image,self.image)
        self.assertEqual(len(result['partitions']),10)
        self.assertFalse(result['recovery_write_verified'])
        self.assertFalse(result['filesystem_contents_fully_validated'])
    def test_damaged_mismatching_and_short_reads_rejected(self):
        with self.assertRaises(ValueError):validate_pair(self.image[:-1],self.image[:-1])
        b=bytearray(self.image);b[-1]^=1
        with self.assertRaises(ValueError):validate_pair(self.image,bytes(b))
        b=bytearray(self.image);b[0x680000]^=1
        with self.assertRaises(ValueError):validate_pair(bytes(b),bytes(b))
        with self.assertRaises(ValueError):validate_pair(bytes(CAPACITY),bytes(CAPACITY))

if __name__=='__main__':unittest.main()

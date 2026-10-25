"""Container integrity, source roundtrip and independently read SquashFS contents."""
import unittest
from pathlib import Path
from tools.build_ui_firmware import ROOT, Member, pack_image, unpack_image, read_cpio, write_cpio, verify_candidate

def member(name,data):
    fields=[1,0o100755,0,0,1,0,len(data),0,0,0,0,len(name)+1,sum(data)&0xffffffff]
    return Member(name,b'070702'+''.join(f'{v:08X}' for v in fields).encode(),data)

class Containers(unittest.TestCase):
    def test_crc_and_vendor_md5_detect_corruption(self):
        items=[member('sw-description',b'description'),member('customer',b'customer'),member('kernel',b'kernel'),member('TRAILER!!!',b'')]
        archive=write_cpio(items)
        self.assertEqual([m.payload for m in read_cpio(archive)],[m.payload for m in items])
        self.assertEqual(unpack_image(pack_image(archive)),archive)
        damaged=bytearray(archive); damaged[128]^=1
        with self.assertRaises(ValueError): read_cpio(bytes(damaged))
        damaged=bytearray(pack_image(archive)); damaged[200]^=1
        with self.assertRaises(ValueError): unpack_image(bytes(damaged))

    def test_replacement_recomputes_crc_and_preserves_other_members(self):
        items=[member('sw-description',b'description'),member('customer',b'old'),member('kernel',b'kernel'),member('TRAILER!!!',b'')]
        output=read_cpio(write_cpio(items,{'customer':b'new filesystem payload'}))
        self.assertEqual(output[1].payload,b'new filesystem payload')
        self.assertEqual(output[0],items[0]);self.assertEqual(output[2],items[2])

    @unittest.skipUnless((ROOT/'evidence/firmware/26011517.5234.2/update.img').exists(), 'local original image required')
    def test_real_vendor_roundtrip_is_byte_identical(self):
        source=(ROOT/'evidence/firmware/26011517.5234.2/update.img').read_bytes()
        archive=unpack_image(source)
        self.assertEqual(write_cpio(read_cpio(archive)),archive)
        self.assertEqual(pack_image(archive),source)

    @unittest.skipUnless((ROOT/'dist/0.5.0/firmware-0.5.0.candidate.img').exists(), 'locally built candidate required')
    def test_all_original_inodes_and_non_ui_bytes_preserved(self):
        report=verify_candidate((ROOT/'evidence/firmware/26011517.5234.2/update.img').read_bytes(),
            (ROOT/'dist/0.5.0/firmware-0.5.0.candidate.img').read_bytes(),ROOT/'web-ui')
        self.assertEqual(report['original_inodes_preserved'],66)
        self.assertEqual(report['console_device_preserved']['rdev'],0x501)
        self.assertEqual(len(report['changes']),6)

if __name__=='__main__': unittest.main()

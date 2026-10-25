"""Container integrity, source roundtrip and independently read SquashFS contents."""
import unittest
import json
from pathlib import Path
from tools.build_ui_firmware import ROOT, OVERLAY, Member, pack_image, unpack_image, read_cpio, write_cpio, verify_candidate

CURRENT_VERSION=json.loads((ROOT/'web-ui/js/bh-update-config.json').read_text(encoding='utf-8'))['ui_version']
CURRENT_CANDIDATE=ROOT/f'dist/{CURRENT_VERSION}/firmware-{CURRENT_VERSION}.candidate.img'

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

    @unittest.skipUnless(CURRENT_CANDIDATE.exists(), 'locally built current candidate required')
    def test_all_original_inodes_and_non_ui_bytes_preserved(self):
        report=verify_candidate((ROOT/'evidence/firmware/26011517.5234.2/update.img').read_bytes(),
            CURRENT_CANDIDATE.read_bytes(),ROOT/'web-ui')
        self.assertEqual(report['original_inodes_preserved'],66)
        self.assertEqual(report['console_device_preserved']['rdev'],0x501)
        self.assertEqual(len(report['changes']),len(OVERLAY))
        cgi=next(x for x in report['changes'] if x['path']=='/ota/www/cgi-bin/bh-diagnostics.cgi')
        self.assertEqual(cgi['mode'],'0o100755')

if __name__=='__main__': unittest.main()

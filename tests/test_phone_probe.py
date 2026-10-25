from pathlib import Path
import unittest
from tools.prepare_phone_probe import compressed_arguments,prepare,ROOT

class DiagnosticProbe(unittest.TestCase):
    def test_independent_instruction_decoder_and_invalid_offsets(self):
        self.assertEqual(compressed_arguments(0x28).hex(),'2256ca86')
        self.assertEqual(compressed_arguments(4).hex(),'1246ca86')
        for value in (-4,2,256):
            with self.assertRaises(ValueError):compressed_arguments(value)
    def test_unpinned_source_rejected_before_patching(self):
        with self.assertRaises(ValueError):prepare(b'not the reviewed device binary')
    @unittest.skipUnless((ROOT/'evidence/firmware/26011517.5234.2/decrypted/lylink-unpacked/rcpservice').exists(),'local pinned vendor binary required')
    def test_real_source_only_changes_three_bounded_log_regions(self):
        source=(ROOT/'evidence/firmware/26011517.5234.2/decrypted/lylink-unpacked/rcpservice').read_bytes()
        binary,report=prepare(source)
        self.assertEqual(len(binary),len(source));self.assertEqual(len(report['changes']),3)
        self.assertIn(b'BH_HU mask=%08x gate=%u\n\0',binary)
        self.assertTrue(report['audio_selection_code_unchanged']);self.assertFalse(report['flashed'])
        self.assertEqual(binary[0x1C058:0x1C080],source[0x1C058:0x1C080])

if __name__=='__main__':unittest.main()

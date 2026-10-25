"""Checks against vendor instruction vectors and the archived device artifacts."""

from __future__ import annotations

import gzip
import hashlib
import struct
import unittest
import zlib
from pathlib import Path

from tools.decrypt_logcat import KEY, RESET_SIZE, decrypt, unwrap
from tools.disassemble_riscv_andes import addigp, andes_branch, gp_memory
from tools.extract_lypack import unpack

ROOT = Path(__file__).resolve().parents[1]
FIRMWARE = ROOT / "evidence/firmware"


class AndesVectors(unittest.TestCase):
    def test_vendor_gp_vectors_and_odd_address(self):
        # Published binutils test vectors, including ADDIGP bit 14 as immediate.
        self.assertEqual(addigp(0x0000100B), (0, 0))
        self.assertEqual(addigp(0x0000500B), (0, 1))
        self.assertEqual(gp_memory(0x00A0402B), ("nds.swgp", 10, 0))
        self.assertEqual(gp_memory(0x00A2402B), ("nds.swgp", 10, 4096))
        self.assertEqual(gp_memory(0x0000252B), ("nds.lwgp", 10, 0))
        self.assertEqual(gp_memory(0x0002252B), ("nds.lwgp", 10, 4096))
        # Actual store to the lylinkapp audio-mode global.
        self.assertEqual(gp_memory(0xD29FC1AB), ("nds.swgp", 9, -0x2E0))

    def test_branches(self):
        self.assertEqual(andes_branch(0x0005705B), ("nds.bbc", 10, 0, 0))
        self.assertEqual(andes_branch(0x08875C5B), ("nds.beqc", 14, 8, 0x98))
        self.assertEqual(andes_branch(0x4005505B), ("nds.beqc", 10, 64, 0))
        self.assertEqual(andes_branch(0x00555413), None)  # ordinary instruction


class LogContainer(unittest.TestCase):
    @unittest.skipUnless((ROOT / 'evidence/logs/2026-10-25-0851/logcat.encrypted').is_file(), 'local device capture required')
    def test_real_export_passes_full_crc_and_size(self):
        raw = (ROOT / "evidence/logs/2026-10-25-0851/logcat.encrypted").read_bytes()
        archive, declared = unwrap(decrypt(raw))
        self.assertEqual(declared, 25421)
        plain = gzip.decompress(archive)  # Verifies CRC32 and uncompressed size.
        self.assertEqual(len(plain), 170868)
        self.assertEqual(hashlib.sha256(plain).hexdigest(),
                         "87ac31a4ca8dfe27cda8befcb506d939c0cf281afe236ea4169aa4b141b2b730")
        self.assertIn(b"sunxi:sunxi_chips chip is:v821b", plain)
        self.assertIn(b"xt25p1288 (16384 Kbytes)", plain)

    def test_short_export_padding(self):
        archive = gzip.compress(b"small diagnostic example", mtime=0)
        wire = bytearray(RESET_SIZE)
        wire[:len(archive)] = archive
        struct.pack_into("<I", wire, 0x333, len(archive))
        encrypted = bytes(value ^ KEY[(i % RESET_SIZE) % len(KEY)]
                          for i, value in enumerate(wire))
        restored, declared = unwrap(decrypt(encrypted))
        self.assertEqual(declared, len(archive))
        self.assertEqual(gzip.decompress(restored), b"small diagnostic example")

    @unittest.skipUnless((ROOT / 'evidence/logs/2026-10-25-0851/logcat.encrypted').is_file(), 'local device capture required')
    def test_corruption_is_not_accepted_as_valid(self):
        raw = (ROOT / "evidence/logs/2026-10-25-0851/logcat.encrypted").read_bytes()
        archive, _ = unwrap(decrypt(raw))
        damaged = bytearray(archive)
        damaged[-8] ^= 1  # Corrupt the actual gzip CRC32.
        with self.assertRaises(gzip.BadGzipFile):
            gzip.decompress(damaged)


@unittest.skipUnless((FIRMWARE / '26122515.5234.2-test/decrypted/customer-root/app/lylink').is_file(), 'local vendor corpus required')
class PackedLibraries(unittest.TestCase):
    def test_both_real_packs_and_changed_transport(self):
        contents = []
        for tag in ("26011517.5234.2", "26122515.5234.2-test"):
            raw = (FIRMWARE / tag / "decrypted/customer-root/app/lylink").read_bytes()
            members = unpack(raw)  # All six per-file CRC32 values must pass.
            self.assertEqual(len(members), 6)
            self.assertTrue(all(content.startswith(b"\x7fELF") for _, content, _ in members))
            contents.append({name: content for name, content, _ in members})
        self.assertNotEqual(contents[0]["rcpservice"], contents[1]["rcpservice"])
        self.assertEqual(contents[0]["liblylinkpcm.so"], contents[1]["liblylinkpcm.so"])

    def test_corrupt_member_is_rejected(self):
        raw = bytearray((FIRMWARE / "26011517.5234.2/decrypted/customer-root/app/lylink").read_bytes())
        raw[0xD933 + 1000] ^= 0x10
        with self.assertRaises((ValueError, zlib.error)):
            unpack(bytes(raw))


if __name__ == "__main__":
    unittest.main()

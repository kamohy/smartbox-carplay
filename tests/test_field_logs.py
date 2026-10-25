import gzip
from pathlib import Path
import tempfile
import unittest
from tools.analyze_field_logs import analyze

class FieldLogs(unittest.TestCase):
    def test_overlaps_modes_units_and_music_are_kept_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            body=('01-01 00:00:36.780 444 470 D linkapp : AudioPlayerCreate sampleRate: 16000 , sampleSize: 16,channels 1,audioType : 8 , hasInput 1\n'
                '01-01 00:00:36.780 149 184 D rcpp : AudioPlayerCreate 983 :sampleRate:8000,sampleSize:16,Channel:1,audioType:8,hasInput:1\n'
                '01-01 00:00:36.832 149 184 E rcpp : CMainAudioServer start playerType=8,audiomode=3\n'
                '01-01 00:00:38.000 149 431 D rcpp : _HUSampleRateCB, samplerate = 8000.000000\n'
                '01-01 00:00:39.000 444 449 D linkapp : HidClient mic times = 1, rate = 8000kHz -> 16000kHz\n'
                '01-01 00:00:40.000 149 184 D rcpp : AudioPlayerCreate 983 :sampleRate:48000,sampleSize:16,Channel:2,audioType:64,hasInput:0\n'
                '01-01 00:00:42.000 149 431 D rcpp : _HUSampleRateCB, samplerate = 48000.000000\n')
            paths=[]
            for name,boot in [('a',5),('b',5),('c',6)]:
                path=root/(name+'.gz');path.write_bytes(gzip.compress((f'Bad-Hippo persistent system log 0.7.0\nBoot counter: {boot}\n'+body).encode()));paths.append(path)
            report=analyze(paths);self.assertEqual(len(report['boots']),2)
            boot=report['boots'][0]
            self.assertEqual(len(boot['phone_request_events']),1)
            self.assertEqual(len(boot['usb_phone_start_events']),1)
            self.assertEqual(boot['modes_observed'],[3])
            self.assertEqual(boot['microphone_conversions'][0]['from_hz'],8000)
            self.assertEqual(boot['microphone_conversions'][0]['to_hz'],16000)
            self.assertEqual(boot['clock_hz_after_phone_start_min_max'],[8000,8000])
    def test_corrupt_archive_and_non_snapshot_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'bad.gz';data=bytearray(gzip.compress(b'Bad-Hippo persistent system log 0.7.0\nBoot counter: 1\n'));data[-8]^=1;path.write_bytes(data)
            with self.assertRaises((gzip.BadGzipFile,EOFError)):analyze([path])
            path=Path(directory)/'index.txt';path.write_bytes(b'<html>wrong endpoint</html>')
            with self.assertRaises(ValueError):analyze([path])

if __name__=='__main__':unittest.main()

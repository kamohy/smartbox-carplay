import unittest
from email.parser import BytesParser
from email.policy import default
from tools.upload_ui_candidate import multipart

class FirmwareMultipart(unittest.TestCase):
    def test_binary_payload_roundtrips_through_standard_mime_parser(self):
        data=bytes(range(256))*4096+b'\r\n\x00\xff'
        body=multipart(data,'SmartBoxBoundary1234')
        message=BytesParser(policy=default).parsebytes(
            b'MIME-Version: 1.0\r\nContent-Type: multipart/form-data; boundary=SmartBoxBoundary1234\r\n\r\n'+body)
        parts=list(message.iter_parts())
        self.assertEqual(len(parts),1)
        self.assertEqual(parts[0].get_param('name',header='content-disposition'),'file')
        self.assertEqual(parts[0].get_filename(),'blob')
        self.assertEqual(parts[0].get_payload(decode=True),data)
    def test_header_injection_rejected(self):
        with self.assertRaises(ValueError):multipart(b'data','bad\r\nInjected: yes')

if __name__=='__main__':unittest.main()

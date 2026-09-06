import struct
import tempfile
from pathlib import Path
import unittest
from unittest.mock import patch
from inspect_gfx_ownership import inspect


class OwnershipTests(unittest.TestCase):
    def sample(self, rsp=0, rdp=False, queued=False, queued2=False, bad=None):
        with tempfile.TemporaryDirectory(prefix='pd-owner-fixture-') as temporary:
            root = Path(temporary)
            ram = bytearray(0x800000)
            layout = [0x50444746,1,0xa8,88,0x88,0x8c,0x80,0x84,4,16,1,2]
            def word(address, value):
                struct.pack_into('<I',ram,address & 0x7fffff,value)
            for offset, value in ((0x88,rsp),(0x8c,rdp),(0x80,queued),(0x84,queued2)):
                word(0x80001000+offset,0x80002000 if value else 0)
            word(0x80002010,rsp or 1)
            word(0x80002004,3)
            if bad=='pointer': word(0x80001088,0x807ffffd)
            if bad=='offset': layout[4]=0xa8
            if bad=='types': layout[11]=1
            if bad=='magic': layout[0]=0
            if bad=='size': ram=ram[:-1]
            (root/'ram').write_bytes(ram)
            (root/'layout').write_bytes(struct.pack('>12I',*layout))
            class FakeElf:
                data=b'fixture'
                symbols={'g_Sched':(0x80001000,0xa8 if bad!='abi' else 0xa4)}
            with patch('inspect_gfx_ownership.Elf32',return_value=FakeElf()):
                return inspect('elf',root/'ram',root/'layout')

    def test_all_queue_combinations(self):
        for rsp in (0,1,2,99):
            for rdp in (False,True):
                for queued in (False,True):
                    for queued2 in (False,True):
                        with self.subTest(rsp=rsp,rdp=rdp,queued=queued,queued2=queued2):
                            report=self.sample(rsp,rdp,queued,queued2)
                            self.assertEqual(report['graphics_idle'],rsp in (0,2) and not(rdp or queued or queued2))
                            self.assertFalse(report['hardware_verified'])

    def test_reject_invalid_or_mismatched_data(self):
        for bad in ('pointer','offset','types','magic','size','abi'):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.sample(bad=bad)


if __name__=='__main__':
    unittest.main()

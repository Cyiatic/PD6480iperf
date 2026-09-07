import struct
import unittest
from inspect_event_drops import decode


class DropTests(unittest.TestCase):
    def fixture(self):
        class Elf:
            data = b'diagnostic fixture'
            symbols = dict(g_PdEventDropTrace=(0x80000100, 80), send_mesg=(0x80001000, 0),
                           pdTraceDroppedEvent=(0x80002000, 0), pdTraceDroppedEventEnd=(0x8000204c, 0))
            def read(self, address, length):
                return bytes.fromhex('240c0001') * (length // 4)
        elf, ram = Elf(), bytearray(0x800000)
        for address, length in ((0x1000, 48), (0x2000, 76)):
            ram[address:address + length] = bytes.fromhex('01000c24') * (length // 4)
        return elf, ram

    def test_zero_and_all_event_indices(self):
        elf, ram = self.fixture()
        self.assertIsNone(decode(elf, ram)['last_drop'])
        for event in range(16):
            struct.pack_into('<I', ram, 0x100 + event * 4, event + 1)
            struct.pack_into('<4I', ram, 0x140, event, 0x80003000, 0x80004000, 123)
            report = decode(elf, ram)
            self.assertEqual(report['counters'][event], event + 1)
            self.assertEqual(report['last_drop']['event'], event)
            self.assertFalse(report['hardware_verified'])
        self.assertEqual(report['sp_drops'], 5)
        self.assertEqual(report['dp_drops'], 10)

    def test_reject_foreign_or_malformed_evidence(self):
        for bad in ('ram_size', 'abi', 'pointer', 'code', 'event', 'symbol', 'span'):
            with self.subTest(bad=bad):
                elf, ram = self.fixture()
                if bad == 'ram_size': ram.pop()
                if bad == 'abi': elf.symbols['g_PdEventDropTrace'] = (0x80000100, 76)
                if bad == 'pointer': elf.symbols['g_PdEventDropTrace'] = (0x807ffffc, 80)
                if bad == 'code': ram[0x2000] ^= 1
                if bad == 'event':
                    struct.pack_into('<I', ram, 0x110, 1)
                    struct.pack_into('<I', ram, 0x140, 16)
                if bad == 'symbol': del elf.symbols['pdTraceDroppedEvent']
                if bad == 'span': elf.symbols['pdTraceDroppedEventEnd'] = (0x80002050, 0)
                with self.assertRaises(ValueError): decode(elf, ram)


if __name__ == '__main__': unittest.main()

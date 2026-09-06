import struct
import unittest
from unittest.mock import patch

from audit_480i_elf import audit, first_allocation_argument


class FixtureElf:
    def __init__(self, depth=614464, colour=1228864, height=480):
        self.symbols = {"mempAlloc": (0x80001000, 4)}
        self.blocks = {}
        for index, (name, size) in enumerate((("viReset", colour), ("mblurAllocate", depth))):
            address = 0x80002000 + index * 0x100
            # Argument's low half is in the call delay slot.
            words = (0x3c040000 | (size >> 16), 0x0c000400, 0x34840000 | (size & 65535))
            self.blocks[address] = struct.pack(">3I", *words)
            self.symbols[name] = (address, 12)
        mode = struct.pack(">3i", 640, height, 640) + bytes(32)
        self.modes = mode * 2

    def read(self, address, size):
        return self.blocks[address][:size]

    def symbol_data(self, name):
        if name != "g_ViModes":
            raise KeyError(name)
        return self.modes


class AllocationGateTests(unittest.TestCase):
    def check_fixture(self, fixture):
        with patch("audit_480i_elf.Elf32", return_value=fixture):
            return audit("fixture")

    def test_full_buffers_pass(self):
        result = self.check_fixture(FixtureElf())
        self.assertEqual(result["depth_allocation_bytes"], 614464)
        self.assertFalse(result["hardware_verified"])

    def test_old_220_line_depth_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Undersized depth"):
            self.check_fixture(FixtureElf(depth=640 * 220 * 2 + 64))

    def test_old_coop_colour_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Undersized double colour"):
            self.check_fixture(FixtureElf(colour=320 * 220 * 2 * 2 + 64))

    def test_low_vertical_resolution_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "not both 640x480"):
            self.check_fixture(FixtureElf(height=220))

    def test_unknown_argument_is_rejected(self):
        fixture = FixtureElf()
        fixture.blocks[0x80002100] = struct.pack(">3I", 0, 0x0c000400, 0)
        with self.assertRaisesRegex(ValueError, "Cannot prove"):
            first_allocation_argument(fixture, "mblurAllocate")


if __name__ == "__main__":
    unittest.main()

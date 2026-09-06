"""Check fixed-480i tables and allocation arguments in a linked N64 ELF.

This is a build regression gate, not an emulator or hardware-boot test.
It intentionally rejects unknown allocation instruction sequences.
"""
import argparse
import json
from pathlib import Path
import struct


class Elf32:
    def __init__(self, path):
        self.data = Path(path).read_bytes()
        if self.data[:7] != b"\x7fELF\x01\x02\x01":
            raise ValueError("Expected big-endian ELF32")
        offset = struct.unpack_from(">I", self.data, 32)[0]
        stride, count = struct.unpack_from(">HH", self.data, 46)
        self.sections = [struct.unpack_from(">10I", self.data, offset + i * stride)
                         for i in range(count)]
        self.symbols = {}
        for section in self.sections:
            if section[1] != 2:
                continue
            strings = self.section_data(self.sections[section[6]])
            for pos in range(section[4], section[4] + section[5], section[9]):
                name, addr, size, _, _, index = struct.unpack_from(">IIIBBH", self.data, pos)
                name = strings[name:].split(b"\0", 1)[0].decode()
                if name and index:
                    self.symbols[name] = (addr, size)

    def section_data(self, section):
        return self.data[section[4]:section[4] + section[5]]

    def read(self, address, size):
        for section in self.sections:
            if section[1] != 8 and section[3] <= address and address + size <= section[3] + section[5]:
                offset = section[4] + address - section[3]
                return self.data[offset:offset + size]
        raise ValueError(f"Address is not backed by ELF bytes: {address:#x}")

    def symbol_data(self, name):
        return self.read(*self.symbols[name])


def first_allocation_argument(elf, name):
    """Track immediate constants through the first mempAlloc call/delay slot.

    This small scanner is specific to the GCC-built allocation routines, which
    put a fixed byte count in a0. It is not general control-flow execution.
    """
    address, size = elf.symbols[name]
    words = struct.unpack(f">{size // 4}I", elf.read(address, size))
    target = elf.symbols["mempAlloc"][0]
    regs = [None] * 32
    regs[0] = 0

    def step(word):
        op, rs, rt, imm = word >> 26, (word >> 21) & 31, (word >> 16) & 31, word & 65535
        if op == 15:
            regs[rt] = imm << 16
        elif op in (9, 13):
            if regs[rs] is None:
                regs[rt] = None
            elif op == 13:
                regs[rt] = regs[rs] | imm
            else:
                signed = imm if imm < 32768 else imm - 65536
                regs[rt] = (regs[rs] + signed) & 0xffffffff
        elif op in (32, 33, 35, 36, 37):
            regs[rt] = None
        elif op == 0 and word != 0:
            rd = (word >> 11) & 31
            regs[rd] = None
        regs[0] = 0

    for index, word in enumerate(words):
        if word >> 26 == 3:
            call = ((address + index * 4 + 4) & 0xf0000000) | ((word & 0x3ffffff) << 2)
            if call == target:
                step(words[index + 1])
                if regs[4] is None:
                    raise ValueError(f"Cannot prove allocation size in {name}")
                return regs[4]
            # Calls can clobber argument/value/temp registers.
            for reg in range(2, 16):
                regs[reg] = None
        else:
            step(word)
    raise ValueError(f"No mempAlloc call found in {name}")


def audit(path):
    elf = Elf32(path)
    modes = elf.symbol_data("g_ViModes")
    dimensions = [struct.unpack_from(">3i", modes, index * 44) for index in range(2)]
    if dimensions != [(640, 480, 640), (640, 480, 640)]:
        raise ValueError(f"Gameplay modes are not both 640x480: {dimensions}")
    color = first_allocation_argument(elf, "viReset")
    depth = first_allocation_argument(elf, "mblurAllocate")
    if color < 640 * 480 * 2 * 2 + 64:
        raise ValueError(f"Undersized double colour buffer: {color}")
    if depth < 640 * 480 * 2 + 64:
        raise ValueError(f"Undersized depth buffer: {depth}")
    return {"gameplay_modes": dimensions, "colour_allocation_bytes": color,
            "depth_allocation_bytes": depth, "hardware_verified": False}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("elf")
    print(json.dumps(audit(parser.parse_args().elf), indent=2))

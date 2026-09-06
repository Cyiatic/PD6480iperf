"""Read scheduler/thread state from an NTSC-final word-swapped emulator dump."""
import argparse
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_480i_elf import Elf32


def inspect(elf_path, ram_path):
    elf = Elf32(elf_path)
    ram = Path(ram_path).read_bytes()
    if len(ram) != 0x800000 or elf.symbols['g_Sched'][1] != 0x9c:
        raise ValueError('Unsupported RAM or scheduler ABI')
    if elf.symbols['g_MainThread'][1] != 0x238:
        raise ValueError('Unsupported thread ABI')

    def word(address):
        return struct.unpack_from('<I', ram, address & 0x7fffff)[0]

    def half(address):
        return struct.unpack_from('<H', ram, (address & 0x7fffff) ^ 2)[0]

    def symbol(value):
        matches = [(name, value - address) for name, (address, size) in elf.symbols.items()
                   if address <= value < address + size]
        return matches[:5]

    def thread(address):
        return {'address': hex(address), 'state': half(address + 16),
                'flags': half(address + 18), 'id': word(address + 20),
                'saved_pc': hex(word(address + 0x11c)),
                'pc_symbol': symbol(word(address + 0x11c)),
                'cause': hex(word(address + 0x120)),
                'badvaddr': hex(word(address + 0x124)),
                'ra': hex(word(address + 0x104)),
                'ra_symbol': symbol(word(address + 0x104)),
                'a0': hex(word(address + 0x3c)),
                's0': hex(word(address + 0x9c))}

    result = {'hardware_verified': False, 'scheduler': {}, 'threads': {}}
    base = elf.symbols['g_Sched'][0]
    for name, offset in [('next_audio', 0x7c), ('next_gfx', 0x80), ('next_gfx2', 0x84),
                         ('current_rsp', 0x88), ('current_rdp', 0x8c)]:
        pointer = word(base + offset)
        result['scheduler'][name] = {'address': hex(pointer)}
        if 0x80000000 <= pointer < 0x80800000 - 88:
            result['scheduler'][name].update(state=hex(word(pointer + 4)),
                                            type=word(pointer + 16))
    for name in ('g_MainThread', 'g_SchedThread', 'g_IdleThread'):
        result['threads'][name] = thread(elf.symbols[name][0])
    fault = word(elf.symbols['__osFaultedThread'][0])
    result['faulted_thread'] = thread(fault) if 0x80000000 <= fault < 0x80800000 - 0x238 else hex(fault)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf', type=Path)
    parser.add_argument('ram', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.elf, args.ram), indent=2))

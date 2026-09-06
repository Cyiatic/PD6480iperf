"""Compare persistent portal-distance tables from two matching ELF/RDRAM pairs."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from audit_480i_elf import Elf32


def table(elf_path, ram_path):
    elf, ram = Elf32(elf_path), Path(ram_path).read_bytes()
    def word(address):
        return struct.unpack_from('<I', ram, address & 0x7fffff)[0]
    def address(name):
        return elf.symbols[name][0]
    count = word(address('g_NumPortals'))
    rows = word(address('var80061430'))
    if not 0 < count < 1024 or not 0x80000000 <= rows < 0x80800000 - count * 4:
        raise ValueError('Invalid portal table')
    values = []
    for i in range(1, count):
        row = word(rows + i * 4)
        if not 0x80000000 <= row < 0x80800000 - i * 2:
            raise ValueError('Invalid row')
        for j in range(i):
            values.append(struct.unpack_from('<H', ram, ((row + 2 * j) & 0x7fffff) ^ 2)[0])
    return word(address('g_StageNum')), count, values


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('old_elf', 'old_ram', 'new_elf', 'new_ram'):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    old = table(args.old_elf, args.old_ram)
    new = table(args.new_elf, args.new_ram)
    if old != new:
        raise ValueError('Portal stage/count/values differ')
    encoded = struct.pack(f'>{len(new[2])}H', *new[2])
    print(json.dumps({'identical': True, 'stage': new[0], 'portals': new[1],
                     'pair_distances': len(new[2]),
                     'sha256': hashlib.sha256(encoded).hexdigest()}))

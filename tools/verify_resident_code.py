"""Compare key resident functions against an ELF in word-swapped emulator RAM.

This detects common cross-build state mistakes, not every possible difference
between ROMs. A state file and its RAM sidecar must still share provenance.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
from audit_480i_elf import Elf32


def verify(elf_path, ram_path):
    elf = Elf32(elf_path)
    ram = Path(ram_path).read_bytes()
    if len(ram) != 8 * 1024 * 1024:
        raise ValueError('Expected an 8 MiB word-swapped RDRAM snapshot')
    names = ['mainLoop', 'memaReset', 'memaAlloc', 'func0f004c6c', 'viReset']
    if 'memaAppendBank' in elf.symbols:
        names.append('memaAppendBank')
    # Later candidates change scheduler code without changing mainLoop's bytes.
    # Include available scheduler handlers so old states cannot hide that delta.
    names.extend(name for name in ('__scExec', '__scTryDispatch', '__scHandleRSP',
                                  '__scHandleRDP', 'mainInit') if name in elf.symbols)
    hashes = {}
    for name in names:
        address, size = elf.symbols[name]
        if not size or size % 4 or address % 4 or not 0x80000000 <= address <= 0x80800000 - size:
            raise ValueError(f'Invalid resident function: {name}')
        expected = elf.symbol_data(name)
        words = struct.unpack_from(f'<{size // 4}I', ram, address & 0x7fffff)
        actual = struct.pack(f'>{size // 4}I', *words)
        if actual != expected:
            raise ValueError(f'Resident code mismatch: {name}; do not mix states and builds')
        hashes[name] = hashlib.sha256(actual).hexdigest()
    return hashes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf', type=Path)
    parser.add_argument('ram', type=Path)
    args = parser.parse_args()
    print(json.dumps({'resident_code_matches': True,
                      'functions': verify(args.elf, args.ram)}, indent=2))

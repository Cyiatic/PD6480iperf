"""Audit PD N64 ROM file-table compressed assets without trusting a build map.

Usage: python tools/audit_rom_assets.py ROM [ROM ...]
Read-only. Output is JSON. Exit 1 if a nonempty compressed asset is invalid.
The detector targets the 2013-file stock NTSC-final table used by this project.
"""
import argparse
import hashlib
import json
import struct
import zlib
from pathlib import Path

FILE_COUNT = 0x7DE  # Includes the null file; one additional table entry is EOF.


def find_table(rom):
    candidates = []
    position = 0x3052
    while (position := rom.find(b'\x11\x73', position, 0x100000)) != -1:
        expected = int.from_bytes(rom[position+2:position+5], 'big')
        if 0x10000 <= expected <= 0x100000:
            try:
                blob = zlib.decompress(rom[position+5:], -15)
            except zlib.error:
                position += 2
                continue
            if len(blob) == expected:
                words = struct.unpack('>' + 'I'*(len(blob)//4), blob[:len(blob)//4*4])
                for i in range(0, len(words)-FILE_COUNT):
                    if words[i] != 0 or not 0x80000 <= words[i+1] < len(rom):
                        continue
                    table = words[i:i+FILE_COUNT+1]
                    if all(0x80000 <= lo <= hi <= len(rom) and lo % 16 == hi % 16 == 0
                           for lo, hi in zip(table[1:-1], table[2:])):
                        candidates.append((position, i*4, table))
        position += 2
    if len(candidates) != 1:
        raise ValueError(f'Expected one NTSC-final table; found {len(candidates)}')
    return candidates[0]


def audit(path):
    rom = Path(path).read_bytes()
    if rom[:4] != bytes.fromhex('80371240'):
        raise ValueError('Expected big-endian .z64')
    data_offset, table_offset, table = find_table(rom)
    invalid, valid, raw, empty = [], 0, 0, 0
    for fileid in range(1, FILE_COUNT):
        begin, end = table[fileid:fileid+2]
        if begin == end:
            empty += 1
            continue
        if rom[begin:begin+2] != b'\x11\x73':
            raw += 1
            continue
        expected = int.from_bytes(rom[begin+2:begin+5], 'big')
        error = None
        if not 0 < expected <= 0x800000:
            error = 'Implausible uncompressed length'
        else:
            try:
                inflater = zlib.decompressobj(-15)
                body = inflater.decompress(rom[begin+5:end], expected+1)
                if not inflater.eof or len(body) != expected:
                    error = f'Truncated/wrong size: wanted {expected}, got {len(body)}'
            except zlib.error as exc:
                error = str(exc)
        if error:
            invalid.append({'file_id': hex(fileid), 'rom_offset': hex(begin),
                            'rom_bytes': end-begin, 'expected_bytes': expected,
                            'header': rom[begin:begin+16].hex(), 'error': error})
        else:
            valid += 1
    lo, hi = table[0x560:0x562]
    return {'rom': str(path), 'sha256': hashlib.sha256(rom).hexdigest(),
            'data_stream_offset': hex(data_offset), 'file_table_offset_in_data': hex(table_offset),
            'compressed_valid': valid, 'compressed_invalid': len(invalid),
            'raw_unchecked': raw, 'empty_aliases': empty,
            'rare_logo': {'file_id': '0x560', 'rom_offset': hex(lo), 'rom_bytes': hi-lo,
                          'header': rom[lo:lo+16].hex()},
            'invalid_examples': invalid[:12]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('roms', nargs='+', type=Path)
    args = parser.parse_args()
    reports = [audit(path) for path in args.roms]
    print(json.dumps(reports, indent=2))
    raise SystemExit(int(any(report['compressed_invalid'] for report in reports)))


if __name__ == '__main__':
    main()

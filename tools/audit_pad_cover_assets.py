"""Audit cover counts in the exact ROM's performance-format pad assets.

Requires this source tree's files.h for NTSC-final file IDs. This is a structural
asset check, not a hardware test or a general validator for stock packed pads.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import zlib
from audit_rom_assets import find_table


def cover_bounds(data):
    if len(data) < 20:
        raise ValueError('Pad header truncated')
    _, count, _, _, offset = struct.unpack_from('>5I', data)
    padding = len(data) - offset - count * 28
    if not 20 <= offset <= len(data) or not 0 <= padding < 16:
        raise ValueError(f'Cover count/bounds mismatch: count={count}, offset={offset:#x}, bytes={len(data)}')
    return count


def audit(rom_path, files_header):
    rom = Path(rom_path).read_bytes()
    _, _, table = find_table(rom)
    ids = re.findall(r'^#define\s+(FILE_BG_\w+_PADS)\s+(0x[0-9a-fA-F]+)\s*$',
                     Path(files_header).read_text(), re.M)
    if not ids:
        raise ValueError('No pad file IDs')
    invalid, valid = [], {}
    for name, number in ids:
        index = int(number, 16)
        start, end = table[index:index + 2]
        try:
            if rom[start:start + 2] != b'\x11\x73':
                raise ValueError('Expected compressed pad asset')
            expected = int.from_bytes(rom[start + 2:start + 5], 'big')
            if not 20 <= expected <= 0x800000:
                raise ValueError('Invalid inflated length')
            decoder = zlib.decompressobj(-15)
            data = decoder.decompress(rom[start + 5:end], expected + 1)
            if not decoder.eof or len(data) != expected:
                raise ValueError('Invalid compressed stream/length')
            valid[name] = cover_bounds(data)
        except (ValueError, zlib.error) as error:
            invalid.append({'file': name, 'file_id': number, 'error': str(error)})
    return {'rom_sha256': hashlib.sha256(rom).hexdigest(), 'valid': len(valid),
            'cover_counts': valid, 'invalid': invalid}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('rom', type=Path)
    parser.add_argument('files_header', type=Path)
    args = parser.parse_args()
    result = audit(args.rom, args.files_header)
    print(json.dumps(result, indent=2))
    raise SystemExit(int(bool(result['invalid'])))

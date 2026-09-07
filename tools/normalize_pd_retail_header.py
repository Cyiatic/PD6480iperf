"""Create a new retail-ID USA1.1 ROM from the authenticated ED-header build.

Changes only cartridge ID/version header bytes, outside the N64 CRC range.
Does not alter code/assets, calculate CRCs, or overwrite either input/output.
"""
import argparse
import hashlib
import json
from pathlib import Path


def normalize(data, expected_sha256):
    if hashlib.sha256(data).hexdigest() != expected_sha256.lower():
        raise ValueError('Source hash mismatch')
    if len(data) != 33554432 or data[:4] != bytes.fromhex('80371240'):
        raise ValueError('Expected a big-endian 32 MiB N64 ROM')
    if data[0x3b:0x40] != b'NEDE\x20':
        raise ValueError('Expected the current ED/16K EEPROM source header')
    result = bytearray(data)
    result[0x3c], result[0x3f] = ord('P'), 1
    assert result[0x3b:0x40] == b'NPDE\x01'
    assert result[0x40:] == data[0x40:]
    assert [i for i in range(64) if result[i] != data[i]] == [0x3c, 0x3f]
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--source-sha256', required=True)
    args = parser.parse_args()
    data = normalize(args.source.read_bytes(), args.source_sha256)
    with args.output.open('xb') as output:
        output.write(data)
    print(json.dumps(dict(source_sha256=args.source_sha256, output_sha256=hashlib.sha256(data).hexdigest(),
                         changed_offsets=['0x3c','0x3f'], body_identical=True, hardware_verified=False),indent=2))

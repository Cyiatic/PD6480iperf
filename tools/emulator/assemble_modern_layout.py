"""Join cross-compiled v6 layout/probe sections; refuses to overwrite a layout."""
import argparse
from pathlib import Path
import struct


def assemble(header, probes):
    if len(header) != 73 * 4 or struct.unpack_from('>2I', header) != (0x50443831, 6):
        raise ValueError('Expected exact v6 compiled header')
    size = struct.unpack_from('>I', header, len(header) - 4)[0]
    if not 4 <= size <= 128 or len(probes) != size * 2:
        raise ValueError('Expected two complete mission configuration probes')
    return header + probes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('header', 'probes', 'output'):
        parser.add_argument(name, type=Path)
    args = parser.parse_args()
    data = assemble(args.header.read_bytes(), args.probes.read_bytes())
    with args.output.open('xb') as output:
        output.write(data)

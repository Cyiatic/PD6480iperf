"""Read diagnostic event-drop counters; never repair, retry or clear events."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_480i_elf import Elf32


def decode(elf, ram):
    if len(ram) != 0x800000:
        raise ValueError('Expected exactly 8 MiB of word-swapped RDRAM')
    required = ('g_PdEventDropTrace', 'send_mesg', 'pdTraceDroppedEvent', 'pdTraceDroppedEventEnd')
    if any(name not in elf.symbols for name in required):
        raise ValueError('Not the event-drop diagnostic ELF')
    base, size = elf.symbols['g_PdEventDropTrace']
    if size != 80 or base & 3 or not 0x80000000 <= base <= 0x80800000 - size:
        raise ValueError('Unknown trace ABI/address')
    begin = elf.symbols['pdTraceDroppedEvent'][0]
    end = elf.symbols['pdTraceDroppedEventEnd'][0]
    if end - begin != 76:
        raise ValueError('Unknown diagnostic instruction span')
    for address, length in ((elf.symbols['send_mesg'][0], 48), (begin, end - begin)):
        if address & 3 or not 0x80000000 <= address <= 0x80800000 - length:
            raise ValueError('Code outside KSEG0 RDRAM')
        actual = struct.unpack_from('<' + 'I' * (length // 4), ram, address & 0x7fffff)
        if struct.pack('>' + 'I' * len(actual), *actual) != elf.read(address, length):
            raise ValueError('RAM does not contain the matching diagnostic code')
    words = struct.unpack_from('<20I', ram, base & 0x7fffff)
    counts = words[:16]
    if any(counts) and (words[16] >= 16 or not counts[words[16]]):
        raise ValueError('Invalid last dropped event')
    return dict(hardware_verified=False, instrumented=True, behavior='records existing full-queue discards only',
                rdram_sha256=hashlib.sha256(ram).hexdigest(),
                elf_sha256=hashlib.sha256(elf.data).hexdigest(),
                counters=list(counts), sp_drops=counts[4], vi_drops=counts[7], dp_drops=counts[9],
                last_drop=(dict(event=words[16], queue=hex(words[17]), thread=hex(words[18]),
                                cp0_count=hex(words[19])) if any(counts) else None))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf', type=Path)
    parser.add_argument('ram', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    rendered = json.dumps(decode(Elf32(args.elf), args.ram.read_bytes()), indent=2) + '\n'
    if args.output:
        with args.output.open('x') as output:
            output.write(rendered)
    print(rendered, end='')

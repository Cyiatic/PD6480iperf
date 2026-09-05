"""Build a deterministic stock NTSC Perfect Dark 16-Kbit EEPROM save.

Layout: n64decomp/perfect_dark src/game/{gamefile,bossfile,pak,crc}.c
and src/game/mplayer/mplayer.c. No ROM or existing save is required.
All times/statistics are synthetic completion data, not earned records.
"""
from pathlib import Path
import argparse
import hashlib
import json
import struct

SERIAL = 0xBAA  # Stock EEPROM serial, not a controller-pak serial.
MASK64 = (1 << 64) - 1
DEFAULT_FLAGS = (1, 3, 4, 5, 9, 10, 11, 13, 15, 16, 17, 18, 19,
                 21, 22, 23, 24, 28, 29, 30, 31)
PROGRESS_FLAGS = (0x24, *range(0x29, 0x3B), 0x41, 0x42, 0x43,
                  *range(0x47, 0x4C))
# All timed cheats in stock NTSC-final: (stage index, difficulty, seconds).
CHEAT_TARGETS = ((2, 0, 123), (5, 0, 100), (8, 0, 230), (16, 2, 331),
                 (12, 1, 427), (9, 1, 191), (11, 0, 170), (13, 2, 447),
                 (14, 0, 105), (7, 2, 479), (10, 2, 235), (0, 1, 90),
                 (1, 2, 390), (6, 1, 300), (3, 1, 150), (15, 1, 317),
                 (4, 2, 120))


class Bits:
    def __init__(self):
        self.bits = []

    def put(self, value, width):
        if not 0 <= value < (1 << width):
            raise ValueError((value, width))
        self.bits.extend((value >> i) & 1 for i in range(width - 1, -1, -1))

    def name(self, name):
        for value in name.encode('ascii').ljust(10, b'\0'):
            self.put(value, 8)

    def finish(self, length):
        if len(self.bits) > length * 8:
            raise ValueError('Save body overflow')
        bits = self.bits + [0] * (length * 8 - len(self.bits))
        return bytes(sum(bits[i + j] << (7-j) for j in range(8))
                     for i in range(0, len(bits), 8))


def checksum(data):
    seed, salt = 0x8F809F473108B3C1, 0
    sums = []
    for order, increment in ((data, 7), (reversed(data), 3)):
        value = 0
        for byte in order:
            seed = (seed + (byte << (salt & 15))) & MASK64
            seed = ((((seed << 63) & MASK64) >> 31)
                    | (((seed << 31) & MASK64) >> 32)) ^ (((seed << 44) & MASK64) >> 32)
            seed ^= (seed >> 20) & 0xFFF
            value ^= seed & 0xFFFFFFFF
            salt += increment
        sums.append(value & 0xFFFF)
    return struct.pack('>HH', *sums)


def record(kind, bodylen, fileid, body=None, filelen=None):
    occupied = body is not None
    if occupied and len(body) != bodylen:
        raise ValueError('Wrong body length')
    filelen = filelen or ((16 + bodylen + 15) & ~15)
    metadata = struct.pack('>II', (kind << 23) | (bodylen << 12) | filelen,
                           (SERIAL << 19) | (fileid << 12) | (1 << 3)
                           | (int(occupied) << 2) | 2)
    header = checksum(metadata) + (checksum(body) if occupied else b'\xff'*4) + metadata
    return header + (body if occupied else b'\x2b'*bodylen) + b'\0'*(filelen - 16 - bodylen)


def make_game():
    b = Bits()
    b.name('Dark')
    b.put(17, 5)  # Thumbnail zero is Joanna; stage thumbnails are index + 1.
    b.put(24 * 3600, 32)
    b.put(2, 2)
    b.put(16, 5)
    b.put(40, 6)  # Stock volume 0x5000 -> 40.
    b.put(40, 6)
    b.put(1, 2)  # Stereo.
    b.put(0, 3)  # 1.1 controls, both players.
    b.put(0, 3)
    flags = bytearray(10)
    for flag in DEFAULT_FLAGS + PROGRESS_FLAGS:
        flags[flag // 8] |= 1 << (flag % 8)
    assert not flags[0x22 // 8] & (1 << (0x22 % 8))  # Hi-Res OFF.
    for value in flags:
        b.put(value, 8)
    b.put(0, 16)
    times = [[120, 180, 240] for _ in range(21)]
    times[20] = [10, 20, 30]  # The Duel.
    for stage, difficulty, target in CHEAT_TARGETS:
        times[stage][difficulty] = min(times[stage][difficulty], target - 1)
    for row in times:
        for value in row:
            b.put(value, 12)
    for _ in range(30 * 4):
        b.put(1, 1)  # Challenges, all four player counts.
    # Co-op includes the 17 campaign stages and three specials, but not The Duel.
    for _ in range(3):
        b.put((1 << 20) - 1, 21)
    for _ in range(8):
        b.put(255, 8)
    b.put(0, 2)  # 32 stock NTSC-final weapons; unused 33rd score stays clear.
    for _ in range(4):
        b.put(255, 8)  # Other found-weapon bits; mines use flags above.
    return b.finish(0xA0)


def make_boss():
    b = Bits()
    b.put(29, 7)  # Last-selected solo file ID.
    b.put(SERIAL, 13)
    b.put(0, 1)
    b.put(0, 4)  # English.
    for _ in range(8):
        b.name('')  # Default team names.
    b.put(255, 8)  # Random music.
    for _ in range(6):
        b.put(255, 8)
    b.put(0, 1)
    b.put(1, 1)  # Alternate title unlocked, but stock title remains selected.
    b.put(0, 1)
    return b.finish(0x5B)


def make_mp():
    b = Bits()
    b.name('Dark')
    fields = ((1080000, 28), (0, 7), (0, 7), (0, 7), (0, 13), (12, 8),
              (18000, 20), (0, 20), (900, 19), (900, 19), (0, 19),
              (90000, 25), (1000, 10), (900, 26), (0, 26), (900, 20),
              (450000, 30), (900, 18), (900, 18), (900, 18), (900, 16),
              (0, 2), (0x7EE, 12))
    for value, width in fields:
        b.put(value, width)
    for _ in range(120):
        b.put(1, 1)
    b.put(0, 35)  # Primary weapon functions.
    return b.finish(0x4E)


def generate():
    records, fileid = [], 17
    for kind, size, count, first in ((0x10, 0x5B, 2, make_boss()),
                                    (0x20, 0x4E, 5, make_mp()),
                                    (0x40, 0x31, 5, None),
                                    (0x80, 0xA0, 5, make_game())):
        for index in range(count):
            records.append(record(kind, size, fileid, first if index == 0 else None))
            fileid += 1
    image = b''.join(records)
    assert len(image) == 0x7C0
    # Terminator advertises max slot length even at the physical EEPROM end.
    image += record(4, 240, fileid)[:64]
    assert len(image) == 2048
    return image


def validate(image):
    if len(image) != 2048:
        raise ValueError('Expected 2048-byte EEPROM')
    offset, ids, used, counts = 0, set(), [], {}
    while offset < len(image):
        h = image[offset:offset+16]
        if len(h) != 16 or checksum(h[8:]) != h[:4]:
            raise ValueError(f'Header checksum at {offset:#x}')
        a, c = struct.unpack('>II', h[8:])
        kind, length, filelen = a >> 23, (a >> 12) & 2047, a & 4095
        fileid, serial = (c >> 12) & 127, c >> 19
        if fileid in ids or serial != SERIAL or c & 3 != 2:
            raise ValueError('Invalid ID/serial/write/version')
        ids.add(fileid)
        counts[kind] = counts.get(kind, 0) + 1
        if kind == 4:
            assert offset == 0x7C0 and filelen == 256 and not c & 4
            break
        assert filelen % 16 == 0 and filelen >= length + 16
        body = image[offset+16:offset+16+length]
        if c & 4:
            if checksum(body) != h[4:8]:
                raise ValueError(f'Body checksum at {offset:#x}')
            used.append({'type': hex(kind), 'id': fileid, 'offset': hex(offset)})
        elif h[4:8] != b'\xff'*4:
            raise ValueError('Unused record checksum marker')
        offset += filelen
    assert counts == {16: 2, 32: 5, 64: 5, 128: 5, 4: 1}
    assert len(used) == 3
    return {'bytes': len(image), 'sha256': hashlib.sha256(image).hexdigest(),
            'occupied_records': used, 'all_headers_and_occupied_bodies_valid': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    data = generate()
    report = validate(data)
    # Never overwrite an existing save, even on repeat invocation.
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open('xb') as stream:
        stream.write(data)
    assert args.output.read_bytes() == data
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

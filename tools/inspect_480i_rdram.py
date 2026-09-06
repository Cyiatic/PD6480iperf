"""Inspect a matching ELF and ParaLLEl's word-swapped 8 MiB RDRAM dump.

This is an emulator diagnostic, never evidence of console/Analogue gameplay.
"""
import argparse
import json
from pathlib import Path
import struct
from audit_480i_elf import Elf32


def inspect(elf_path, ram_path):
    elf = Elf32(elf_path)
    ram = Path(ram_path).read_bytes()
    if len(ram) != 8 * 1024 * 1024:
        raise ValueError('Expected a full 8 MiB RDRAM dump')
    def addr(name):
        return elf.symbols[name][0]
    def word(address):
        return struct.unpack_from('<I', ram, address & 0x7fffff)[0]
    def byte(address):
        return ram[(address & 0x7fffff) ^ 3]
    def half(address):
        return struct.unpack_from('<h', ram, (address & 0x7fffff) ^ 2)[0]
    back = word(addr('g_ViBackData'))
    report = {
        'stage': word(addr('g_StageNum')),
        'logical_vi_resolution': word(addr('g_ViRes')),
        'hires_option': word(addr('g_HiResEnabled')),
        'oom_marker': byte(addr('g_LvOom')),
        'oom_requested_bytes': word(addr('g_LvOomSize')),
        'eeprom_detected': word(addr('g_PakHasEeprom')),
        'framebuffers': [hex(word(addr('g_FrameBuffers') + n * 4)) for n in range(2)],
        'depth': hex(word(addr('var800844f0'))),
        'active_dimensions': [half(back + 0x18), half(back + 0x1a)],
        'active_framebuffer': hex(word(back + 0x28)),
        'hardware_verified': False,
    }
    if 'var80084014' in elf.symbols:
        report['level_paused'] = bool(word(addr('var80084014')))
    for name in ('g_MempOnboardPools', 'g_MempExpansionPools'):
        pool = addr(name) + 4 * 20  # MEMPOOL_STAGE, sizeof(memorypool)
        report[name] = {'left': hex(word(pool + 4)), 'right': hex(word(pool + 8)),
                        'free_bytes': word(pool + 8) - word(pool + 4)}
    # GCC NTSC-final ABI, measured with sizeof/offsetof in memory_layout.c.
    # Do not trust the older offset comments in types.h (several are stale).
    if elf.symbols['g_Vars'][1] == 0x504:
        variables = addr('g_Vars')
        report['level_frame_number'] = word(variables + 0x0c)
        report['tick_mode'] = word(variables + 0x2ac)
        report['in_cutscene'] = word(variables + 0x4bc)
        player = word(variables + 0x284)
        if 0x80000000 <= player <= 0x80800000 - 0x1c70:
            report['player_pause_mode'] = word(player + 0x1a24)
        count = word(variables + 0x2bc)
        rooms = word(addr('g_Rooms'))
        if 0 < count < 4096 and 0x80000000 <= rooms < 0x80800000 - count * 0x90:
            report['room_count'] = count
            report['loaded_rooms'] = [i for i in range(1, count)
                                      if half(rooms + i * 0x90 + 2)]
            sizes = [(i, word(rooms + i * 0x90 + 0x84)) for i in range(1, count)]
            # Unloaded values are the room's declared initial gfx request;
            # loaded values may have been adjusted after decompression.
            sizes = [(i, size) for i, size in sizes if 0 < size < 0x80000000]
            if sizes:
                room, size = max(sizes, key=lambda entry: entry[1])
                report['largest_room_gfx_request'] = {'room': room, 'bytes': size}
    if elf.symbols['g_MemaHeap'][1] == 0x3fc:
        heap = addr('g_MemaHeap')
        free_sizes = [word(heap + 12 + i * 8 + 4) for i in range(124)]
        report['mema_free_bytes'] = sum(free_sizes)
        report['mema_largest_recorded_free_block'] = max(free_sizes)
        report['mema_reserved_bytes'] = word(addr('g_MainMemaHeapSize'))
    config = addr('g_MissionConfig')
    report['mission_config'] = {'difficulty': byte(config) >> 1,
                                'stage': byte(config + 1),
                                'index': byte(config + 2)}
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf', type=Path)
    parser.add_argument('ram', type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.elf, args.ram), indent=2))

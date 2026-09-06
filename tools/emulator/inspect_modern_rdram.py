"""Inspect newer-core RDRAM using offsets compiled from that source's headers.

Accepts only an 8 MiB word-swapped emulator dump. No hardware claim is made.
Compile modern_memory_layout.c with the candidate flags and objcopy .rodata
to a raw layout file. Do not reuse a different build's state or layout.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_480i_elf import Elf32

KEYS = ('magic version vars_size level_frame tick_mode in_cutscene current_player '
        'room_count player_size player_pause room_size room_gfx room_gfx_length '
        'vi_size vi_width vi_height vi_framebuffer sched_size sched_rsp sched_rdp '
        'thread_size thread_state thread_flags thread_pc thread_cause thread_badva').split()


def inspect(elf_path, ram_path, layout_path):
    elf = Elf32(elf_path)
    ram, layout = Path(ram_path).read_bytes(), Path(layout_path).read_bytes()
    if len(ram) != 0x800000 or len(layout) < 4 * len(KEYS):
        raise ValueError('Wrong RAM or layout size')
    offsets = dict(zip(KEYS, struct.unpack_from('>' + 'I' * len(KEYS), layout)))
    if offsets['magic'] != 0x50443831 or offsets['version'] != 1:
        raise ValueError('Wrong layout magic/version')
    for name, key in [('g_Vars', 'vars_size'), ('g_Sched', 'sched_size'),
                      ('g_MainThread', 'thread_size')]:
        if elf.symbols[name][1] != offsets[key]:
            raise ValueError(f'ABI mismatch for {name}')

    def physical(address, size=4):
        if not (0x80000000 <= address <= 0x80800000 - size
                or 0xa0000000 <= address <= 0xa0800000 - size):
            raise ValueError(f'Not a RAM pointer: {address:#x}')
        return address & 0x7fffff

    def word(address):
        return struct.unpack_from('<I', ram, physical(address))[0]

    def half(address):
        return struct.unpack_from('<h', ram, physical(address, 2) ^ 2)[0]

    def byte(address):
        return ram[physical(address, 1) ^ 3]

    def address(name):
        return elf.symbols[name][0]

    # Explicit resident code checks, including modern optimized subsystems.
    hashes = {}
    for name in ('mainInit', 'mainLoop', 'mainProc', '__scExec', '__scTryDispatch',
                 '__scFramebufferAvailable', 'schedSubmitGfxTask', '__scHandleRetrace',
                 '__scHandleRSP', '__scHandleRDP', 'viReset', 'bgPreload',
                 'bgLoadRoom', 'mblurAllocate', 'mblurReset', 'dmaExec',
                 'menuReset', 'menuPushDialog', 'menuRenderModels'):
        if name not in elf.symbols:
            continue
        start, size = elf.symbols[name]
        if not size or size % 4:
            raise ValueError(f'Invalid code symbol: {name}')
        actual = b''.join(ram[i:i + 4][::-1] for i in range(
            physical(start, size), physical(start, size) + size, 4))
        if actual != elf.symbol_data(name):
            raise ValueError(f'Resident code mismatch: {name}')
        hashes[name] = hashlib.sha256(actual).hexdigest()

    variables = address('g_Vars')
    back = word(address('g_ViBackData'))
    result = {
        'hardware_verified': False,
        'elf_sha256': hashlib.sha256(Path(elf_path).read_bytes()).hexdigest(),
        'rdram_sha256': hashlib.sha256(ram).hexdigest(),
        'layout_sha256': hashlib.sha256(layout).hexdigest(),
        'resident_code_hashes': hashes,
        'stage': word(address('g_StageNum')),
        'level_frame_number': word(variables + offsets['level_frame']),
        'tick_mode': word(variables + offsets['tick_mode']),
        'in_cutscene': word(variables + offsets['in_cutscene']),
        'framebuffers': [hex(word(address('g_FrameBuffers') + i * 4))
                        for i in range(elf.symbols['g_FrameBuffers'][1] // 4)],
        'depth': hex(word(address('var800844f0'))),
        'active_dimensions': [half(back + offsets['vi_width']), half(back + offsets['vi_height'])],
        'active_framebuffer': hex(word(back + offsets['vi_framebuffer'])),
        'hires_option': word(address('g_HiResEnabled')),
        'oom_marker': byte(address('g_LvOom')),
        'oom_requested_bytes': word(address('g_LvOomSize')),
        'eeprom_detected': word(address('g_PakHasEeprom')),
    }
    current = word(variables + offsets['current_player'])
    if current:
        result['player_pause_mode'] = word(current + offsets['player_pause'])
    count = word(variables + offsets['room_count'])
    rooms = word(address('g_Rooms'))
    if rooms and 0 < count < 4096:
        physical(rooms, count * offsets['room_size'])
        result['room_count'] = count
        result['loaded_rooms'] = [i for i in range(1, count)
                                  if word(rooms + i * offsets['room_size'] + offsets['room_gfx'])]
    for name in ('g_MempOnboardPools', 'g_MempExpansionPools'):
        if elf.symbols[name][1] != 9 * 20:
            raise ValueError('Unknown memory pool ABI')
        pool = address(name) + 4 * 20
        result[name] = {'left': hex(word(pool + 4)), 'right': hex(word(pool + 8)),
                        'free_bytes': word(pool + 8) - word(pool + 4)}
    result['threads'] = {}
    for name in ('g_MainThread', 'g_SchedThread'):
        start = address(name)
        result['threads'][name] = {key: hex(word(start + offsets['thread_' + key]))
                                   for key in ('pc', 'cause', 'badva')}
        result['threads'][name]['state'] = half(start + offsets['thread_state'])
        result['threads'][name]['flags'] = half(start + offsets['thread_flags'])

    if 'var8008dcc0' in elf.symbols:
        if elf.symbols['var8008dcc0'][1] != 160:
            raise ValueError('Unknown prepared VI mode ABI')
        result['prepared_vi_modes'] = []
        for index in range(2):
            start = address('var8008dcc0') + index * 80
            result['prepared_vi_modes'].append({
                'ctrl': hex(word(start + 4)), 'width': word(start + 8),
                'v_sync': word(start + 16), 'x_scale': word(start + 32),
                'field_origins': [word(start + 40), word(start + 60)],
                'field_y_scales': [word(start + 44), word(start + 64)],
            })

    if 'g_PdAllocTrace' in elf.symbols:
        def caller_name(pointer):
            for name, (start, size) in elf.symbols.items():
                if size and start <= pointer < start + size:
                    return f'{name}+{pointer - start:#x}'
            return hex(pointer)

        count = word(address('g_PdAllocTraceUsed'))
        if count > elf.symbols['g_PdAllocTrace'][1] // 16:
            raise ValueError('Allocation trace count out of bounds')
        result['allocation_trace_note'] = ('Requested bytes, not retained live bytes; '
                                            'subsequent shrinking is not subtracted.')
        result['allocation_trace'] = []
        for index in range(count):
            start = address('g_PdAllocTrace') + index * 16
            caller, calls, requested, largest = [word(start + offset) for offset in range(0, 16, 4)]
            result['allocation_trace'].append(dict(caller=caller_name(caller), calls=calls,
                                                   requested_bytes=requested, largest_request=largest))
        start = address('g_PdAllocFirstFailure')
        result['first_allocation_failure'] = dict(caller=caller_name(word(start)),
                requested_bytes=word(start + 4), last_file=hex(word(start + 8)),
                expansion_free_bytes=word(start + 12))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf', type=Path)
    parser.add_argument('ram', type=Path)
    parser.add_argument('layout', type=Path)
    parser.add_argument('--output', type=Path, help='Write a new JSON evidence file; refuses overwrite')
    args = parser.parse_args()
    rendered = json.dumps(inspect(args.elf, args.ram, args.layout), indent=2) + '\n'
    if args.output:
        with args.output.open('x', encoding='utf-8') as target:
            target.write(rendered)
    print(rendered, end='')

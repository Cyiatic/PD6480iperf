"""Safety/identity checks for the v79 diagnostic, never a release acceptance gate."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_480i_elf import Elf32, audit as audit_video
from inspect_480i_rdram import inspect


def direct_jumps(elf, name):
    address, size = elf.symbols[name]
    targets = []
    for index, (word,) in enumerate(struct.iter_unpack('>I', elf.read(address, size))):
        if word >> 26 in (2, 3):
            targets.append(((address + index * 4 + 4) & 0xf0000000) | ((word & 0x3ffffff) << 2))
        if word >> 26 == 0 and word & 63 == 9:
            raise ValueError(f'Unexpected indirect call in {name}')
    return targets


def audit(path, ram_path=None):
    elf = Elf32(path)
    if elf.symbol_data('__osContRamWrite') != bytes.fromhex('03e0000824020001'):
        raise ValueError('Physical Controller Pak write blocker differs from audited return stub')
    shadow = elf.symbols['pdHwEeprom'][0]
    for name in ('pakReadEeprom', 'pakWriteEeprom'):
        if direct_jumps(elf, name) != [shadow]:
            raise ValueError(f'{name} does not call only the RAM EEPROM shim')
    if direct_jumps(elf, 'pakProbeEeprom') or direct_jumps(elf, 'pdHwEeprom'):
        raise ValueError('Unexpected external calls in diagnostic probe/shadow store')
    seed = elf.symbol_data('g_PdHwEeprom')
    seed_hash = hashlib.sha256(seed).hexdigest()
    if seed_hash != 'fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d':
        raise ValueError('Diagnostic EEPROM seed is not the validated Dark image')
    result = {'diagnostic_only': True, 'elf_sha256': hashlib.sha256(elf.data).hexdigest(),
              'seed_sha256': seed_hash, 'physical_controller_pak_writes_blocked': True,
              'game_eeprom_access_redirected_to_ram': True, 'video': audit_video(path)}
    if ram_path:
        ram = Path(ram_path).read_bytes()
        if len(ram) != 0x800000:
            raise ValueError('Expected completed 8 MiB RAM dump')
        result['snapshot'] = inspect(path, ram_path)
        result['replay'] = {name: (ram[(elf.symbols[name][0] & 0x7fffff) ^ 3]
            if elf.symbols[name][1] == 1 else
            struct.unpack_from('<I', ram, elf.symbols[name][0] & 0x7fffff)[0])
            for name in ('g_PdHwPhase', 'g_PdHwPhaseTicks', 'g_PdHwToggleChecks',
                         'g_PdHwSaveReads', 'g_PdHwSaveWrites', 'g_LvShowStats')}
        state, replay = result['snapshot'], result['replay']
        result['emulator_sequence_completed'] = (
            replay['g_PdHwPhase'] == 8 and replay['g_PdHwToggleChecks'] == 3
            and state['stage'] == 38 and state['hires_option'] == 1
            and state['oom_marker'] == 0 and state['active_dimensions'] == [640, 480]
            and state.get('level_paused') is False and state.get('player_pause_mode') == 0)
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf', type=Path)
    parser.add_argument('--ram', type=Path)
    parser.add_argument('--rom', type=Path)
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = audit(args.elf, args.ram)
    if args.rom:
        result['rom_sha256'] = hashlib.sha256(args.rom.read_bytes()).hexdigest()
    rendered = json.dumps(result, indent=2)
    if args.out:
        with args.out.open('x') as stream:
            stream.write(rendered + '\n')
    print(rendered)

"""Bounded software input tests from a matching-build, unpaused cold-boot seed.

Only the existing control-style/aim-mode settings are instrumented in RAM.
Movement and aiming are real libretro controller input. Never a hardware claim.
"""
import argparse
import json
import math
import os
from pathlib import Path
import struct
import subprocess
import sys


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('distribution', 'host', 'core', 'rom', 'elf', 'seed', 'layout', 'out'):
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    sys.path.insert(0, str(args.distribution / 'tools'))
    from audit_480i_elf import Elf32
    elf = Elf32(args.elf)
    names = ('current_player current_stats mpindex config_size controlmode options '
             'aim prop position theta pitch pause').split()
    layout = dict(zip(names, struct.unpack('>12I', args.layout.read_bytes())))
    args.out.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ)
    env['PATH'] = 'C:/msys64/mingw64/bin;' + env.get('PATH', '')

    def inspect(folder):
        ram = (folder / 'rdram-last.bin').read_bytes()
        assert len(ram) == 0x800000
        def word(addr):
            return struct.unpack_from('<I', ram, addr & 0x7fffff)[0]
        def byte(addr):
            return ram[(addr & 0x7fffff) ^ 3]
        def flt(addr):
            return struct.unpack('<f', struct.pack('<I', word(addr)))[0]
        base = elf.symbols['g_Vars'][0]
        player = word(base + layout['current_player'])
        stats = word(base + layout['current_stats'])
        assert 0x80000000 <= player < 0x80800000
        mpindex = word(stats + layout['mpindex'])
        assert mpindex < 6
        config = elf.symbols['g_PlayerConfigsArray'][0] + mpindex * layout['config_size']
        prop = word(player + layout['prop'])
        result = dict(aim=word(player + layout['aim']), pause=word(player + layout['pause']),
            position=[flt(prop + layout['position'] + i * 4) for i in range(3)],
            theta=flt(player + layout['theta']), pitch=flt(player + layout['pitch']),
            graph=byte(elf.symbols['g_LvShowStats'][0]),
            controlmode=byte(config + layout['controlmode']),
            config=config, control_word=word(config + layout['controlmode']),
            option_word=word(config + layout['options']))
        assert result['pause'] == 0, 'Tests require unpaused gameplay'
        assert result['graph'] == 0, 'FPS graph unexpectedly enabled'
        assert all(math.isfinite(v) for v in result['position'])
        return result

    def run(name, seed, inputs, ticks=60, toggle=False):
        before = inspect(seed)
        folder = args.out / name
        folder.mkdir()
        controls = folder / 'input.txt'
        controls.write_text(inputs)
        config = before['config']
        # Big-endian config byte/halfword, written as aligned emulator u32s.
        control_word = (before['control_word'] & 0x00ffffff) | (1 << 24)
        option_word = before['option_word'] & ~(0x10 << 16)
        if toggle:
            option_word |= 0x10 << 16
        writes = folder / 'settings-only-writes.txt'
        writes.write_text(f"0 {config + layout['controlmode']:08x} {control_word:08x}\n"
                          f"0 {config + layout['options']:08x} {option_word:08x}\n")
        command = [str(args.host.resolve()), str(args.core.resolve()), str(args.rom.resolve()),
            str(folder.resolve()), str(ticks), 'cached_interpreter', str(controls.resolve()),
            str((seed / 'state.bin').resolve()), str((seed / 'save-memory.bin').resolve()),
            'eeprom-header', str(writes.resolve()), '1']
        with (folder / 'host.log').open('x') as log:
            subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT,
                           check=True, timeout=180)
        result = inspect(folder)
        assert result['controlmode'] == 1
        (folder / 'inspection.json').write_text(json.dumps(result, indent=2) + '\n')
        print(name, json.dumps(result), flush=True)
        return folder, result

    seed, initial = run('configured-12', args.seed, '', 60)
    _, idle = run('idle', seed, '')
    movements = {}
    for direction, mask in [('up', 16), ('down', 32), ('left', 64), ('right', 128)]:
        _, result = run('dpad-' + direction, seed, f'0 60 {mask} 0 0\n')
        delta = [a - b for a, b in zip(result['position'], idle['position'])]
        assert sum(x*x for x in delta) > 1, 'D-pad did not move player: ' + direction
        assert abs(result['theta'] - idle['theta']) < 0.1, 'D-pad unexpectedly turned camera'
        movements[direction] = delta
    for a, b in [('up', 'down'), ('left', 'right')]:
        assert sum(x*y for x, y in zip(movements[a], movements[b])) < 0
    held, l_result = run('l-hold', seed, '0 60 1024 0 0\n')
    assert l_result['aim'] == 1
    _, r_result = run('r-hold', seed, '0 60 2048 0 0\n')
    assert r_result['aim'] == 1
    _, released = run('l-released', held, '', 30)
    assert released['aim'] == 0
    toggled, toggle_on = run('l-toggle-on', seed, '0 6 1024 0 0\n', toggle=True)
    assert toggle_on['aim'] == 1
    _, toggle_off = run('l-toggle-off', toggled, '0 6 1024 0 0\n', toggle=True)
    assert toggle_off['aim'] == 0
    _, look_x = run('stick-look-x', seed, '0 60 0 20000 0\n')
    _, look_y = run('stick-look-y', seed, '0 60 0 0 -20000\n')
    assert abs(look_x['theta'] - idle['theta']) > 1
    assert abs(look_y['pitch'] - idle['pitch']) > 1
    report = dict(passed=True, hardware_verified=False, emulator_eeprom_header_adapter=True,
        settings_only_ram_writes=True, controller_style='1.2', controller_ports_tested=[1],
        dpad_movement=movements, l_hold_and_release=True, r_hold=True,
        l_toggle_on_and_off=True, analog_camera_both_axes=True, graph_remained_off=True)
    (args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()

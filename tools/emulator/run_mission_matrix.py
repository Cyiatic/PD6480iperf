"""Exercise normal Accept Mission/level initialization from a matching menu state.

Explicit instrumentation: at tick zero only g_MissionConfig's first word is
changed (Perfect Agent, stage ID/index, solo). Normal controller A then invokes
the game's Accept Mission handler; Start skips the intro. No code or ROM edits.
This does not establish hardware operation, a full playthrough or performance.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_480i_elf import Elf32
from inspect_480i_rdram import inspect
from verify_resident_code import verify as verify_code


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'elf', 'rom', 'state', 'host', 'core', 'out'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--stages', nargs='+', required=True)
    parser.add_argument('--ticks', type=int, default=1500)
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--skip-tick', type=int, default=1000)
    args = parser.parse_args()
    # The host creates state.bin and rdram-last.bin together. Check that
    # sidecar now, then verify the actual restored resident code after each run.
    # Never assume that a state supplied with a new ROM contains the new code.
    verify_code(args.elf, args.state.parent / 'rdram-last.bin')
    if args.out.exists():
        raise ValueError('Use a new output directory; do not overwrite evidence')
    args.out.mkdir(parents=True)
    constants = (args.source / 'src/include/constants.h').read_text()
    defines = {k: int(v, 0) for k, v in re.findall(
        r'^#define\s+((?:SOLOSTAGEINDEX|STAGE)_\w+)\s+(0x[0-9a-fA-F]+|\d+)\s*$',
        constants, re.M)}
    elf = Elf32(args.elf)
    address = elf.symbols['g_MissionConfig'][0]
    rom_hash = hashlib.sha256(args.rom.read_bytes()).hexdigest()
    state_hash = hashlib.sha256(args.state.read_bytes()).hexdigest()
    elf_hash = hashlib.sha256(args.elf.read_bytes()).hexdigest()
    environment = dict(os.environ)
    environment['PATH'] = 'C:/msys64/mingw64/bin;' + environment.get('PATH', '')
    inputs = args.out / 'accept-skip-move.txt'
    inputs.write_text(f'30 40 1 0 0\n{args.skip_tick} {args.skip_tick + 15} 8 0 0\n'
                      f'{args.skip_tick + 400} {args.skip_tick + 550} 0 0 -18000\n')

    def run(name):
        stage = defines['STAGE_' + name]
        index = defines['SOLOSTAGEINDEX_' + name]
        output = args.out / name.lower()
        output.mkdir()
        writes = output / 'selection.txt'
        writes.write_text(f'0 {address:08x} {(4 << 24) | (stage << 16) | (index << 8):08x}\n')
        print('START', name, flush=True)
        command = [str(args.host.resolve()), str(args.core.resolve()), str(args.rom.resolve()),
                   str(output.resolve()), str(args.ticks), 'cached_interpreter',
                   str(inputs.resolve()), str(args.state.resolve()), '-', 'eeprom-header',
                   str(writes.resolve())]
        report = {'requested_stage': name, 'requested_stage_id': stage,
                  'rom_sha256': rom_hash, 'instrumented_menu_selection': True,
                  'source_state_sha256': state_hash, 'elf_sha256': elf_hash,
                  'eeprom_header_adapter': True, 'hardware_verified': False}
        try:
            with (output / 'run.log').open('w') as log:
                result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                        env=environment, timeout=240)
            report['exit_code'] = result.returncode
            if result.returncode == 0:
                report['resident_code_hashes'] = verify_code(args.elf, output / 'rdram-last.bin')
                report['snapshot'] = inspect(args.elf, output / 'rdram-last.bin')
                subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-i',
                    str(output / f'frame-{args.ticks}.ppm'), '-frames:v', '1',
                    str(output / 'final.png')], check=True, env=environment)
                state = report['snapshot']
                report['load_gate_passed'] = (state['stage'] == stage and
                    state['oom_marker'] == 0 and state['active_dimensions'] == [640, 480]
                    and state.get('in_cutscene') == 0 and state.get('tick_mode') == 1
                    and state.get('level_frame_number', 0) > 100)
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError, ValueError) as error:
            report['error'] = str(error)
            report['load_gate_passed'] = False
        (output / 'report.json').write_text(json.dumps(report, indent=2))
        print('DONE', name, json.dumps(report), flush=True)
        return report

    reports = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(run, name.upper()) for name in args.stages]
        for future in as_completed(futures):
            reports.append(future.result())
            (args.out / 'summary.json').write_text(json.dumps(reports, indent=2))
    return 0 if all(r.get('load_gate_passed') for r in reports) else 1


if __name__ == '__main__':
    sys.exit(main())

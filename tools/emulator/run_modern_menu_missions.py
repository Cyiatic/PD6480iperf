"""Bounded normal-ROM mission samples using ordinary menu input only.

Seed must be a matching-build Mission Select state with Defection highlighted.
Each independent run restores that seed, moves DOWN through the stock list,
then uses the real mission/difficulty/Accept handlers via controller A.
No mission-config writes, synthetic ROM patches or foreign-build states.
Results are software load samples, never hardware or full-playthrough proof.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

from inspect_modern_rdram import inspect


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_stages(source):
    menu = (source / 'src/game/mainmenu.c').read_text()
    body = re.search(r'g_StageNames\[NUM_SOLOSTAGES\]\s*=\s*\{(.*?)\n\};', menu, re.S).group(1)
    names = re.findall(r'\{\s*STAGE_(\w+)\s*,', body)
    if len(names) != 21 or len(set(names)) != 21 or names[0] != 'DEFECTION':
        raise ValueError('Unexpected stock mission list')
    constants = (source / 'src/include/constants.h').read_text()
    ids = {name: int(value, 0) for name, value in re.findall(
        r'^#define\s+STAGE_(\w+)\s+(0x[0-9a-fA-F]+|\d+)\s*$', constants, re.M)}
    return [(name, ids[name]) for name in names]


def expected_rooms(source, name, count):
    arrays = {'INFILTRATION': 'Infiltration', 'RESCUE': 'Rescue',
              'ESCAPE': 'Escape', 'MAIANSOS': 'MaianSos'}
    if name not in arrays:
        return set(range(1, count))
    bg = (source / 'src/game/bg.c').read_text()
    body = re.search(r'g_BgPreload' + arrays[name] + r'\[\]\[2\]\s*=\s*\{(.*?)\n\};', bg, re.S).group(1)
    spans = re.findall(r'\{\s*(0x[0-9a-f]+|\d+)\s*,\s*(0x[0-9a-f]+|\d+)\s*\}', body)
    if not spans:
        raise ValueError('Preload table did not parse')
    return {room for lo, hi in spans for room in range(int(lo, 0), int(hi, 0) + 1)
            if 0 < room < count}


def input_sequence(index):
    lines = [f'{30 + i * 45} {36 + i * 45} 0 0 22000' for i in range(index)]
    base = index * 45 + 60
    for start, end, button in [(30, 42, 1), (160, 172, 1), (300, 312, 1),
                               (1050, 1062, 8), (1230, 1242, 8)]:
        lines.append(f'{base + start} {base + end} {button} 0 0')
    return '\n'.join(lines) + '\n', base + 1500


def evaluate_snapshot(snapshot, stage, required):
    missing = sorted(required - set(snapshot.get('loaded_rooms', [])))
    faults = [name for name, thread in snapshot.get('threads', {}).items() if thread['flags']]
    cache = snapshot.get('room_cache')
    room_ready = not missing
    unwarmed = []
    if cache:
        unwarmed = sorted(required - {r['room'] for r in cache.get('rooms',[]) if r['warmed'] == 1})
        room_ready = (cache['mode'] == 3 and cache.get('partition_valid') is True
                      and cache.get('load_failures') == 0 and cache.get('allocator_faults') == 0
                      and not cache.get('missing_visible_rooms') and not unwarmed)
    solo = snapshot.get('mission_configuration') == dict(
        cooperative=False, counteroperative=False, ai_buddies=0)
    passed = bool(required) and solo and (
        snapshot['stage'] == stage and snapshot['oom_marker'] == 0
        and snapshot['active_dimensions'] == [640, 480]
        and snapshot.get('level_frame_number', 0) > 100
        and snapshot.get('tick_mode') == 1 and snapshot.get('in_cutscene') == 0
        and room_ready and not snapshot['rooms_missing_vertex_batches']
        and not faults)
    return dict(expected_preload_rooms=sorted(required), missing_preload_rooms=missing,
                room_policy='budgeted-retained-cache' if cache else 'full-preload',
                unwarmed_required_rooms=unwarmed,
                thread_faults=faults, load_gate_passed=passed,
                unpaused_snapshot=passed and snapshot.get('player_pause_mode') == 0)


def validate_solo_seed(seed):
    configuration = seed.get('mission_configuration')
    if configuration != dict(cooperative=False, counteroperative=False, ai_buddies=0):
        raise ValueError('Compiled v6 solo-mode proof required; co-op/AI-buddy seed rejected')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source', 'elf', 'rom', 'state', 'layout', 'host', 'core', 'out'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--rom-sha256', required=True)
    parser.add_argument('--state-sha256', required=True)
    parser.add_argument('--stages', nargs='+', required=True)
    parser.add_argument('--jobs', type=int, choices=range(1, 5), default=2)
    args = parser.parse_args()
    if digest(args.rom) != args.rom_sha256 or digest(args.state) != args.state_sha256:
        raise ValueError('ROM/state identity mismatch')
    seed = inspect(args.elf, args.state.parent / 'rdram-last.bin', args.layout)
    if seed['stage'] != 38 or seed.get('synthetic_replay_diagnostic'):
        raise ValueError('Expected normal-ROM CI mission-list seed')
    validate_solo_seed(seed)
    if 'rooms_missing_vertex_batches' not in seed:
        raise ValueError('Version3 batch-aware compiled layout required')
    stages = source_stages(args.source)
    selected = set(name.upper() for name in args.stages)
    if not selected.issubset({name for name, _ in stages}):
        raise ValueError('Unknown mission requested')
    args.out.mkdir(parents=True, exist_ok=False)
    metadata = {'rom_sha256': digest(args.rom), 'state_sha256': digest(args.state),
                'elf_sha256': digest(args.elf), 'layout_sha256': digest(args.layout),
                'hardware_verified': False, 'instrumented_menu_selection': False,
                'eeprom_header_adapter': True, 'seed': str(args.state),
                'seed_highlight': 'DEFECTION, visually verified before this run',
                'jobs': args.jobs, 'source_files_sha256': {name: digest(args.source / name)
                    for name in ('src/game/mainmenu.c', 'src/game/bg.c', 'src/include/constants.h')}}
    (args.out / 'run-metadata.json').write_text(json.dumps(metadata, indent=2) + '\n')
    environment = dict(os.environ)
    environment['PATH'] = 'C:/msys64/mingw64/bin;' + environment.get('PATH', '')

    def run(index, name, stage):
        output = args.out / name.lower()
        output.mkdir()
        text, ticks = input_sequence(index)
        inputs = output / 'input.txt'
        inputs.write_text(text)
        report = dict(requested_stage=name, requested_stage_id=stage, menu_index=index,
                      ticks=ticks, load_gate_passed=False, hardware_verified=False,
                      instrumented_menu_selection=False)
        command = [str(args.host.resolve()), str(args.core.resolve()), str(args.rom.resolve()),
                   str(output.resolve()), str(ticks), 'cached_interpreter', str(inputs.resolve()),
                   str(args.state.resolve()), '-', 'eeprom-header']
        print('START', name, 'ordinary-input ticks', ticks, flush=True)
        try:
            with (output / 'host.log').open('x') as log:
                result = subprocess.run(command, stdout=log, stderr=subprocess.STDOUT,
                                        env=environment, timeout=600)
            report['exit_code'] = result.returncode
            if result.returncode != 0:
                raise ValueError(f'Host failed with native exit {result.returncode}')
            subprocess.run(['ffmpeg', '-v', 'error', '-i', str(output / f'frame-{ticks}.ppm'),
                            '-frames:v', '1', str(output / 'final.png')], check=True, env=environment)
            snapshot = inspect(args.elf, output / 'rdram-last.bin', args.layout)
            report['snapshot'] = snapshot
            required = expected_rooms(args.source, name, snapshot.get('room_count', 0))
            report.update(evaluate_snapshot(snapshot, stage, required))
        except (ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            report['error'] = str(error)
        (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
        snap = report.get('snapshot', {})
        print('DONE', name, json.dumps(dict(gate=report['load_gate_passed'],
            stage=snap.get('stage'), frame=snap.get('level_frame_number'),
            pause=snap.get('player_pause_mode'), oom=snap.get('oom_marker'),
            oom_bytes=snap.get('oom_requested_bytes'),
            free=snap.get('g_MempExpansionPools', {}).get('free_bytes'),
            missing=report.get('missing_preload_rooms'),
            missing_batches=snap.get('rooms_missing_vertex_batches'), error=report.get('error'))), flush=True)
        return report

    reports = []
    with ThreadPoolExecutor(max_workers=args.jobs) as executor:
        futures = [executor.submit(run, index, name, stage)
                   for index, (name, stage) in enumerate(stages) if name in selected]
        for future in as_completed(futures):
            reports.append(future.result())
            (args.out / 'summary.json').write_text(json.dumps(reports, indent=2) + '\n')
    return 0 if all(report['load_gate_passed'] for report in reports) else 1


if __name__ == '__main__':
    raise SystemExit(main())

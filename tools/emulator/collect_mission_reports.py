"""Reinspect completed matrix snapshots, keeping paused and active gates separate.

Requires each run's original report and full RAM dump. This generates evidence,
not an emulator run, full-playthrough result or hardware verification.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from inspect_480i_rdram import inspect
from verify_resident_code import verify


def collect(elf, rom, roots, expected):
    rom_hash = hashlib.sha256(rom.read_bytes()).hexdigest()
    elf_hash = hashlib.sha256(elf.read_bytes()).hexdigest()
    reports = {}
    for root in roots:
        for path in sorted(root.glob('*/report.json')):
            report = json.loads(path.read_text())
            name = report['requested_stage']
            if name in reports:
                raise ValueError(f'Duplicate stage {name}')
            if report.get('rom_sha256') != rom_hash or report.get('elf_sha256') != elf_hash:
                raise ValueError(f'ROM/ELF identity mismatch: {path}')
            if report.get('exit_code') != 0 or report.get('error'):
                raise ValueError(f'Unsuccessful run: {path}')
            ram = path.parent / 'rdram-last.bin'
            report['resident_code_hashes'] = verify(elf, ram)
            state = inspect(elf, ram)
            # Do not silently replace an old report with a different snapshot.
            for key in ('stage', 'level_frame_number', 'oom_marker', 'active_dimensions'):
                if state.get(key) != report['snapshot'].get(key):
                    raise ValueError(f'Snapshot changed at {key}: {path}')
            report['snapshot'] = state
            report['load_gate_passed'] = (
                state['stage'] == report['requested_stage_id']
                and state['oom_marker'] == 0 and state['active_dimensions'] == [640, 480]
                and state.get('in_cutscene') == 0 and state.get('tick_mode') == 1
                and state.get('level_frame_number', 0) > 100)
            report['unpaused_snapshot'] = (
                report['load_gate_passed'] and state.get('level_paused') is False
                and state.get('player_pause_mode') == 0)
            reports[name] = report
    if len(reports) != expected:
        raise ValueError(f'Expected {expected} unique stages, found {len(reports)}')
    return [reports[name] for name in sorted(reports)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--elf', type=Path, required=True)
    parser.add_argument('--rom', type=Path, required=True)
    parser.add_argument('--roots', type=Path, nargs='+', required=True)
    parser.add_argument('--expected', type=int, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    result = collect(args.elf, args.rom, args.roots, args.expected)
    with args.out.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'stages': len(result),
                      'initial_load_passes': sum(r['load_gate_passed'] for r in result),
                      'unpaused_snapshots': sum(r['unpaused_snapshot'] for r in result),
                      'hardware_verified': False}))
    raise SystemExit(0 if all(r['load_gate_passed'] for r in result) else 1)

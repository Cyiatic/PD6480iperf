"""Reinspect normal-input mission chains; never select a result just because it passes.

Roots are supplied in parent-before-child order. A repeated mission is accepted
only as an authenticated continuation of its immediately preceding sample.
Original samples stay in the output, including startup cutscene samples.
"""
import argparse
import json
from pathlib import Path
from inspect_modern_rdram import inspect
from run_modern_menu_missions import digest, evaluate_snapshot, expected_rooms, source_stages


def verify_continuation(parent, child, parent_state_sha256):
    if child.get('parent_rdram_sha256') != parent['snapshot']['rdram_sha256']:
        raise ValueError('Continuation parent RAM mismatch')
    if child.get('parent_state_sha256') != parent_state_sha256:
        raise ValueError('Continuation parent state mismatch')
    if (child['requested_stage'], child['requested_stage_id']) != (
            parent['requested_stage'], parent['requested_stage_id']):
        raise ValueError('Continuation mission changed')
    snapshot = parent['snapshot']
    cache = snapshot.get('room_cache', {})
    if (snapshot['oom_marker'] or cache.get('load_failures', 0)
            or cache.get('allocator_faults', 0)
            or any(t['flags'] for t in snapshot['threads'].values())):
        raise ValueError('Cannot supersede a failed allocation or CPU fault')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('elf', 'rom', 'layout', 'source', 'out'):
        parser.add_argument('--' + name, type=Path, required=True)
    parser.add_argument('--roots', type=Path, nargs='+', required=True)
    args = parser.parse_args()
    identity = dict(rom_sha256=digest(args.rom), elf_sha256=digest(args.elf),
                    layout_sha256=digest(args.layout))
    stages = dict(source_stages(args.source))
    histories, latest = {}, {}
    for root in args.roots:
        metadata = json.loads((root / 'run-metadata.json').read_text())
        if any(metadata.get(key) != value for key, value in identity.items()):
            raise ValueError('Matrix ROM/ELF/layout identity mismatch')
        if metadata.get('instrumented_menu_selection') is not False:
            raise ValueError('Not ordinary-input evidence')
        for path in sorted(root.glob('*/report.json')):
            report = json.loads(path.read_text())
            name = report['requested_stage']
            if stages.get(name) != report['requested_stage_id']:
                raise ValueError('Unknown mission or wrong stage ID')
            if report.get('exit_code') != 0 or report.get('error'):
                raise ValueError('Unfinished/unsuccessful host')
            if report.get('instrumented_menu_selection') is not False:
                raise ValueError('Not ordinary-input report')
            if name in latest:
                parent, parent_path = latest[name]
                if Path(metadata.get('parent', '')).resolve() != parent_path.parent.parent.resolve():
                    raise ValueError('Duplicate/forked mission, not a direct continuation')
                verify_continuation(parent, report, digest(parent_path.parent / 'state.bin'))
            elif 'parent' in metadata:
                raise ValueError('Continuation parent missing from collection')
            snapshot = inspect(args.elf, path.parent / 'rdram-last.bin', args.layout)
            if snapshot['rdram_sha256'] != report['snapshot']['rdram_sha256']:
                raise ValueError('Original RAM changed')
            report['snapshot'] = snapshot
            report.update(evaluate_snapshot(snapshot, stages[name],
                expected_rooms(args.source, name, snapshot['room_count'])))
            report['evidence_path'] = str(path)
            report['input_sha256'] = digest(path.parent / 'input.txt')
            report['final_state_sha256'] = digest(path.parent / 'state.bin')
            report['final_png_sha256'] = digest(path.parent / 'final.png')
            histories.setdefault(name, []).append(report)
            latest[name] = report, path
    if set(latest) != set(stages):
        raise ValueError('Expected every stock solo mission exactly once in final selection')
    missions = [latest[name][0] for name in stages]
    result = dict(identity=identity, hardware_verified=False,
        instrumented_menu_selection=False, selection='direct authenticated continuation, not best result',
        samples=sum(map(len, histories.values())),
        initial_load_passes=sum(h[0]['load_gate_passed'] for h in histories.values()),
        final_load_passes=sum(r['load_gate_passed'] for r in missions),
        final_unpaused_samples=sum(r['unpaused_snapshot'] for r in missions),
        missions=missions, history=histories)
    with args.out.open('x') as stream:
        stream.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps({k: v for k, v in result.items() if k not in ('missions', 'history')}, indent=2))
    return 0 if all(r['load_gate_passed'] for r in missions) else 1


if __name__ == '__main__':
    raise SystemExit(main())

"""Reinspect completed normal-input samples with the current strict load gate."""
import argparse
import json
from pathlib import Path
from run_modern_menu_missions import digest, evaluate_snapshot, expected_rooms
from inspect_modern_rdram import inspect

parser = argparse.ArgumentParser(description=__doc__)
for name in ('elf','rom','layout','source','out'):
    parser.add_argument('--'+name,type=Path,required=True)
parser.add_argument('--roots',type=Path,nargs='+',required=True)
parser.add_argument('--expected',type=int,required=True)
args = parser.parse_args()
identity = dict(rom_sha256=digest(args.rom),elf_sha256=digest(args.elf),layout_sha256=digest(args.layout))
reports = {}
for root in args.roots:
    metadata = json.loads((root/'run-metadata.json').read_text())
    if any(metadata.get(key) != value for key,value in identity.items()):
        raise ValueError('Matrix identity mismatch')
    if metadata.get('instrumented_menu_selection') is not False:
        raise ValueError('Not ordinary-input evidence')
    for path in sorted(root.glob('*/report.json')):
        old = json.loads(path.read_text())
        name = old['requested_stage']
        if name in reports:
            raise ValueError('Duplicate mission')
        if old.get('exit_code') != 0 or old.get('error'):
            raise ValueError(f'Unfinished/unsuccessful host run: {name}')
        snapshot = inspect(args.elf,path.parent/'rdram-last.bin',args.layout)
        if snapshot['rdram_sha256'] != old['snapshot']['rdram_sha256']:
            raise ValueError('Original RAM evidence changed')
        required = expected_rooms(args.source,name,snapshot.get('room_count',0))
        old.update(evaluate_snapshot(snapshot,old['requested_stage_id'],required))
        old['snapshot'] = snapshot
        reports[name] = old
if len(reports) != args.expected:
    raise ValueError(f'Expected {args.expected} completed missions, found {len(reports)}')
result = dict(identity=identity, hardware_verified=False,instrumented_menu_selection=False,
              missions=[reports[name] for name in sorted(reports)])
with args.out.open('x') as stream:
    stream.write(json.dumps(result,indent=2)+'\n')
for name,report in reports.items():
    snap=report['snapshot']
    print(name, json.dumps(dict(gate=report['load_gate_passed'],
        frame=snap['level_frame_number'],paused=snap['player_pause_mode'],
        oom=snap['oom_requested_bytes'],missing=len(report['missing_preload_rooms']),
        missing_batches=snap['rooms_missing_vertex_batches'],faults=report['thread_faults'])))
raise SystemExit(0 if all(r['load_gate_passed'] for r in reports.values()) else 1)

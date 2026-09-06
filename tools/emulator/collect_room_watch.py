"""Preserve bounded read-only room-counter watch evidence; never copy ROM/RAM/states.

Usage: collect_room_watch.py PLAN OUTDIR
PLAN has workspace, rom, rom_sha256, elf, layout, host, core, directory, input,
save, log, ticks, controller_mask. This collector requires a completed cold run.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import struct
import subprocess
from inspect_modern_rdram import inspect
from audit_480i_elf import Elf32


EVENT = re.compile(r'^WATCH frame=(\d+) event=(\d+) counter=([0-9a-f]{8}) '
                   r'before=(\d+) after=(\d+) state=([01])$', re.MULTILINE)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def event_snapshot(elf, ram, layout):
    # The frontend can yield while an allocator update is unfinished. Preserve
    # a validator rejection as a failure/unknown, never silently turn it into a
    # valid partition. Final snapshots still use the strict inspector directly.
    try:
        return {'snapshot': inspect(elf, ram, layout)}
    except ValueError as error:
        return {'snapshot': None, 'snapshot_validation_error': str(error)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    base = Path(plan['workspace'])
    paths = {key: base / plan[key] for key in
             ('rom', 'elf', 'layout', 'host', 'core', 'directory', 'input', 'save', 'log')}
    if digest(paths['rom']) != plan['rom_sha256']:
        raise ValueError('Wrong candidate ROM')
    log = paths['log'].read_text()
    if f"DONE frames={plan['ticks']} " not in log or 'TEST RAM WRITE' in log:
        raise ValueError('Incomplete run or RAM-write diagnostic')
    if 'WATCH restored baseline=' in log:
        raise ValueError('This collector requires a cold run')
    elf = Elf32(paths['elf'])
    counter = elf.symbols['g_BgCacheLoadFailures'][0]
    gate = elf.symbols['g_BgCacheMode'][0]
    expected = f'READ-ONLY WATCH counter={counter:08x} gate={gate:08x} value=3 limit=8'
    if expected not in log:
        raise ValueError('Watch configuration does not match candidate symbols')
    events = EVENT.findall(log)
    if len(events) > 8:
        raise ValueError('Too many watch captures')
    final = inspect(paths['elf'], paths['directory'] / 'rdram-last.bin', paths['layout'])
    if final.get('synthetic_replay_diagnostic') or 'allocation_trace' in final:
        raise ValueError('Instrumented ROM is not a normal read-only watch')
    identity = {key + '_sha256': digest(paths[key]) for key in
                ('rom', 'elf', 'layout', 'host', 'core', 'input', 'save', 'log')}
    args.out.mkdir(parents=True, exist_ok=False)
    (args.out / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    (args.out / 'host.log').write_bytes(paths['log'].read_bytes())
    (args.out / 'input.txt').write_bytes(paths['input'].read_bytes())
    summaries, previous_frame = [], 0
    for number, entry in enumerate(events, 1):
        frame, event, address, before, after, state_saved = entry
        frame, event, before, after = map(int, (frame, event, before, after))
        if event != number or frame <= previous_frame or after <= before or int(address, 16) != counter:
            raise ValueError('Invalid event ordering/counter')
        previous_frame = frame
        stem = f'watch-{event}-frame-{frame}'
        ram = paths['directory'] / (stem + '-rdram.bin')
        state = paths['directory'] / (stem + '-state.bin')
        ppm = paths['directory'] / f'frame-{frame}.ppm'
        data = ram.read_bytes()
        if len(data) != 0x800000 or struct.unpack_from('<I', data, counter & 0x7fffff)[0] != after or struct.unpack_from('<I', data, gate & 0x7fffff)[0] != 3:
            raise ValueError('Counter and snapshot disagree')
        details = event_snapshot(paths['elf'], ram, paths['layout'])
        snapshot = details['snapshot']
        record = dict(identity, event=event, frontend_tick=frame, before=before, after=after,
                      rdram_sha256=digest(ram), ppm_sha256=digest(ppm), **details,
                      hardware_verified=False, rom_instrumentation=False,
                      eeprom_header_adapter=True, controller_mask=plan['controller_mask'],
                      sample_boundary='libretro return; may be inside an unfinished game frame')
        if state_saved == '1':
            record['state_sha256'] = digest(state)
        (args.out / (stem + '.json')).write_text(json.dumps(record, indent=2) + '\n')
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(ppm), '-frames:v', '1',
                        str(args.out / (stem + '.png'))], check=True)
        summary = dict(event=event, frontend_tick=frame, before=before, after=after)
        if snapshot is not None:
            cache = snapshot['room_cache']
            summary.update(stage=snapshot['stage'], level_frame=snapshot['level_frame_number'],
                epoch=cache['epoch'], missing_visible_rooms=cache['missing_visible_rooms'],
                free_bytes=cache['free_bytes'], largest_free_span=cache['largest_free_span'],
                partition_valid=cache['partition_valid'])
        else:
            summary['snapshot_validation_error'] = details['snapshot_validation_error']
            summary['partition_valid'] = False
        summaries.append(summary)
    final_record = dict(identity, snapshot=final, hardware_verified=False,
                        rom_instrumentation=False, eeprom_header_adapter=True,
                        controller_mask=plan['controller_mask'], ticks=plan['ticks'],
                        state_sha256=digest(paths['directory'] / 'state.bin'))
    final_ppm = paths['directory'] / f"frame-{plan['ticks']}.ppm"
    final_record['final_ppm_sha256'] = digest(final_ppm)
    (args.out / 'final.json').write_text(json.dumps(final_record, indent=2) + '\n')
    subprocess.run(['ffmpeg', '-v', 'error', '-i', str(final_ppm), '-frames:v', '1',
                    str(args.out / 'final.png')], check=True)
    (args.out / 'summary.json').write_text(json.dumps(summaries, indent=2) + '\n')
    print(json.dumps(summaries, indent=2))


if __name__ == '__main__':
    main()

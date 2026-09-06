"""Preserve completed ordinary-controller samples, including failed/navigation samples.

Read-only with respect to emulator runs. Outputs small JSON/PNG evidence only,
never ROM/state/RAM/save binaries. No blanket gameplay or hardware pass label.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from inspect_modern_rdram import inspect


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('plan', type=Path)
    parser.add_argument('out', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    base = Path(plan['workspace'])
    paths = {key: base / plan[key] for key in ('rom', 'elf', 'layout', 'host', 'core')}
    if digest(paths['rom']) != plan['rom_sha256']:
        raise ValueError('Wrong candidate')
    identity = {key + '_sha256': digest(path) for key, path in paths.items()}
    args.out.mkdir(parents=True, exist_ok=False)
    summary = []
    for sample in plan['samples']:
        source = base / sample['directory']
        # Completion requires a final state AND exact final image, not live last-RAM.
        state, ram = source / 'state.bin', source / 'rdram-last.bin'
        ppm = source / ('frame-' + str(sample['ticks']) + '.ppm')
        if not all(path.is_file() for path in (state, ram, ppm)):
            raise ValueError('Missing completed sample files')
        output = args.out / source.name
        output.mkdir()
        snapshot = inspect(paths['elf'], ram, paths['layout'])
        if snapshot.get('synthetic_replay_diagnostic') or 'allocation_trace' in snapshot:
            raise ValueError('Not a normal ROM sample')
        record = dict(identity, snapshot=snapshot, hardware_verified=False,
                      rom_instrumentation=False, eeprom_header_adapter=True,
                      controller_mask=sample['controller_mask'], ticks=sample['ticks'],
                      observation=sample['observation'], state_sha256=digest(state),
                      final_ppm_sha256=digest(ppm), final_rdram_sha256=digest(ram))
        if sample.get('host'):
            record['host_sha256'] = digest(base / sample['host'])
        if sample.get('input'):
            inputs = base / sample['input']
            record['input_sha256'] = digest(inputs)
            (output / 'input.txt').write_bytes(inputs.read_bytes())
        else:
            record['controller_input'] = 'none (host argument -)'
        if sample.get('parent'):
            parent = base / sample['parent']
            record['parent'] = sample['parent']
            record['parent_state_sha256'] = digest(parent / 'state.bin')
            record['parent_rdram_sha256'] = digest(parent / 'rdram-last.bin')
            # Prove resident code in the parent belongs to the same candidate ELF.
            inspect(paths['elf'], parent / 'rdram-last.bin', paths['layout'])
        else:
            record['cold_boot'] = True
            record['save_sha256'] = digest(base / sample['save'])
        if sample.get('log'):
            logfile = base / sample['log']
            text = logfile.read_text()
            if f"DONE frames={sample['ticks']} " not in text:
                raise ValueError('Host log lacks terminal marker')
            (output / 'host.log').write_bytes(logfile.read_bytes())
        subprocess.run(['ffmpeg', '-v', 'error', '-i', str(ppm), '-frames:v', '1',
                        str(output / 'final.png')], check=True)
        (output / 'report.json').write_text(json.dumps(record, indent=2) + '\n')
        summary.append(dict(sample=source.name, stage=snapshot['stage'],
            players=snapshot.get('active_player_count'), oom=snapshot['oom_marker'],
            oom_bytes=snapshot['oom_requested_bytes'], observation=sample['observation']))
    (args.out / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    (args.out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()

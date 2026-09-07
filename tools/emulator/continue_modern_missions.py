"""Bounded ordinary-input continuation of same-ROM cutscene load samples.

Original evidence is immutable. A single late Start pulse is sent only when the
observed prior sample is still in a cutscene; paused samples get a single B.
No failure flags are cleared and no room memory or mission data is written.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
from pathlib import Path
import subprocess
from inspect_modern_rdram import inspect
from run_modern_menu_missions import digest, expected_rooms, evaluate_snapshot

def final_video_frame(output, ticks):
    frame = output / f'frame-{ticks}.ppm'
    if not frame.is_file() or frame.stat().st_size == 0:
        raise ValueError('Completed run produced no final video frame; native exit0 is not a pass')
    return frame

def continuation_input(snapshot, exercise=False):
    if exercise:
        if snapshot['in_cutscene'] or snapshot['player_pause_mode']:
            raise ValueError('Movement/menu exercise requires an unpaused gameplay parent')
        return ('30 100 0 0 -18000\n140 200 4096 0 0\n270 282 8 0 0\n'
                '370 376 0 22000 0\n470 476 0 -22000 0\n')
    return ('30 42 8 0 0\n' if snapshot['in_cutscene'] else
            ('30 42 2 0 0\n' if snapshot['player_pause_mode'] else ''))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('source','elf','rom','layout','host','core','root','out'):
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--stages',nargs='+',required=True)
    parser.add_argument('--ticks',type=int,default=1500)
    parser.add_argument('--jobs',type=int,choices=range(1,5),default=2)
    parser.add_argument('--exercise',action='store_true',help='Ordinary forward/fire/pause/menu swipes')
    args = parser.parse_args()
    if not 600 <= args.ticks <= 2400: raise ValueError('Unbounded continuation')
    metadata = json.loads((args.root/'run-metadata.json').read_text())
    identities = dict(rom_sha256=digest(args.rom),elf_sha256=digest(args.elf),layout_sha256=digest(args.layout))
    if any(metadata[key] != value for key,value in identities.items()):
        raise ValueError('Foreign ROM/ELF/layout')
    if metadata.get('instrumented_menu_selection') is not False:
        raise ValueError('Not a normal controller-input sample')
    args.out.mkdir(parents=True,exist_ok=False)
    newmeta = dict(identities, parent=str(args.root), hardware_verified=False,
                   instrumented_menu_selection=False,ticks=args.ticks,exercise=args.exercise)
    preserve_save=metadata.get('save_policy')=='preserve-matching'
    connected_mask=metadata.get('connected_mask',1)
    newmeta.update(save_policy='preserve-matching' if preserve_save else 'legacy-erased',connected_mask=connected_mask)
    (args.out/'run-metadata.json').write_text(json.dumps(newmeta,indent=2)+'\n')
    environment = dict(os.environ,PATH='C:/msys64/mingw64/bin;'+os.environ.get('PATH',''))
    def run(name):
        original = args.root/name.lower()
        prior = json.loads((original/'report.json').read_text())
        if prior.get('exit_code') != 0 or prior.get('error'): raise ValueError('Unfinished prior host')
        snap = inspect(args.elf,original/'rdram-last.bin',args.layout)
        if snap['rdram_sha256'] != prior['snapshot']['rdram_sha256']: raise ValueError('Changed prior RAM')
        cache = snap.get('room_cache',{})
        if snap['oom_marker'] or cache.get('load_failures',0) or cache.get('allocator_faults',0):
            raise ValueError('Do not try to continue through a known allocation failure')
        if any(t['flags'] for t in snap['threads'].values()): raise ValueError('Faulted prior CPU')
        output = args.out/name.lower()
        output.mkdir()
        save=original/'save-memory.bin'
        if preserve_save and (save.stat().st_size!=296960 or digest(save)!=prior.get('save_memory_sha256')):
            raise ValueError('Missing/changed matching parent save-memory')
        text = continuation_input(snap,args.exercise)
        (output/'input.txt').write_text(text)
        report = dict(requested_stage=prior['requested_stage'],requested_stage_id=prior['requested_stage_id'],
            parent_rdram_sha256=snap['rdram_sha256'],parent_state_sha256=digest(original/'state.bin'),
            parent_cutscene=snap['in_cutscene'],hardware_verified=False,instrumented_menu_selection=False,
            ticks=args.ticks,load_gate_passed=False,exercise=args.exercise)
        command = [str(args.host.resolve()),str(args.core.resolve()),str(args.rom.resolve()),str(output.resolve()),
            str(args.ticks),'cached_interpreter',str((output/'input.txt').resolve()),str((original/'state.bin').resolve()),
            str(save.resolve()) if preserve_save else '-','eeprom-header','-',str(connected_mask)]
        print('START',name,'bounded late ordinary input',text.strip(),flush=True)
        try:
            with (output/'host.log').open('x') as log:
                completed = subprocess.run(command,stdout=log,stderr=subprocess.STDOUT,env=environment,timeout=600)
            report['exit_code'] = completed.returncode
            if completed.returncode: raise ValueError('Continuation host failed')
            frame = final_video_frame(output,args.ticks)
            subprocess.run(['ffmpeg','-v','error','-i',str(frame),
                            '-frames:v','1',str(output/'final.png')],check=True,env=environment)
            final = inspect(args.elf,output/'rdram-last.bin',args.layout)
            report['snapshot'] = final
            report['save_memory_sha256']=digest(output/'save-memory.bin')
            report['connected_mask']=connected_mask
            report.update(evaluate_snapshot(final,report['requested_stage_id'],expected_rooms(args.source,name,final['room_count'])))
        except (ValueError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as error:
            # Retain the failed run too; do not abort collection of other futures
            # or synthesize a successful snapshot from native exit0 alone.
            report['error'] = str(error)
        (output/'report.json').write_text(json.dumps(report,indent=2)+'\n')
        final = report.get('snapshot',{})
        print('DONE',name,json.dumps(dict(gate=report['load_gate_passed'],stage=final.get('stage'),
            frame=final.get('level_frame_number'),cutscene=final.get('in_cutscene'),pause=final.get('player_pause_mode'),
            oom=final.get('oom_marker'),cache_failures=final.get('room_cache',{}).get('load_failures'),
            evictions=final.get('room_cache',{}).get('evictions'),faults=report.get('thread_faults'),
            error=report.get('error'))),flush=True)
        return report
    reports = []
    with ThreadPoolExecutor(max_workers=args.jobs) as workers:
        pending = [workers.submit(run,name.upper()) for name in args.stages]
        for future in as_completed(pending):
            reports.append(future.result())
            (args.out/'summary.json').write_text(json.dumps(reports,indent=2)+'\n')
    return 0 if all(r['load_gate_passed'] for r in reports) else 1

if __name__ == '__main__': raise SystemExit(main())

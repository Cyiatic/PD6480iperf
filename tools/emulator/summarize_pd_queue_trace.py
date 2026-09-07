"""Summarize the authenticated, read-only normal-v86f emulator observer log."""
import argparse
import hashlib
import json
from pathlib import Path


def summarize(path):
    text = path.read_text()
    if 'PDOBS authenticated normal-v86f enqueue code; read-only; limit8192' not in text or 'PDOBS rejected' in text:
        raise ValueError('Missing successful exact-code authentication')
    if 'DONE frames=3000 ram=8388608' not in text:
        raise ValueError('Run did not reach its terminal checkpoint')
    events = [json.loads(line[6:]) for line in text.splitlines() if line.startswith('PDOBS {')]
    for previous, current in zip(events, events[1:]):
        if current['n'] != previous['n'] + 1:
            raise ValueError('Trace has a sequence gap')
    blocked = next(e for e in events if e['ev']=='guest_sendcall' and
                   e['thread']=='80068f90' and e['queue']=='80068f78' and
                   e['a']=='80068f78' and e['b']=='00000002' and
                   e['argqvalid']==e['argqcapacity']==32)
    dropped = next(e for e in events if e['n']>blocked['n'] and e['ev']=='guest_fullcheck' and
                   e['a']=='00000020' and e['queue']=='8006b418' and
                   e['argqvalid']==e['argqcapacity']==8)
    retraces = [e for e in events if blocked['n']<e['n']<dropped['n'] and
                e['ev']=='guest_sendcall' and e['queue']=='8006b418']
    if [e['argqvalid'] for e in retraces] != list(range(8)):
        raise ValueError('Expected the eight queued VI notifications')
    if any(e['b']!='800020ac' for e in retraces) or dropped['intbuf'] != ['800020ac']*8:
        raise ValueError('Queue is not eight retrace-handler notifications')
    later_sp = [e for e in events if e['n']>dropped['n'] and e['ev']=='guest_sp_handler']
    if later_sp:
        raise ValueError('The trace later services an SP completion; inspect manually')
    return dict(hardware_verified=False, guest_rom_modified=False,
                log_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                total_events=len(events), bounded_trace_saturated=len(events)==8192,
                blocked_main_completion=blocked, queued_retraces=retraces,
                full_queue_sp_completion=dropped,
                interpretation='Main queue blocks scheduler completion; eight VI messages fill interruptQ; kernel discards SP completion.',
                limits='Exact normal-v86f software run only. Kernel branch semantics checked against its ELF. Does not prove a console occurrence or exclude other failures.')


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('log',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=summarize(args.log)
    with args.output.open('x') as output:
        output.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:result[key] for key in ('total_events','bounded_trace_saturated','interpretation')},indent=2))

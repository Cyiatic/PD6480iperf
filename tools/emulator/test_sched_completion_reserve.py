"""Compile the actual retrace notifier; preserve two graphics completion slots.

Checks bounded queues with paused/slow consumers and negative one/no-slot
controls. This is a queue invariant test, not proof of RCP timing on hardware.
"""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def extract(source):
    start = source.index('static void __scNotifyMainRetrace(')
    opening = source.index('{', start)
    depth, end = 1, opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


PREFIX = r'''
#include <stdio.h>
#include <stdint.h>
#include <string.h>
typedef intptr_t OSMesg;
typedef struct { int validCount, msgCount, first; OSMesg msg[32]; } OSMesgQueue;
typedef struct { OSMesgQueue *gfxmq; } OSSched;
#define OS_SC_RETRACE_MSG 1
#define OS_SC_DONE_MSG 2
#define OS_MESG_NOBLOCK 0
static int blocked, bad_flag;
static int osSendMesg(OSMesgQueue *q, OSMesg msg, int flag) {
    if(flag != OS_MESG_NOBLOCK) bad_flag++;
    if(q->validCount >= q->msgCount) { if(msg==OS_SC_DONE_MSG) blocked++; return -1; }
    q->msg[(q->first+q->validCount)%q->msgCount]=msg;
    q->validCount++; return 0;
}
static int receive(OSMesgQueue *q) {
    int msg=q->msg[q->first]; q->first=(q->first+1)%q->msgCount;
    q->validCount--; return msg;
}
#define CHECK(x) do { if(!(x)) {printf("FAIL line %d: %s\n",__LINE__,#x);return 42;} } while(0)
'''

TESTS = r'''
int main(void) {
    OSMesgQueue q={0}; OSSched sc={&q};
    int r,d,i,j,done,sent=0,received=0,outstanding=0,running=0;
    uint32_t random=0x50443634u;
    sc.gfxmq=NULL; __scNotifyMainRetrace(&sc); sc.gfxmq=&q;
    for(r=0;r<=30;r++) for(d=0;d<=2;d++) {
        memset(&q,0,sizeof(q));q.msgCount=32;
        for(i=0;i<r;i++) osSendMesg(&q,OS_SC_RETRACE_MSG,0);
        for(i=0;i<d;i++) osSendMesg(&q,OS_SC_DONE_MSG,0);
        for(i=0;i<10000;i++) __scNotifyMainRetrace(&sc);
        for(i=d;i<2;i++) {
            CHECK(osSendMesg(&q,OS_SC_DONE_MSG,0)==0);
            for(j=0;j<100;j++) __scNotifyMainRetrace(&sc);
        }
        done=0;while(q.validCount) done+=receive(&q)==OS_SC_DONE_MSG;
        CHECK(done==2 && blocked==0 && bad_flag==0);
        __scNotifyMainRetrace(&sc); CHECK(q.validCount==1); /* boot wakeup */
    }
    memset(&q,0,sizeof(q));q.msgCount=32;
    for(i=0;i<500000;i++) {
        random=random*1664525u+1013904223u;
        switch(random>>30) {
        case 0: __scNotifyMainRetrace(&sc);break;
        case 1: if(outstanding<2) {outstanding++;running++;} break;
        case 2: if(running) {
            CHECK(osSendMesg(&q,OS_SC_DONE_MSG,0)==0);running--;sent++;
        } break;
        case 3: if(q.validCount && receive(&q)==OS_SC_DONE_MSG) {outstanding--;received++;} break;
        }
        CHECK(q.validCount<=32 && outstanding>=0 && outstanding<=2);
    }
    done=0;while(q.validCount) done+=receive(&q)==OS_SC_DONE_MSG;
    CHECK(sent==received+done && outstanding==running+done && blocked==0 && bad_flag==0);
    puts("PASS:93 slow-consumer queue states,two completions preserved,boot retrace,500000 interleavings");
    return 0;
}
'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    routine = extract((args.root / 'src/lib/sched.c').read_text())
    env = dict(os.environ, PATH='C:/msys64/mingw64/bin;' + os.environ.get('PATH', ''))
    with tempfile.TemporaryDirectory(prefix='pd-completion-reserve-') as temporary:
        root = Path(temporary)
        for name, slots, expected in (('actual',2,0),('one-slot-negative',1,42),('no-slot-negative',0,42)):
            body = routine.replace('msgCount - 2', f'msgCount - {slots}')
            if slots != 2 and body == routine:
                raise AssertionError('Negative control did not change actual helper')
            source, binary = root / (name+'.c'), root / (name+'.exe')
            source.write_text(PREFIX + body + TESTS)
            subprocess.run(['C:/msys64/mingw64/bin/gcc.exe','-O2','-Wall','-Werror',str(source),'-o',str(binary)],check=True,env=env)
            run = subprocess.run([str(binary)],env=env,capture_output=True,text=True)
            if run.returncode != expected:
                raise AssertionError(f'{name}: {run.returncode}: {run.stdout} {run.stderr}')
            print(name+': '+run.stdout.strip())

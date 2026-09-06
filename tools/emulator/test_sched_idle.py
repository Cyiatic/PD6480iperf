"""Compile actual scheduler idle check; exercise ownership and priority boundaries."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def function(source):
    start = source.index('bool schedIsGfxIdle(void)')
    opening = source.index('{', start)
    depth, end = 1, opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


PREFIX = r'''
#include <stdbool.h>
#include <stddef.h>
#include <stdio.h>
#include <string.h>
typedef int OSPri;
typedef int OSThread;
#define THREADPRI_SCHED 15
#define M_AUDTASK 2
struct Task { struct { struct { int type; } t; } list; };
struct { struct Task *curRSPTask, *curRDPTask, *nextGfxTask, *nextGfxTask2; } g_Sched;
OSThread g_MainThread, another_thread;
OSThread *__osRunningThread=&g_MainThread;
int priority=10, calls=0, error=0, clear_on_restore=0;
OSPri osGetThreadPri(void *thread) { if(thread) error++; return priority; }
void osSetThreadPri(void *thread, OSPri next) {
  if(thread || (calls==0 && next!=THREADPRI_SCHED+1) || (calls==1 && next!=10)) error++;
  priority=next; calls++;
  if(next==10 && clear_on_restore) memset(&g_Sched,0,sizeof(g_Sched));
}
#define CHECK(x) do { if(!(x)) { printf("FAIL line %d\n",__LINE__); return 42; } } while(0)
'''

TESTS = r'''
int main(void) {
  struct Task audio={{{2}}}, graphics={{{1}}}, unknown={{{99}}};
  struct Task *rsp[]={NULL,&audio,&graphics,&unknown};
  int r,d,n,m,expected;
  for(r=0;r<4;r++) for(d=0;d<2;d++) for(n=0;n<2;n++) for(m=0;m<2;m++) {
    calls=error=0; priority=10; clear_on_restore=0;
    g_Sched.curRSPTask=rsp[r]; g_Sched.curRDPTask=d ? &graphics : NULL;
    g_Sched.nextGfxTask=n ? &graphics : NULL; g_Sched.nextGfxTask2=m ? &graphics : NULL;
    expected=r<2 && !d && !n && !m;
    CHECK(schedIsGfxIdle()==expected);
    CHECK(calls==2 && !error && priority==10);
  }
  // Ownership must be evaluated BEFORE restoring priority. Completion at the
  // restore boundary may clear queues, but must not rewrite the sampled result.
  memset(&g_Sched,0,sizeof(g_Sched));
  g_Sched.nextGfxTask2=&graphics; calls=error=0; clear_on_restore=1;
  CHECK(!schedIsGfxIdle()); CHECK(calls==2 && !error && priority==10);
  CHECK(g_Sched.nextGfxTask2==NULL);
  // A non-main caller cannot promise no later graphics producer will run.
  __osRunningThread=&another_thread; calls=error=0;
  CHECK(!schedIsGfxIdle()); CHECK(calls==0 && !error && priority==10);
  puts("PASS: actual idle helper,32 ownership states,audio vs unknown,atomic sampling,priority restoration,non-main rejection");
  return 0;
}
'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path)
    args = parser.parse_args()
    routine = function((args.root / 'src/lib/sched.c').read_text())
    # Negative control removes the critical-section entry and must fail.
    unsafe = routine.replace('osSetThreadPri(0, THREADPRI_SCHED + 1);', '')
    env = dict(os.environ, PATH='C:/msys64/mingw64/bin;' + os.environ.get('PATH', ''))
    with tempfile.TemporaryDirectory(prefix='pd-gfx-idle-') as temporary:
        root = Path(temporary)
        for name, body, expected in (('actual',routine,0),('unlocked-negative',unsafe,42)):
            source, binary = root / (name+'.c'), root / (name+'.exe')
            source.write_text(PREFIX + body + TESTS)
            subprocess.run(['C:/msys64/mingw64/bin/gcc.exe','-O2','-Wall','-Werror',str(source),'-o',str(binary)],check=True,env=env)
            run = subprocess.run([str(binary)],env=env,capture_output=True,text=True)
            if run.returncode != expected:
                raise AssertionError(f'{name}: {run.returncode}: {run.stdout} {run.stderr}')
            print(name+': '+run.stdout.strip())

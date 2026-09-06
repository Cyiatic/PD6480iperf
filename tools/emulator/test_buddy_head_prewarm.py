"""Compile/exercise the actual default-AI-buddy head prewarm helper."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def check(source_root):
    text = (source_root / 'src/game/body.c').read_text()
    start = text.index('void bodyPreloadDefaultBuddyHead(void)')
    routine = text[start:text.index('\nstruct model *bodyAllocateModel(', start)]
    lv = (source_root / 'src/game/lv.c').read_text()
    assert lv.count('bodyPreloadDefaultBuddyHead();') == 1
    assert lv.index('bodyPreloadDefaultBuddyHead();') < lv.index('bgPreload();')
    prefix = '''#include <stdint.h>
#include <stddef.h>
typedef uint32_t u32;
#define HEAD_VD 1
#define STAGE_CITRAINING 38
#define STAGE_MBR 55
#define CHEAT_PUGILIST 0
#define CHEAT_HOTSHOT 1
#define CHEAT_HITANDRUN 2
#define CHEAT_ALIEN 3
struct { int iscoop; } g_MissionConfig;
struct { int numaibuddies, normmplayerisrunning, stagenum; } g_Vars;
struct { void *filedata; int filenum; } g_HeadsAndBodies[2];
u32 g_CheatsActiveBank0;
int calls, loaded_file;
void *modeldefLoadToNew(int file) { calls++; loaded_file=file; return (void *)0x1234; }
#define CHECK(condition) do { if (!(condition)) return 42; } while (0)
'''
    tests = '''
void reset(void) {
  g_MissionConfig.iscoop=1; g_Vars.numaibuddies=1;
  g_Vars.normmplayerisrunning=0; g_Vars.stagenum=47;
  g_CheatsActiveBank0=0; g_HeadsAndBodies[HEAD_VD].filedata=NULL;
  g_HeadsAndBodies[HEAD_VD].filenum=0x561; calls=loaded_file=0;
}
int main(void) {
  reset(); bodyPreloadDefaultBuddyHead();
  CHECK(calls==1 && loaded_file==0x561 && g_HeadsAndBodies[HEAD_VD].filedata==(void *)0x1234);
  bodyPreloadDefaultBuddyHead(); CHECK(calls==1);
  reset(); g_Vars.numaibuddies=4; bodyPreloadDefaultBuddyHead(); CHECK(calls==1);
  reset(); g_MissionConfig.iscoop=0; bodyPreloadDefaultBuddyHead(); CHECK(calls==0);
  reset(); g_Vars.numaibuddies=0; bodyPreloadDefaultBuddyHead(); CHECK(calls==0);
  reset(); g_Vars.normmplayerisrunning=1; bodyPreloadDefaultBuddyHead(); CHECK(calls==0);
  reset(); g_Vars.stagenum=STAGE_CITRAINING; bodyPreloadDefaultBuddyHead(); CHECK(calls==0);
  reset(); g_Vars.stagenum=STAGE_MBR; bodyPreloadDefaultBuddyHead(); CHECK(calls==0);
  for(unsigned flags=1;flags<16;flags++) {
    reset(); g_CheatsActiveBank0=flags; bodyPreloadDefaultBuddyHead(); CHECK(calls==0);
  }
  reset(); g_CheatsActiveBank0=1u<<10; bodyPreloadDefaultBuddyHead(); CHECK(calls==1);
  return 0;
}
'''
    env = dict(os.environ, PATH='C:/msys64/mingw64/bin;' + os.environ.get('PATH', ''))
    with tempfile.TemporaryDirectory(prefix='pd-buddy-prewarm-') as temporary:
        root = Path(temporary)
        source, binary = root / 'test.c', root / 'test.exe'
        source.write_text(prefix + routine + tests)
        subprocess.run(['C:/msys64/mingw64/bin/gcc.exe', '-Wall', '-Werror', str(source),
                        '-o', str(binary)], env=env, check=True)
        subprocess.run([str(binary)], env=env, check=True)
    print('PASS: actual C preloads only the pending default buddy head once; excludes solo, Combat, CI, Mr Blonde and all alternate-buddy cheat combinations; call precedes room budgeting')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    check(parser.parse_args().source_root)

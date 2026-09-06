"""Compile the actual CI reservation helper; no ROM or emulated RAM edits."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def check(source_root):
    text = (source_root / 'src/game/bg.c').read_text()
    start = text.index('static u32 bgGetLateAllocationReserve(u32 prepaidlatebytes)')
    routine = text[start:text.index('\nvoid bgPreload(u32 prepaidlatebytes)', start)]
    prefix = '''#include <stdint.h>
#include <stddef.h>
#include <assert.h>
typedef uint32_t u32;
typedef int32_t s32;
#define ARRAYCOUNT(a) (sizeof(a)/sizeof((a)[0]))
#define ALIGN16(a) (((a)+15)&~15)
#define STAGE_CITRAINING 38
struct { int stagenum; } g_Vars;
struct { struct { void *unk004; u32 unk008; } unk840; } g_Menus[4];
'''
    tests = '''
// Avoid Windows crash reporting for the deliberately failing negative control.
#undef assert
#define assert(condition) do { if (!(condition)) return 42; } while (0)
int main(void) {
  g_Vars.stagenum=STAGE_CITRAINING;
  for(int i=0;i<4;i++) g_Menus[i].unk840.unk008=153600;
  assert(bgGetLateAllocationReserve(0)==131072+4*153600);
  for(int i=0;i<4;i++) {
    g_Menus[i].unk840.unk004=(void *)1;
    assert(bgGetLateAllocationReserve(0)==131072+(3-i)*153600);
  }
  for(int i=0;i<4;i++) {
    g_Menus[i].unk840.unk004=NULL;
    g_Menus[i].unk840.unk008=i*16+1;
  }
  assert(bgGetLateAllocationReserve(0)==131072+16+32+48+64);
  for(int stage=0;stage<100;stage++) if(stage!=STAGE_CITRAINING) {
    g_Vars.stagenum=stage;
    assert(bgGetLateAllocationReserve(0)==131072);
  }
  assert(bgGetLateAllocationReserve(21792)==109280);
  for(u32 paid=0;paid<131072;paid+=16)
    assert(bgGetLateAllocationReserve(paid)+paid==131072);
  assert(bgGetLateAllocationReserve(131072)==131072);
  assert(bgGetLateAllocationReserve(0xffffffff)==131072);
}
'''
    negative = 'static u32 bgGetLateAllocationReserve(u32 prepaidlatebytes) { return 131072 + (g_Vars.stagenum==38 ? 153600 : 0); }'
    env = dict(os.environ, PATH='C:/msys64/mingw64/bin;' + os.environ.get('PATH', ''))
    with tempfile.TemporaryDirectory(prefix='pd-late-reserve-') as temporary:
        root = Path(temporary)
        for name, function, accepted in [('actual', routine, True), ('old-one-player', negative, False)]:
            source, binary = root / (name + '.c'), root / (name + '.exe')
            source.write_text(prefix + function + tests)
            subprocess.run(['C:/msys64/mingw64/bin/gcc.exe', '-Wall', '-Werror', '-Wno-sign-compare',
                            str(source), '-o', str(binary)], env=env, check=True)
            result = subprocess.run([str(binary)], env=env, capture_output=True)
            if result.returncode != (0 if accepted else 42):
                raise AssertionError(f'{name}: unexpected result {result.returncode}')
    print('PASS: actual C reserves all pending menus, credits prepaid model bytes without unsigned underflow, conserves total late allowance; old one-player reserve rejected')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    check(parser.parse_args().source_root)

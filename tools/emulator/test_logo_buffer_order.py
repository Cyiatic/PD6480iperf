"""Compile the actual logo configuration routine and reject the old reset."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def check(root):
    source = (root / 'src/lib/vi.c').read_text()
    for declaration in ('u8 g_ViFrontIndex = 0;', 'u8 g_ViBackIndex = 1;'):
        if declaration not in source:
            raise ValueError('Review one-time boot index initialization')
    begin = source.index('void viConfigureForLogos(void)')
    end = source.index('\n/**', begin)
    routine = source[begin:end]
    negative = routine.replace('{', '{\n g_ViFrontIndex = 0; g_ViBackIndex = 1;', 1)
    prefix = '''#include <stdint.h>
#include "pd480_framebuffer.h"
typedef uint8_t u8;
struct rend_vidat { unsigned fb; };
struct rend_vidat g_ViDataArray[2] = {{PD480_FB0}, {PD480_FB1}};
struct rend_vidat *g_ViFrontData = &g_ViDataArray[0], *g_ViBackData = &g_ViDataArray[0];
u8 g_ViFrontIndex = 0, g_ViBackIndex = 1;
int var8005d588, var8005d58c;
#define CHECK(x) do { if (!(x)) return 1; } while (0)
'''
    tests = '''
int main(void) {
    viConfigureForLogos();
    CHECK(g_ViFrontIndex == 0 && g_ViBackIndex == 1);
    CHECK(g_ViFrontData == &g_ViDataArray[0] && g_ViBackData == &g_ViDataArray[1]);
    for (int initial = 0; initial < 2; initial++) {
        g_ViFrontIndex = initial; g_ViBackIndex = 1-initial;
        for (int frame = 0; frame < 200; frame++) {
            int front = g_ViFrontIndex, back = g_ViBackIndex;
            unsigned displayed = g_ViDataArray[front].fb;
            var8005d588 = 99; var8005d58c = 77;
            viConfigureForLogos();
            CHECK(g_ViFrontIndex == front && g_ViBackIndex == back);
            CHECK(g_ViFrontData == &g_ViDataArray[front] && g_ViBackData == &g_ViDataArray[back]);
            CHECK(!var8005d588 && !var8005d58c);
            CHECK(pd480CanRender(g_ViBackData->fb, displayed, displayed, 0, 0));
            CHECK(pd480CanRender(g_ViBackData->fb, displayed | 0x20000000u, displayed, 0, 0));
            g_ViFrontIndex ^= 1; g_ViBackIndex ^= 1;
        }
    }
    return 0;
}
'''
    env = dict(os.environ)
    env['PATH'] = 'C:/msys64/mingw64/bin;' + env.get('PATH', '')
    with tempfile.TemporaryDirectory(prefix='pd-logo-order-') as directory:
        for label, code, expected in [('actual', routine, 0), ('old-reset', negative, 1)]:
            cfile = Path(directory) / (label + '.c')
            binary = Path(directory) / (label + '.exe')
            cfile.write_text(prefix + code + tests)
            subprocess.run(['C:/msys64/mingw64/bin/gcc.exe', '-Wall', '-Werror',
                            '-I', str(root / 'src/include'), str(cfile), '-o', str(binary)], check=True, env=env)
            result = subprocess.run([str(binary)], env=env)
            if result.returncode != expected:
                raise AssertionError(f'{label}: expected {expected}, got {result.returncode}')
    print('PASS: actual logo routine preserves both buffer orders across 400 transitions; old reset rejected')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    check(parser.parse_args().source_root)

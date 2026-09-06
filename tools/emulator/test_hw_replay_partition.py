"""Compile actual diagnostic input writer; protect physical controller status."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def check(source_root):
    source = (source_root / 'src/lib/hwtest.c').read_text()
    begin = source.index('static void pdHwApplyInput(')
    end = source.index('\nvoid pdHwReplay(', begin)
    routine = source[begin:end]
    prefix = '''#include <stdint.h>
#include <string.h>
#undef errno
typedef int32_t s32;
typedef struct { uint16_t button; int8_t stick_x, stick_y; uint8_t errno; } OSContPad;
struct contsample { OSContPad pads[4]; };
#define CHECK(x) do { if (!(x)) return 1; } while (0)
'''
    test = '''
int main(void) {
    struct contsample samples[20], before[20];
    OSContPad pad = {0x8000, 25, 45, 0};
    for (int first=0; first<20; first++) for (int last=0; last<20; last++) {
        memset(samples, 0xa5, sizeof(samples));
        for (int n=0; n<20; n++) for (int p=0; p<4; p++)
            samples[n].pads[p].errno = p ? 8 : 0;
        memcpy(before, samples, sizeof(samples));
        pdHwApplyInput(samples, first, last, &pad);
        for (int n=0; n<20; n++) {
            int delta=(n-first+20)%20, count=(last-first+20)%20;
            if (!delta || delta>count) CHECK(!memcmp(&samples[n], &before[n], sizeof(samples[n])));
            for (int p=0; p<4; p++) {
                CHECK(samples[n].pads[p].errno == before[n].pads[p].errno);
                if (delta && delta<=count) {
                    CHECK(samples[n].pads[p].button == (p ? 0 : pad.button));
                    CHECK(samples[n].pads[p].stick_x == (p ? 0 : pad.stick_x));
                    CHECK(samples[n].pads[p].stick_y == (p ? 0 : pad.stick_y));
                }
            }
        }
    }
    return 0;
}
'''
    needle = 'samples[index].pads[i].stick_y = i == 0 ? pad->stick_y : 0;'
    if routine.count(needle) != 1:
        raise ValueError('Input loop changed; review the negative control')
    negative = routine.replace(needle, needle + '\n samples[index].pads[i].errno = 0;')
    environment = dict(os.environ)
    environment['PATH'] = 'C:/msys64/mingw64/bin;' + environment.get('PATH', '')
    with tempfile.TemporaryDirectory(prefix='pd-replay-partition-') as directory:
        directory = Path(directory)
        for name, code, expected in [('actual', routine, 0), ('fake-presence', negative, 1)]:
            cfile, exe = directory / (name + '.c'), directory / (name + '.exe')
            cfile.write_text(prefix + code + test)
            subprocess.run(['C:/msys64/mingw64/bin/gcc.exe', '-Wall', '-Werror',
                            str(cfile), '-o', str(exe)], check=True, env=environment)
            result = subprocess.run([str(exe)], env=environment)
            if result.returncode != expected:
                raise AssertionError(f'{name}: expected {expected}, got {result.returncode}')
    print('PASS: 400 ring boundaries, prior/next partitions and physical errno preserved; old fake-presence control rejected')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    check(parser.parse_args().source_root)

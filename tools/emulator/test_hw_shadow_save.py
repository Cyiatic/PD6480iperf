"""Compile and exercise the diagnostic's actual RAM EEPROM transfer routine."""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def check(source_root):
    source = (source_root / 'src/lib/hwtest.c').read_text()
    begin = source.index('s32 pdHwEeprom(')
    end = source.index('\nstatic void pdHwPhase', begin)
    routine = source[begin:end]
    prefix = '''#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>
#include <assert.h>
#include <string.h>
typedef uint32_t u32;
typedef int32_t s32;
typedef uint8_t u8;
u8 g_PdHwEeprom[2048];
u32 g_PdHwSaveReads, g_PdHwSaveWrites;
'''
    tests = '''
int main(void) {
    u8 input[2048], output[2048], before[2048];
    for (int i = 0; i < 2048; i++) input[i] = i ^ (i >> 3);
    assert(pdHwEeprom(true, 0, input, 2048) == 0);
    assert(pdHwEeprom(false, 0, output, 2048) == 0);
    assert(!memcmp(input, output, 2048));
    input[0] = 37;
    assert(pdHwEeprom(true, 255, input, 8) == 0);
    assert(pdHwEeprom(false, 255, output, 8) == 0 && output[0] == 37);
    memcpy(before, g_PdHwEeprom, 2048);
    assert(pdHwEeprom(true, 255, input, 9) != 0);
    assert(pdHwEeprom(true, 0, input, UINT32_MAX) != 0);
    assert(pdHwEeprom(false, 255, output, 9) != 0);
    assert(pdHwEeprom(true, 0, NULL, 8) != 0);
    assert(pdHwEeprom(false, 0, NULL, 8) != 0);
    assert(!memcmp(before, g_PdHwEeprom, 2048));
    assert(g_PdHwSaveReads == 2 && g_PdHwSaveWrites == 2);
}
'''
    environment = dict(os.environ)
    environment['PATH'] = 'C:/msys64/mingw64/bin;' + environment.get('PATH', '')
    with tempfile.TemporaryDirectory(prefix='pd-hw-shadow-') as directory:
        path = Path(directory)
        code, binary = path / 'test.c', path / 'test.exe'
        code.write_text(prefix + routine + tests)
        subprocess.run(['C:/msys64/mingw64/bin/gcc.exe', '-Wall', '-Werror',
                        str(code), '-o', str(binary)], check=True, env=environment)
        subprocess.run([str(binary)], check=True, env=environment)
    print('PASS: actual RAM EEPROM routine round trips, rejects overrun/null and preserves guards')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    check(parser.parse_args().source_root)

"""Run the candidate's actual bgTickRooms C function against allocator stubs.

Usage: python tools/test_bg_cache_policy.py SOURCE_ROOT HOST_C_COMPILER
This verifies policy boundaries, not rendering or console performance.
"""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


def extract_function(source, signature):
    start = source.index(signature)
    opening = source.index('{', start)
    depth = 0
    for end in range(opening, len(source)):
        depth += (source[end] == '{') - (source[end] == '}')
        if depth == 0:
            return source[start:end + 1]
    raise ValueError('Unterminated C function')


HARNESS = r'''
#include <assert.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
typedef int s32;
#define ROOMFLAG_ONSCREEN 4
struct { int roomcount; } g_Vars;
struct { int loaded240; int flags; } g_Rooms[8];
int g_BgUnloadDelay240 = 120, g_BgUnloadDelay240_2 = 120;
int bytes_free, evictions, defrags;
int memaGetLongestFree(void) { return bytes_free; }
void bgUnloadRoom(int i) { g_Rooms[i].loaded240 = 0; evictions++; }
void memaDefrag(void) { defrags++; }
@FUNCTION@
void reset(int spare) {
    memset(g_Rooms, 0, sizeof(g_Rooms));
    g_Vars.roomcount = 8; bytes_free = spare; evictions = defrags = 0;
}
int main(void) {
    /* Exactly 64 KiB: retain an old room, saturating its age. */
    reset(65536); g_Rooms[1].loaded240 = 120; bgTickRooms();
    assert(evictions == 0 && g_Rooms[1].loaded240 == 120);
    /* Below the threshold: original limit of two evictions per tick. */
    reset(65535);
    for (int i = 1; i <= 3; i++) g_Rooms[i].loaded240 = 119;
    bgTickRooms();
    assert(evictions == 2 && defrags == 2 && g_Rooms[3].loaded240 == 120);
    /* A visible room must not be selected by timed eviction. */
    reset(0); g_Rooms[1].loaded240 = 120; g_Rooms[1].flags = ROOMFLAG_ONSCREEN;
    bgTickRooms(); assert(evictions == 0 && g_Rooms[1].loaded240 == 1);
    /* Young rooms and unloaded slots are preserved under pressure. */
    reset(0); g_Rooms[1].loaded240 = 1; bgTickRooms();
    assert(evictions == 0 && g_Rooms[1].loaded240 == 2 && g_Rooms[2].loaded240 == 0);
    puts("PASS: threshold, eviction cap, visible protection, young/unloaded rooms");
    return 0;
}
'''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    parser.add_argument('compiler', type=Path)
    args = parser.parse_args()
    environment = dict(os.environ)
    environment['PATH'] = str(args.compiler.resolve().parent) + os.pathsep + environment.get('PATH', '')
    function = extract_function((args.source_root / 'src/game/bg.c').read_text(),
                                'void bgTickRooms(void)')
    with tempfile.TemporaryDirectory(prefix='pd-bg-cache-test-') as directory:
        root = Path(directory)
        source, binary = root / 'test.c', root / 'test.exe'
        source.write_text(HARNESS.replace('@FUNCTION@', function))
        subprocess.run([str(args.compiler), '-std=c99', '-Wall', '-Werror',
                        str(source), '-o', str(binary)], check=True, env=environment)
        subprocess.run([str(binary)], check=True, env=environment)

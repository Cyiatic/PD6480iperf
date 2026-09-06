"""Compile the actual mema allocator with 32-bit-address stubs on the host.

Only free-list metadata is dereferenced; emulated bank addresses are never host
pointers. This tests bank ownership, not a console or rendering workload.
"""
import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile

PREFIX = r'''
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>
#include <assert.h>
typedef int32_t s32;
typedef uint32_t u32;
typedef uint8_t u8;
u8 g_LvOom;
'''
TEST = r'''
static u32 free_total(void) {
    u32 size = 0;
    for (int i = 0; i < MAX_SPACES; i++) size += g_MemaHeap.spaces[i].size;
    return size;
}
int main(void) {
    void *blocks[32];
    memaReset((void *)0x80200000, 0x20000);
    blocks[0] = memaAlloc(0x2000);
    assert((u32)blocks[0] == 0x80200000);
    assert(memaAppendBank((void *)0x80500000, 0x20000));
    assert(free_total() == 0x3e000);
    for (int i = 1; i < 32; i++) {
        blocks[i] = memaAlloc(0x2000);
        u32 address = (u32)blocks[i];
        assert((address >= 0x80200000 && address < 0x80220000) ||
               (address >= 0x80500000 && address < 0x80520000));
    }
    assert(free_total() == 0);
    /* Live allocations remain in their bank; holes must never become free. */
    for (int i = 0; i < 32; i += 2) memaFree(blocks[i], 0x2000);
    for (int i = 1; i < 32; i += 2) memaFree(blocks[i], 0x2000);
    memaDefrag();
    assert(free_total() == 0x40000 && memaGetLongestFree() == 0x20000);
    assert(!memaAppendBank((void *)0x80510000, 0x20000)); /* overlap */
    assert(!memaAppendBank((void *)0x80520001, 0x20000)); /* alignment */
    assert(!memaAppendBank((void *)0x807ffff0, 0x20)); /* RDRAM end */
    assert(!memaAppendBank(NULL, 0x20000));
    assert(!memaAppendBank((void *)0x80520000, 0));
    assert(free_total() == 0x40000);
    /* Adjacent real banks may merge. Reset must forget the old banks. */
    assert(memaAppendBank((void *)0x80520000, 0x10000));
    assert(memaGetLongestFree() == 0x30000 && free_total() == 0x50000);
    memaReset((void *)0x80300000, 0x10000);
    assert(free_total() == 0x10000 && memaGetLongestFree() == 0x10000);
    assert((u32)memaAlloc(0x10000) == 0x80300000 && free_total() == 0);
    /* Growth must not bridge unowned space, even with another free bank. */
    memaReset((void *)0x80200000, 0x20000);
    blocks[0] = memaAlloc(0x20000);
    assert(memaAppendBank((void *)0x80500000, 0x20000));
    assert(!memaGrow(0x80220000, 16));
    assert(!memaRealloc(0x80200000, 0x20000, 0x20010));
    assert(free_total() == 0x20000);
    blocks[1] = memaAlloc(0x10000);
    assert((u32)blocks[1] == 0x80500000);
    assert(memaRealloc(0x80500000, 0x10000, 0x20000));
    assert(free_total() == 0);
    assert(memaRealloc(0x80500000, 0x20000, 0x10000));
    memaFree(blocks[0], 0x20000);
    memaFree(blocks[1], 0x10000);
    assert(free_total() == 0x40000 && memaGetLongestFree() == 0x20000);
    /* Deterministic fragmented workload: verify ownership after every step. */
    void *active[64] = {0};
    u32 sizes[64] = {0}, random = 0x50443634;
    memaReset((void *)0x80200000, 0x20000);
    assert(memaAppendBank((void *)0x80500000, 0x20000));
    for (int step = 0; step < 10000; step++) {
        random = random * 1664525u + 1013904223u;
        int slot = (random >> 16) & 63;
        u32 wanted = ((random >> 8) & 255) * 16 + 16;
        if (active[slot]) {
            if (step % 3 == 0) {
                if (memaRealloc((u32)active[slot], sizes[slot], wanted)) sizes[slot] = wanted;
            } else {
                memaFree(active[slot], sizes[slot]);
                active[slot] = NULL;
                sizes[slot] = 0;
            }
        } else {
            active[slot] = memaAlloc(wanted);
            if (active[slot]) sizes[slot] = wanted;
        }
        u32 owned = free_total();
        for (int i = 0; i < 64; i++) if (active[i]) {
            u32 start = (u32)active[i], end = start + sizes[i];
            assert((start >= 0x80200000 && end <= 0x80220000) ||
                   (start >= 0x80500000 && end <= 0x80520000));
            for (int j = i + 1; j < 64; j++) if (active[j]) {
                u32 other = (u32)active[j];
                assert(end <= other || start >= other + sizes[j]);
            }
            owned += sizes[i];
        }
        assert(owned == 0x40000);
    }
    for (int i = 0; i < 64; i++) if (active[i]) memaFree(active[i], sizes[i]);
    assert(free_total() == 0x40000 && memaGetLongestFree() == 0x20000);
    puts("PASS: bank ownership, grow/shrink, invalid banks, reset, 10000 fragmented operations");
    return 0;
}
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    parser.add_argument('compiler', type=Path)
    args = parser.parse_args()
    source = (args.source_root / 'src/lib/mema.c').read_text()
    source = re.sub(r'^#include[^\n]*\n', '', source, flags=re.M)
    environment = dict(os.environ)
    environment['PATH'] = str(args.compiler.resolve().parent) + os.pathsep + environment.get('PATH', '')
    with tempfile.TemporaryDirectory(prefix='pd-mema-banks-') as directory:
        root = Path(directory)
        code, binary = root / 'test.c', root / 'test.exe'
        code.write_text(PREFIX + source + TEST)
        subprocess.run([str(args.compiler), '-std=c99', '-Wall', '-Werror',
                        '-Wno-int-to-pointer-cast', '-Wno-pointer-to-int-cast',
                        str(code), '-o', str(binary)], env=environment, check=True)
        subprocess.run([str(binary)], env=environment, check=True)

"""Compile the real blur routines; check all quadrants, bounds and full-screen quads."""
import argparse
import os
from pathlib import Path
import re
import subprocess
import tempfile


def check(root):
    source = (root / 'src/game/menugfx.c').read_text()
    begin = source.index('void menugfxCreateBlur(void)')
    end = source.index('Gfx *menugfxRenderDialogBackground', begin)
    code = source[begin:end]
    defines = source[source.index('#define BLURIMG_WIDTH'):source.index('/**')]
    prefix = r'''
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef uint8_t u8;
typedef uint16_t u16;
typedef uint32_t u32;
typedef int16_t s16;
typedef int32_t s32;
typedef float f32;
typedef uint64_t Gfx;
#define PAL 0
#define UNCACHED(x) ((u8 *)(x))
#define osVirtualToPhysical(x) (x)
struct gfxvtx { s16 x, y, z, s, t; u8 colour; };
struct vidata { void *fb; int x, y, bufx, bufy; } front, back;
struct vidata *g_ViFrontData = &front, *g_ViBackData = &back;
u8 storage[2400 + 32], *g_BlurBuffer = storage + 16;
struct gfxvtx captured[4];
u32 coloursbuffer[1];
u32 *gfxAllocateColours(int count) { return coloursbuffer; }
struct gfxvtx *gfxAllocateVertices(int count) { return captured; }
#define CHECK(x) do { if (!(x)) { fprintf(stderr, "failure line %d\n", __LINE__); return 1; } } while (0)
'''
    # GBI is not emulated here: capture the actual routine's vertex output.
    for macro in sorted(set(re.findall(r'\b(g(?:SP|DP)\w+)\(', code))):
        prefix += f'#define {macro}(pkt, ...) ((void)(pkt))\n'
    tests = r'''
int main(void) {
    const int sizes[][2] = {{320,240}, {640,480}, {640,240}, {576,432}};
    const u16 quadrant[] = {0xf800,0x07c0,0x003e,0xfffe};
    Gfx commands[128];
    for (int mode=0; mode<4; mode++) {
        int w=sizes[mode][0], h=sizes[mode][1];
        u8 *fb=malloc(w*h*2);
        CHECK(fb != NULL);
        for (int y=0; y<h; y++) for (int x=0; x<w; x++) {
            u16 colour=quadrant[(y>=h/2)*2+(x>=w/2)];
            fb[(y*w+x)*2]=colour>>8; fb[(y*w+x)*2+1]=colour;
        }
        front=(struct vidata){fb,w,h,w,h};
        // Source and destination descriptors can differ. Read the front's pitch.
        back=(struct vidata){NULL,123,87,123,87};
        memset(storage,0xa5,sizeof(storage));
        menugfxCreateBlur();
        for (int y=0; y<30; y++) for (int x=0; x<40; x++) {
            u16 actual=(g_BlurBuffer[(y*40+x)*2]<<8)|g_BlurBuffer[(y*40+x)*2+1];
            CHECK(actual==quadrant[(y>=15)*2+(x>=20)]);
        }
        for (int i=0;i<16;i++) CHECK(storage[i]==0xa5 && storage[2416+i]==0xa5);
        back.x=w; back.y=h;
        for (int shift=-30; shift<=30; shift+=30) {
            menugfxRenderBgBlur(commands,0xffffffff,shift,shift);
            CHECK(captured[0].x==shift && captured[0].y==shift);
            CHECK(captured[1].x==shift+w*10+40 && captured[1].y==shift);
            CHECK(captured[2].x==shift+w*10+40 && captured[2].y==shift+h*10+50);
            CHECK(captured[3].x==shift && captured[3].y==shift+h*10+50);
            CHECK(captured[0].s==0 && captured[0].t==0);
            CHECK(captured[2].s==1280 && captured[2].t==960);
            for (int i=0;i<4;i++) CHECK(captured[i].z==-10);
        }
        free(fb);
    }
    return 0;
}
'''
    negative_quad = code.replace('g_ViBackData->x * 10u', '320 * 10u').replace('g_ViBackData->y * 10u', '240 * 10u')
    negative_sample = code.replace('s32 fbwidth = g_ViFrontData->bufx;', 's32 fbwidth = 320;').replace('s32 fbheight = g_ViFrontData->bufy;', 's32 fbheight = 240;')
    env = dict(os.environ)
    env['PATH'] = 'C:/msys64/mingw64/bin;' + env.get('PATH', '')
    with tempfile.TemporaryDirectory(prefix='pd-menu-blur-') as directory:
        for label, routine, expected in [('actual',code,0), ('quarter-quad',negative_quad,1), ('quarter-sample',negative_sample,1)]:
            cfile = Path(directory) / (label+'.c')
            binary = Path(directory) / (label+'.exe')
            cfile.write_text(prefix + defines + routine + tests)
            subprocess.run(['C:/msys64/mingw64/bin/gcc.exe','-Wall','-Werror','-Wno-unused-but-set-variable',str(cfile),'-o',str(binary)],env=env,check=True)
            result = subprocess.run([str(binary)],env=env,capture_output=True,text=True)
            if result.returncode != expected:
                raise AssertionError(f'{label}: {result.returncode}, expected {expected}: {result.stderr}')
    print('PASS: real C blur, four dimensions/four quadrants, output guards, three full-screen overlay offsets; quarter-screen negative controls rejected')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    check(parser.parse_args().source_root)

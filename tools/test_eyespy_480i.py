"""Compile the actual fisheye math/row-copy functions with a recording GBI shim.

This checks coordinates/texture fields, not RDP output or gameplay. The caller
must still cold-boot the candidate and visually exercise its real display list.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess


def function(source, name):
    start = source.index('static ', source.rfind('\n}', 0, source.index(name)))
    opening = source.index('{', source.index(name, start))
    depth = 1
    end = opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


SHIM = r'''
#include <assert.h>
#include <math.h>
#include <stdint.h>
#include <stdio.h>
typedef int32_t s32;
typedef uint32_t u32;
typedef uint16_t u16;
typedef float f32;
typedef struct { uint32_t w[2]; } Gfx;
struct view { int x,y,viewtop,viewy; } view, *g_ViBackData=&view;
static u16 fb[640*480];
static Gfx commands[64];
static int loads, rects, fills, imagewidth, tilewidth, leftbound, rightbound;
static unsigned tests;
#define G_IM_FMT_RGBA 0
#define G_IM_SIZ_16b 0
#define G_TX_RENDERTILE 0
#define G_TX_NOMIRROR 0
#define G_TX_CLAMP 2
#define G_TX_NOMASK 0
#define G_TX_NOLOD 0
#define gDPPipeSync(p) ((void)(p))
#define gDPLoadSync(p) ((void)(p))
#define gDPSetTextureImage(p,f,z,w,a) ((void)(p), (void)(a), imagewidth=(w))
#define gDPLoadBlock(p,t,s,v,n,d) ((void)(p), loads++, assert((n)+1==imagewidth), assert(((n)+1)*2<=4096))
#define gDPSetTile(p,f,z,line,mem,tile,pal,ct,mt,st,cs,ms,ss) ((void)(p), assert((line)*8>=imagewidth*2), assert((ct)==G_TX_CLAMP && (cs)==G_TX_CLAMP))
#define gDPSetTileSize(p,t,s,v,r,b) ((void)(p), tilewidth=(r)/4+1, assert(tilewidth==imagewidth), assert((b)==0))
static void rectangle(int x1,int y1,int x2,int y2,int s,int t,int dx,int dy) {
    double last=s/32.0 + ((x2-x1)/4-1)*dx/1024.0;
    rects++;
    assert(x1>=leftbound*4 && x2<=rightbound*4 && x2>x1);
    assert(y1>=0 && y2<=view.y*4 && y2-y1==4);
    assert(s>=0 && s<=32767 && t==0 && dx>=0 && dx<=32767 && dy==1024);
    assert(last<imagewidth && last>=0);
}
#define gSPTextureRectangle(p,a,b,c,d,t,s,v,dx,dy) ((void)(p),rectangle(a,b,c,d,s,v,dx,dy))
static void fill(int x1,int y1,int x2,int y2) {
    fills++;
    assert(x1>=leftbound && x2<=rightbound && x2>=x1);
    assert(y1>=view.viewtop && y2<=view.viewtop+view.viewy && y2-y1==1);
}
#define gDPFillRectangle(p,a,b,c,d) ((void)(p),fill(a,b,c,d))
'''

MAIN = r'''
int main(void) {
    int configs[][6]={{640,480,0,480,0,640},{640,480,0,240,0,640},
        {640,480,240,240,0,640},{640,480,0,480,320,320},
        {640,480,240,240,320,320},{320,240,10,220,0,320}};
    for (unsigned c=0;c<sizeof(configs)/sizeof(configs[0]);c++) {
        view.x=configs[c][0];view.y=configs[c][1];view.viewtop=configs[c][2];view.viewy=configs[c][3];
        int left=configs[c][4],width=configs[c][5];
        float half=view.viewy*0.5f;
        leftbound=left;rightbound=left+width;
        float centre=bview0f142d74((int)half,-1,half,half*half);
        assert(fabsf(centre-half*1.5f/view.y)<0.00001f);
        assert(bview0f142d74(-1,-1,half,half*half)==0);
        assert(bview0f142d74((int)half+1,-1,half,half*half)==0);
        for (int row=0;row<view.viewy;row++) {
            int folded=row<=half?row:view.viewy-row;
            float lens=bview0f142d74(folded,-1,half,half*half);
            assert(isfinite(lens) && lens>=0 && lens<=centre+0.00001f);
            if (row>0 && row<view.viewy) assert(lens>0);
            for (int startup=0;startup<=50;startup++) {
                for (int damage=0;damage<=1;damage++) {
                    float scale=lens*(startup/50.0f)*(damage?1.03f:1.0f);
                    loads=rects=fills=0;
                    Gfx *end=bviewCopyFisheyeRow(commands,fb,view.viewtop+row,scale,left,width);
                    assert(end>=commands && end<commands+64);
                    assert(loads==rects && loads<=1);
                    bviewDrawFisheyeRect(commands,view.viewtop+row,scale,left,width);
                    assert(fills==2);
                    tests++;
                }
            }
        }
        fills=0;
        bviewDrawFisheyeRect(commands,view.viewtop-1,0,left,width);
        bviewDrawFisheyeRect(commands,view.viewtop+view.viewy,0,left,width);
        assert(fills==0);
    }
    printf("PASS %u actual-C row/startup/damage cases; six viewport layouts; bounded masks/texture fields\n",tests);
    return 0;
}
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--cc', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    path = args.source / 'src/game/bondview.c'
    source = path.read_text()
    names = ('bviewCopyFisheyeRow', 'bviewDrawFisheyeRect', 'bview0f142d74')
    selected = '\n\n'.join(function(source, name) for name in names)
    testfile = args.out / 'eyespy-test.c'
    testfile.write_text(SHIM + selected + MAIN)
    binary = args.out / 'eyespy-test.exe'
    subprocess.run([args.cc, '-std=c99', '-O2', '-Wall', '-Werror',
                    '-Wno-pointer-to-int-cast', str(testfile), '-lm', '-o', str(binary)], check=True)
    result = subprocess.run([str(binary)], capture_output=True, text=True)
    # The original function must fail the new full-height centre assertion.
    old = subprocess.check_output(['git', '-C', str(args.source), 'show',
                                  '9bce9e60addc08b3b658fb0224621f32a99f1bdd:src/game/bondview.c'], text=True)
    negativefile = args.out / 'old-radius-negative.c'
    negativefile.write_text(SHIM + function(old, 'bview0f142d74') + r'''
int main(void) { view.y=480; float scale=bview0f142d74(240,-1,240,240*240);
printf("Original centre scale: %.6f (expected 0.75)\n",scale);
return fabsf(scale-0.75f)<0.00001f?0:17; }
''')
    negativebin = args.out / 'old-radius-negative.exe'
    subprocess.run([args.cc, '-std=c99', '-O2', str(negativefile), '-lm', '-o', str(negativebin)], check=True)
    negative = subprocess.run([str(negativebin)], capture_output=True, text=True)
    report = {'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
              'functions': names, 'result': result.returncode, 'stdout': result.stdout,
              'stderr': result.stderr, 'negative_control_exit': negative.returncode,
              'negative_control_stdout': negative.stdout,
              'scope': 'Actual source math and GBI arguments; not RDP/gameplay/hardware proof'}
    (args.out / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    if result.returncode != 0 or negative.returncode != 17:
        raise SystemExit('Fisheye regression gate failed')


if __name__ == '__main__':
    main()

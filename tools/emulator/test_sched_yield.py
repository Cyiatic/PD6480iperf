"""Compile actual scheduler handlers and check SP/DP/audio event interleavings.

This is a host state-machine regression test, not an RCP timing benchmark.
Only hardware entry points and task-completion notification are stubbed.
"""
import argparse
import os
from pathlib import Path
import subprocess
import tempfile


FUNCTIONS = ('__scExec', '__scTryDispatch', '__scHandleRSP', '__scHandleRDP')


def extract_function(source, name):
    start = source.index('static void ' + name + '(')
    opening = source.index('{', start)
    depth = 1
    end = opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return source[start:end]


PREFIX = r'''
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <stdint.h>
typedef uint32_t u32;
typedef void *OSMesg;
typedef struct { struct { int type; } t; } OSTask;
typedef struct Task {
    u32 state;
    OSTask list;
    int id;
} OSScTask;
typedef struct {
    OSScTask *curRSPTask, *curRDPTask, *nextAudTask, *nextGfxTask, *nextGfxTask2;
    void *gfxmq;
    int retraceMsg;
} OSSched;
#define OS_SC_NEEDS_RDP 1
#define OS_SC_NEEDS_RSP 2
#define OS_SC_RCP_MASK 3
#define OS_SC_YIELD 16
#define OS_SC_YIELDED 32
#define M_GFXTASK 1
#define M_AUDTASK 2
#define RSPEVENT_GFX_START 1
#define RSPEVENT_AUD_START 2
#define DPC_SET_FREEZE 1
#define OS_MESG_NOBLOCK 0
static bool g_Resetting;
static int var8005dd18 = 1;
static struct { int screenshottimer; } g_MenuData;
static int yielded, completed[3], starts, notifications, invalid_completion;
static void profileHandleRspEvent(int event) { (void)event; }
static void osWritebackDCacheAll(void) {}
static void osSpTaskLoad(OSTask *task) { (void)task; }
static void osSpTaskStartGo(OSTask *task) { (void)task; starts++; }
static int osSpTaskYielded(OSTask *task) { (void)task; return yielded; }
static void osDpSetStatus(int value) { (void)value; }
static void schedUpdatePendingArtifacts(void) {}
static void menugfxCreateBlur(void) {}
static void osSendMesg(void *queue, OSMesg msg, int flag) {
    (void)queue; (void)msg; (void)flag; notifications++;
}
static void __scTaskComplete(OSSched *sc, OSScTask *task) {
    (void)sc;
    if (task->state & OS_SC_RCP_MASK) invalid_completion++;
    completed[task->id]++;
}
'''


TESTS = r'''
#define CHECK(cond) do { if (!(cond)) { \
    fprintf(stderr, "FAIL %s:%d: %s\n", __func__, __LINE__, #cond); return 1; \
} } while (0)

static OSScTask gfx = {3, {{M_GFXTASK}}, 0};
static OSScTask aud = {2, {{M_AUDTASK}}, 1};
static OSScTask nextgfx = {3, {{M_GFXTASK}}, 2};

static int finish_second(OSSched *sc) {
    CHECK(sc->curRSPTask == &nextgfx && sc->curRDPTask == &nextgfx);
    __scHandleRSP(sc);
    CHECK(sc->curRSPTask == NULL && sc->curRDPTask == &nextgfx);
    __scHandleRDP(sc);
    CHECK(sc->curRSPTask == NULL && sc->curRDPTask == NULL);
    CHECK(completed[0] == 1 && completed[2] == 1 && !invalid_completion);
    CHECK(sc->nextGfxTask == NULL && sc->nextGfxTask2 == NULL);
    return 0;
}

static int normal(int dp_first) {
    OSSched sc = {0};
    sc.nextGfxTask = &gfx;
    sc.nextGfxTask2 = &nextgfx;
    __scTryDispatch(&sc);
    CHECK(sc.curRSPTask == &gfx && sc.curRDPTask == &gfx);
    if (dp_first) {
        __scHandleRDP(&sc);
        CHECK(completed[0] == 0 && sc.curRDPTask == NULL);
        __scHandleRSP(&sc);
    } else {
        __scHandleRSP(&sc);
        CHECK(completed[0] == 0 && sc.curRDPTask == &gfx && sc.curRSPTask == NULL);
        __scHandleRDP(&sc);
    }
    CHECK(completed[1] == 0 && starts == 2);
    return finish_second(&sc);
}

/* order 0: yield,DP,audio,RSP; 1: DP,yield,audio,RSP;
 * 2: yield,audio,DP,RSP; 3: yield,audio,RSP,DP. */
static int successful_yield(int order) {
    OSSched sc = {0};
    sc.nextGfxTask = &gfx;
    sc.nextGfxTask2 = &nextgfx;
    __scTryDispatch(&sc);
    gfx.state |= OS_SC_YIELD;
    sc.nextAudTask = &aud;
    yielded = 1;
    if (order == 1) __scHandleRDP(&sc);
    __scHandleRSP(&sc);
    CHECK(sc.curRSPTask == &aud);
    CHECK(sc.curRDPTask == (order == 1 ? NULL : &gfx));
    CHECK(sc.nextGfxTask == &gfx && sc.nextGfxTask2 == &nextgfx);
    CHECK(completed[0] == 0);
    if (order == 0) __scHandleRDP(&sc);
    __scHandleRSP(&sc); /* audio completes, yielded gfx resumes */
    CHECK(completed[1] == 1 && sc.curRSPTask == &gfx);
    CHECK(sc.curRDPTask == (order <= 1 ? NULL : &gfx));
    CHECK((gfx.state & (OS_SC_YIELD | OS_SC_YIELDED)) == 0);
    if (order == 2) __scHandleRDP(&sc);
    CHECK(completed[0] == 0);
    __scHandleRSP(&sc);
    if (order == 3) {
        CHECK(sc.curRSPTask == NULL && sc.curRDPTask == &gfx && completed[0] == 0);
        __scHandleRDP(&sc);
    }
    CHECK(starts == 4 && completed[0] == 1);
    return finish_second(&sc);
}

static int unsuccessful_yield(int dp_before_audio) {
    OSSched sc = {0};
    sc.nextGfxTask = &gfx;
    sc.nextGfxTask2 = &nextgfx;
    __scTryDispatch(&sc);
    gfx.state |= OS_SC_YIELD;
    sc.nextAudTask = &aud;
    yielded = 0; /* SP task finished before honoring yield */
    __scHandleRSP(&sc);
    CHECK(sc.curRSPTask == &aud && sc.curRDPTask == &gfx && completed[0] == 0);
    if (dp_before_audio) __scHandleRDP(&sc);
    __scHandleRSP(&sc);
    if (!dp_before_audio) {
        CHECK(sc.curRSPTask == NULL && sc.curRDPTask == &gfx);
        __scHandleRDP(&sc);
    }
    CHECK(completed[0] == 1 && completed[1] == 1 && starts == 3);
    return finish_second(&sc);
}

static int reject_non_yielded_alias(void) {
    OSSched sc = {0};
    sc.curRDPTask = &gfx;
    sc.nextGfxTask = &gfx;
    gfx.state = OS_SC_NEEDS_RDP;
    __scTryDispatch(&sc);
    CHECK(sc.curRSPTask == NULL && sc.curRDPTask == &gfx && starts == 0);
    return 0;
}

int main(int argc, char **argv) {
    if (argc != 2) return 2;
    int test = atoi(argv[1]);
    if (test < 2) return normal(test);
    if (test < 6) return successful_yield(test - 2);
    if (test < 8) return unsuccessful_yield(test - 6);
    return reject_non_yielded_alias();
}
'''


def run_source(source, directory, label):
    code = directory / (label + '.c')
    binary = directory / (label + '.exe')
    code.write_text(PREFIX + '\n'.join(extract_function(source, name)
                                     for name in FUNCTIONS) + TESTS)
    environment = dict(os.environ)
    environment['PATH'] = 'C:/msys64/mingw64/bin;' + environment.get('PATH', '')
    subprocess.run(['C:/msys64/mingw64/bin/gcc.exe', '-Wall', '-Werror',
                    str(code), '-o', str(binary)], check=True, env=environment)
    outcomes = []
    for test in range(9):
        result = subprocess.run([str(binary), str(test)], capture_output=True,
                                text=True, env=environment)
        outcomes.append(result.returncode == 0)
        print(f'{label} case {test}: {"PASS" if outcomes[-1] else "FAIL"}')
        if result.returncode:
            print(result.stderr.strip())
    return outcomes


def run_boot(source, directory, label):
    # Extract the actual six-task boot loop, not a rewritten model of its wait.
    start = source.index('\t\tj = 0;')
    opening = source.index('{', source.index('while (j < 6)', start))
    depth, end = 1, opening + 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    loop = source[start:end]
    prefix = r'''
#include <stdio.h>
#include <stdint.h>
typedef intptr_t s32;
typedef short s16;
typedef void *OSMesg;
#define OS_MESG_BLOCK 1
#define OS_SC_DONE_MSG 2
static int g_SchedMesgQueue, var8005dcc8, var8005dcf0;
static int event_index, in_flight, submissions, invalid_reuse;
static s16 retrace = 1, done = OS_SC_DONE_MSG;
static void viUpdateMode(void) {}
static void osRecvMesg(void *queue, OSMesg *message, int flags) {
    (void)queue; (void)flags;
    /* DP wake-up/retrace is delivered before full SP+DP completion. */
    if (event_index++ % 3 == 2) { *message = &done; in_flight = 0; }
    else *message = &retrace;
}
static void rdpCreateTask(int start, int end, int ignored, void *message) {
    (void)start; (void)end; (void)ignored; (void)message;
    if (in_flight) invalid_reuse++;
    in_flight = 1; submissions++;
}
int main(void) {
    int j;
    s32 i;
    s16 scdonemsg = OS_SC_DONE_MSG;
    OSMesg receivedmsg;
'''
    suffix = r'''
    if (submissions != 6 || invalid_reuse || in_flight) {
        fprintf(stderr, "Unsafe boot reuse: submissions=%d reuse=%d in_flight=%d\n",
                submissions, invalid_reuse, in_flight);
        return 1;
    }
    return 0;
}
'''
    code, binary = directory / (label + '-boot.c'), directory / (label + '-boot.exe')
    code.write_text(prefix + loop + suffix)
    environment = dict(os.environ)
    environment['PATH'] = 'C:/msys64/mingw64/bin;' + environment.get('PATH', '')
    subprocess.run(['C:/msys64/mingw64/bin/gcc.exe', '-Wall', '-Werror',
                    str(code), '-o', str(binary)], check=True, env=environment)
    result = subprocess.run([str(binary)], capture_output=True, text=True, env=environment)
    print(f'{label} boot loop: {"PASS" if result.returncode == 0 else "FAIL"}')
    if result.returncode:
        print(result.stderr.strip())
    return result.returncode == 0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    parser.add_argument('--baseline-revision')
    args = parser.parse_args()
    current = (args.source_root / 'src/lib/sched.c').read_text()
    with tempfile.TemporaryDirectory(prefix='pd-scheduler-yield-') as temp:
        directory = Path(temp)
        outcomes = run_source(current, directory, 'current')
        if not all(outcomes):
            raise SystemExit('Current scheduler fails event-interleaving checks')
        if not run_boot((args.source_root / 'src/lib/main.c').read_text(), directory, 'current'):
            raise SystemExit('Current boot loop reuses an in-flight task')
        if args.baseline_revision:
            baseline = subprocess.check_output(
                ['git', '-C', str(args.source_root), 'show',
                 args.baseline_revision + ':src/lib/sched.c'], text=True)
            previous = run_source(baseline, directory, 'baseline')
            if previous != [True, True, False, False, False, False, True, True, True]:
                raise SystemExit('Unexpected negative-control results')
            old_boot = subprocess.check_output(
                ['git', '-C', str(args.source_root), 'show',
                 args.baseline_revision + ':src/lib/main.c'], text=True)
            if run_boot(old_boot, directory, 'baseline'):
                raise SystemExit('Expected original boot loop to fail the early-DP wake-up case')
    print('PASS: 9 handler cases plus the actual boot loop; negative controls reject old behavior')

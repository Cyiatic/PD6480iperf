/* Compile only for inspection, never link into the ROM. Extract .rodata with
 * objcopy; inspect_modern_rdram.py consumes these candidate-ABI offsets. */
#include <ultra64.h>
#include <PR/sched.h>
#include "types.h"
#define OFF(t, f) __builtin_offsetof(t, f)
const u32 pdModernLayout[] = {
    0x50443831, 1,
    sizeof(struct g_vars), OFF(struct g_vars, lvframenum),
    OFF(struct g_vars, tickmode), OFF(struct g_vars, in_cutscene),
    OFF(struct g_vars, currentplayer), OFF(struct g_vars, roomcount),
    sizeof(struct player), OFF(struct player, pausemode),
    sizeof(struct room), OFF(struct room, gfxdata), OFF(struct room, gfxdatalen),
    sizeof(struct rend_vidat), OFF(struct rend_vidat, bufx),
    OFF(struct rend_vidat, bufy), OFF(struct rend_vidat, fb),
    sizeof(OSSched), OFF(OSSched, curRSPTask), OFF(OSSched, curRDPTask),
    sizeof(OSThread), OFF(OSThread, state), OFF(OSThread, flags),
    OFF(OSThread, context.pc), OFF(OSThread, context.cause),
    OFF(OSThread, context.badvaddr),
};

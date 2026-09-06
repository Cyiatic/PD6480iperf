/* Compile with the candidate's MIPS/ABI/version flags and inspect .rodata.
 * These values are diagnostic metadata, not linked into the game.
 */
#include <ultra64.h>
#include <PR/sched.h>
#include "types.h"
#define OFF(t, f) __builtin_offsetof(struct t, f)
const u32 pdTestLayout[] = {
    sizeof(struct g_vars), OFF(g_vars, tickmode), OFF(g_vars, stagenum),
    OFF(g_vars, roomcount), OFF(g_vars, lvframenum), OFF(g_vars, in_cutscene),
    sizeof(struct room), OFF(room, loaded240), OFF(room, gfxdata),
    OFF(room, vtxbatches), OFF(room, gfxdatalen), OFF(room, flags),
    OFF(g_vars, currentplayer), sizeof(struct player), OFF(player, pausemode),
};

/* Offsets consumed by inspect_scheduler_rdram.py. */
#define TOFF(t, f) __builtin_offsetof(t, f)
const u32 pdSchedTestLayout[] = {
    sizeof(OSSched), TOFF(OSSched, nextAudTask), TOFF(OSSched, nextGfxTask),
    TOFF(OSSched, nextGfxTask2), TOFF(OSSched, curRSPTask), TOFF(OSSched, curRDPTask),
    sizeof(OSThread), TOFF(OSThread, state), TOFF(OSThread, flags), TOFF(OSThread, id),
    TOFF(OSThread, context.pc), TOFF(OSThread, context.cause),
    TOFF(OSThread, context.badvaddr), TOFF(OSThread, context.ra) + 4,
    TOFF(OSThread, context.a0) + 4, TOFF(OSThread, context.s0) + 4,
};

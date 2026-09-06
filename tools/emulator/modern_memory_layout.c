/* Compile only for inspection, never link into the ROM. Extract .rodata with
 * objcopy; inspect_modern_rdram.py consumes these candidate-ABI offsets. */
#include <ultra64.h>
#include <PR/sched.h>
#include "types.h"
#ifdef PD_BGCACHE_LAYOUT
#include "bgcache.h"
#include "constants.h"
#endif
#define OFF(t, f) __builtin_offsetof(t, f)
const u32 pdModernLayout[] = {
    0x50443831,
#ifdef PD_BGCACHE_LAYOUT
    4,
#else
    3,
#endif
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
    OFF(struct player, prop), OFF(struct player, isdead),
    OFF(struct player, bondhealth), OFF(struct player, hands),
    sizeof(struct hand), OFF(struct hand, loadedammo),
    OFF(struct player, ammoheldarr), sizeof(struct prop),
    OFF(struct prop, pos), OFF(struct prop, rooms),
    OFF(struct player, playertriggeron),
    OFF(struct room, vtxbatches), OFF(struct room, numvtxbatches),
    sizeof(struct vtxbatch), sizeof(struct roomgfxdata),
    OFF(struct roomgfxdata, opablocks), OFF(struct roomgfxdata, xlublocks),
#ifdef PD_BGCACHE_LAYOUT
    sizeof(struct bgcacheroom), OFF(struct bgcacheroom, loadsize),
    OFF(struct bgcacheroom, lastuse), OFF(struct bgcacheroom, expectedbatches),
    OFF(struct bgcacheroom, warmed), sizeof(struct bgcacheheap),
    OFF(struct bgcacheheap, free), OFF(struct bgcacheheap, start),
    OFF(struct bgcacheheap, size), OFF(struct bgcacheheap, banks),
    OFF(struct bgcacheheap, faults), sizeof(struct bgcacheblock),
    OFF(struct bgcacheblock, next), OFF(struct bgcacheblock, size),
    OFF(struct room, flags), OFF(struct room, loaded240), ROOMFLAG_ONSCREEN,
#endif
};

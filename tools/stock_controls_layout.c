/* Inspection only: compile for MIPS, extract .rodata, never link into ROM. */
#include <ultra64.h>
#include "types.h"
#define OFF(t, f) __builtin_offsetof(t, f)
const u32 stockControlsLayout[] = {
    OFF(struct g_vars, currentplayer),
    OFF(struct g_vars, currentplayerstats),
    OFF(struct playerstats, mpindex),
    sizeof(struct mpplayerconfig),
    OFF(struct mpplayerconfig, controlmode),
    OFF(struct mpplayerconfig, options),
    OFF(struct player, insightaimmode),
    OFF(struct player, prop),
    OFF(struct prop, pos),
    OFF(struct player, vv_theta),
    OFF(struct player, vv_verta),
    OFF(struct player, pausemode),
};

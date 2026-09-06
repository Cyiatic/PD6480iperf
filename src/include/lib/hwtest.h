/* DIAGNOSTIC ONLY: never link this controller/save shim into a candidate. */
#ifndef _IN_LIB_HWTEST_H
#define _IN_LIB_HWTEST_H
#include <ultra64.h>
#include "types.h"
extern s32 g_PdHwPhase;
extern u32 g_PdHwPhaseTicks;
extern u32 g_PdHwToggleChecks;
extern u32 g_PdHwSaveReads;
extern u32 g_PdHwSaveWrites;
void pdHwReplay(struct contsample *samples, s32 first, s32 last);
s32 pdHwEeprom(bool write, u8 address, u8 *buffer, u32 len);
void pdHwWatchStart(void);
void pdHwMark(u32 step);
#endif

/* DIAGNOSTIC BRANCH ONLY. Never include this replay/save shim in a release. */
#ifndef _IN_LIB_HWTEST_H
#define _IN_LIB_HWTEST_H
#include <ultra64.h>
extern s32 g_PdHwPhase;
extern u32 g_PdHwPhaseTicks;
extern u32 g_PdHwToggleChecks;
extern u32 g_PdHwSaveReads;
extern u32 g_PdHwSaveWrites;
void pdHwInstallReplay(void);
s32 pdHwEeprom(bool write, u8 address, u8 *buffer, u32 len);
#endif

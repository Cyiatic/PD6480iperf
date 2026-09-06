/* Inspector-only ABI table. Never link this into a ROM. */
#include <ultra64.h>
#include <PR/sched.h>
#define OFF(t, f) __builtin_offsetof(t, f)
const u32 pdGfxOwnershipLayout[] = {
    0x50444746, 1, sizeof(OSSched), sizeof(OSScTask),
    OFF(OSSched, curRSPTask), OFF(OSSched, curRDPTask),
    OFF(OSSched, nextGfxTask), OFF(OSSched, nextGfxTask2),
    OFF(OSScTask, state), OFF(OSScTask, list.t.type), M_GFXTASK, M_AUDTASK,
};

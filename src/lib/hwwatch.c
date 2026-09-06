/* V82E isolated diagnostic: stop after ten seconds without main progress.
 * The timeout display is CPU-written 320x240, NOT 480i validation/gameplay.
 * EEPROM remains RAM-only; no input replay or physical Pak writes. */
#include <ultra64.h>
#include "constants.h"
#include "bss.h"
#include "data.h"
#include "types.h"
#include "video480i.h"
#include "lib/crash.h"
#include "lib/hwtest.h"
#include "lib/vi.h"

extern OSThread g_SchedThread;
extern OSSched g_Sched;
extern u32 g_MainNumGfxTasks;
extern bool g_JoyBusy;
extern u32 g_JoyCyclicPollDisableCount;

volatile u32 g_PdHwBootStep = 0;
volatile u32 g_PdHwHeartbeat = 0;
static OSThread g_PdHwWatchThread;
static u64 g_PdHwWatchStack[1024];
static OSTimer g_PdHwWatchTimer;
static OSMesgQueue g_PdHwWatchQueue;
static OSMesg g_PdHwWatchMessages[4];

void pdHwMark(u32 step)
{
	g_PdHwBootStep = step;
	g_PdHwHeartbeat = osGetCount();
}

static void pdHwWatchProc(void *arg)
{
	OSMesg msg;
	u32 state;
	u32 schedstate;
	u32 i;
	volatile u16 *fb = (volatile u16 *) PHYS_TO_K1(PD480_FB1);
	osSetTimer(&g_PdHwWatchTimer, OS_USEC_TO_CYCLES(1000000),
		OS_USEC_TO_CYCLES(1000000), &g_PdHwWatchQueue, NULL);
	for (;;) {
		osRecvMesg(&g_PdHwWatchQueue, &msg, OS_MESG_BLOCK);
		if ((u32)(osGetCount() - g_PdHwHeartbeat) > OS_USEC_TO_CYCLES(10000000)) break;
	}
	state = g_MainThread.state;
	schedstate = g_SchedThread.state;
	osStopThread(&g_MainThread);
	osStopThread(&g_SchedThread);
	/* Do not depend on the stopped game's display-list/VI ownership path. */
	osWritebackDCacheAll();
	g_ViBackData->x = 320;
	g_ViBackData->y = 240;
	crashReset();
	rmonPrintf("V82E STARTUP TIMEOUT - DIAGNOSTIC\n");
	rmonPrintf("STEP %u MAIN STATE %u SCHED STATE %u\n", g_PdHwBootStep, state, schedstate);
	rmonPrintf("MAIN PC %08x RA %08x\n", g_MainThread.context.pc, (u32)g_MainThread.context.ra);
	rmonPrintf("MAIN CAUSE %08x BAD %08x\n", g_MainThread.context.cause, g_MainThread.context.badvaddr);
	rmonPrintf("MAIN SP %08x A0 %08x A1 %08x\n", (u32)g_MainThread.context.sp,
		(u32)g_MainThread.context.a0, (u32)g_MainThread.context.a1);
	rmonPrintf("SCHED PC %08x RA %08x\n", g_SchedThread.context.pc, (u32)g_SchedThread.context.ra);
	rmonPrintf("SCHED CAUSE %08x BAD %08x\n", g_SchedThread.context.cause, g_SchedThread.context.badvaddr);
	rmonPrintf("GFX %u RSP %08x RDP %08x\n", g_MainNumGfxTasks, g_Sched.curRSPTask, g_Sched.curRDPTask);
	rmonPrintf("JOY BUSY %u DISABLE %u\n", g_JoyBusy, g_JoyCyclicPollDisableCount);
	rmonPrintf("RAM SAVE READ %u WRITE %u\n", g_PdHwSaveReads, g_PdHwSaveWrites);
	for (;;) {
		for (i = 0; i < 320 * 240; i++) fb[i] = 1;
		crashRenderFrame((u16 *)fb);
		osViSetMode(&osViModeNtscLan1);
		osViSwapBuffer((void *)fb);
		osViBlack(false);
		osRecvMesg(&g_PdHwWatchQueue, &msg, OS_MESG_BLOCK);
	}
}

void pdHwWatchStart(void)
{
	pdHwMark(1);
	osCreateMesgQueue(&g_PdHwWatchQueue, g_PdHwWatchMessages, 4);
	osCreateThread(&g_PdHwWatchThread, 7, pdHwWatchProc, NULL,
		&g_PdHwWatchStack[1024], THREADPRI_SCHED + 1);
	osStartThread(&g_PdHwWatchThread);
}

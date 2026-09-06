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
	u32 mainqueue;
	u32 schedqueue;
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
	mainqueue = (u32)g_MainThread.queue;
	schedqueue = (u32)g_SchedThread.queue;
	osStopThread(&g_MainThread);
	osStopThread(&g_SchedThread);
	/* Do not depend on the stopped game's display-list/VI ownership path. */
	osWritebackDCacheAll();
	g_ViBackData->x = 320;
	g_ViBackData->y = 240;
	crashReset();
	rmonPrintf("V82H STARTUP TIMEOUT - DIAGNOSTIC\n");
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
	rmonPrintf("WAIT MAIN %08x SCHED %08x\n", mainqueue, schedqueue);
	rmonPrintf("QUEUES SI %08x IRQ %08x GFX %08x\n",
		&g_PiMesgQueue.mtqueue, &g_Sched.interruptQ.mtqueue, &g_SchedMesgQueue.mtqueue);
	rmonPrintf("VI CURRENT %08x NEXT %08x\n", osViGetCurrentFramebuffer(), osViGetNextFramebuffer());
	rmonPrintf("FB SCHEDULED %08x QUEUED %08x\n", g_Sched.scheduledFB, g_Sched.queuedFB);
	rmonPrintf("TASK1 %08x FB %08x STATE %x\n", g_Sched.nextGfxTask,
		g_Sched.nextGfxTask ? g_Sched.nextGfxTask->framebuffer : 0,
		g_Sched.nextGfxTask ? g_Sched.nextGfxTask->state : 0);
	rmonPrintf("TASK2 %08x FB %08x STATE %x\n", g_Sched.nextGfxTask2,
		g_Sched.nextGfxTask2 ? g_Sched.nextGfxTask2->framebuffer : 0,
		g_Sched.nextGfxTask2 ? g_Sched.nextGfxTask2->state : 0);
	rmonPrintf("STAGE %u LVFRAME %u PHASE %u TICK %u\n", g_Vars.stagenum,
		g_Vars.lvframenum, g_PdHwPhase, g_PdHwPhaseTicks);
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

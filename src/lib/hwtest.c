/* V82B HARDWARE DIAGNOSTIC, NOT A RELEASE CANDIDATE.
 * Programmatic file selection and opening Video Options are test setup.
 * L, Hi-Res and movement then use the ordinary input consumers/handlers.
 * Replace only samples in the main thread's newly acquired partition. The
 * scheduler retains its real polling and owns the other partition; unlike the
 * older core, this core no longer has a separate joy playback interface.
 * All game-pak save access is redirected to RAM. Controller Pak writes blocked.
 */
#include <ultra64.h>
#include "constants.h"
#include "bss.h"
#include "data.h"
#include "types.h"
#include "lib/hwtest.h"
#include "game/filemgr.h"
#include "game/menu.h"
#include "game/player.h"

extern struct menudialogdef g_FilemgrFileSelectMenuDialog;
extern struct menudialogdef g_VideoOptionsMenuDialog;
extern struct menuitem g_VideoOptionsMenuItems[];
extern u8 g_PdHwEeprom[2048];
s32 g_PdHwPhase = 0;
u32 g_PdHwPhaseTicks = 0;
u32 g_PdHwToggleChecks = 0;
u32 g_PdHwSaveReads = 0;
u32 g_PdHwSaveWrites = 0;

s32 pdHwEeprom(bool write, u8 address, u8 *buffer, u32 len)
{
	u32 offset = (u32)address * 8;
	u32 i;
	if (buffer == NULL || len > sizeof(g_PdHwEeprom) - offset) return -1;
	for (i = 0; i < len; i++) {
		if (write) g_PdHwEeprom[offset + i] = buffer[i];
		else buffer[i] = g_PdHwEeprom[offset + i];
	}
	if (write) g_PdHwSaveWrites++;
	else g_PdHwSaveReads++;
	return 0;
}

static void pdHwPhase(s32 phase)
{
	g_PdHwPhase = phase;
	g_PdHwPhaseTicks = 0;
}

static bool pdHwPulse(u32 tick, u32 start)
{
	return tick >= start && tick < start + 3;
}

void pdHwReplay(struct contsample *samples, s32 first, s32 last)
{
	OSContPad pad = {0};
	struct menudialog *dialog;
	u32 tick;
	s32 i;
	s32 index;
	if (first == last) return;
	dialog = g_Menus[0].curdialog;
	tick = ++g_PdHwPhaseTicks;
	switch (g_PdHwPhase) {
	case 0:
		if (g_Vars.stagenum == STAGE_CITRAINING) pdHwPhase(1);
		else if (pdHwPulse(tick % 180, 60)) pad.button = START_BUTTON;
		break;
	case 1:
		if (dialog && dialog->definition == &g_FilemgrFileSelectMenuDialog
				&& g_FileLists[0] && g_FileLists[0]->numfiles == 1) {
			if (tick > 90) {
				union handlerdata data = {0};
				data.list.value = 0;
				g_MpPlayerNum = 0;
				filemgrChooseAgentListMenuHandler(MENUOP_SET, NULL, &data);
				pdHwPhase(2);
			}
		} else g_PdHwPhaseTicks = 0;
		break;
	case 2:
		if (!dialog && tick > 90 && g_Vars.lvframenum > 100) pdHwPhase(3);
		else if (pdHwPulse(tick % 90, 30)) pad.button = B_BUTTON;
		break;
	case 3:
		if (pdHwPulse(tick, 30)) pad.button = L_TRIG;
		if (tick >= 180 && tick < 300) pad.stick_y = 45;
		if (tick >= 360 && tick < 450) pad.stick_x = 25;
		if (tick >= 510 && tick < 620) pad.stick_y = 45;
		if (tick > 720) pdHwPhase(4);
		break;
	case 4:
		g_MpPlayerNum = 0;
		if (tick == 1) playerPause(MENUROOT_MAINMENU);
		if (tick >= 90 && dialog) {
			menuPushDialog(&g_VideoOptionsMenuDialog);
			pdHwPhase(5);
		}
		break;
	case 5:
		if (!dialog || dialog->definition != &g_VideoOptionsMenuDialog) {
			pdHwPhase(99);
			break;
		}
		if (pdHwPulse(tick, 60) || pdHwPulse(tick, 120)) pad.button = D_CBUTTONS;
		if (tick == 200 && dialog->focuseditem != &g_VideoOptionsMenuItems[2]) {
			pdHwPhase(99);
			break;
		}
		if (pdHwPulse(tick, 240) || pdHwPulse(tick, 420) || pdHwPulse(tick, 600)) {
			pad.button = A_BUTTON;
		}
		if (tick == 260 || tick == 440 || tick == 620) {
			if (!!g_HiResEnabled != (tick != 440)) pdHwPhase(99);
			else g_PdHwToggleChecks++;
		}
		if (tick > 720) pdHwPhase(6);
		break;
	case 6:
		if (!dialog && tick > 90) pdHwPhase(7);
		else if (pdHwPulse(tick % 90, 30)) pad.button = B_BUTTON;
		break;
	case 7:
		if (pdHwPulse(tick, 60) || pdHwPulse(tick, 150)) pad.button = L_TRIG;
		if (tick % 600 >= 200 && tick % 600 < 290) pad.stick_x = 35;
		if (tick % 600 >= 360 && tick % 600 < 450) pad.stick_y = 45;
		if (tick > 1800) pdHwPhase(8);
		break;
	default:
		break;
	}
	index = first;
	do {
		index = (index + 1) % 20;
		for (i = 0; i < 4; i++) {
			samples[index].pads[i].button = i == 0 ? pad.button : 0;
			samples[index].pads[i].stick_x = i == 0 ? pad.stick_x : 0;
			samples[index].pads[i].stick_y = i == 0 ? pad.stick_y : 0;
			samples[index].pads[i].errno = 0;
		}
	} while (index != last);
}

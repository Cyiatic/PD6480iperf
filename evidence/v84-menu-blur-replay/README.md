# v84 isolated menu diagnostic — original N64 and software

Private source branch diagnostics/v84-menu-blur-replay, commit 0ad993ef7.
ROM SHA256 97eaf57d8f59e026b9f7c540f162633d9719b1b0e6ee3aca539e26b19ec4e175.
ELF SHA256 a2c03761fc837cefa29cb40b72bf009ad647e9a7f0ebb1c6e70abad5cae6d416.
CRC1/2 93c5bdb0 / 2d783879.

NOT THE DISTRIBUTED NORMAL ROM. It adds synthetic input, programmatic file/menu
setup, a mutable stock Dark save in RAM, physical Controller Pak write blocking
and the prior startup watcher. The old yellow HUD prefix still reads V82HTEST;
identity is established by the uploaded v84 diagnostic hash and fresh capture.
Its menugfx.c/mainmenu.c are identical to normal v84, verified by git diff.

Replay phase9 exercises right/left/right/left file-menu swipes before selecting
Dark; phase3 walks/turns and toggles L; phase4 pauses and repeats both swipe
directions; phase5 displays the non-interactive fixed-resolution label and
cycles L; phases6/7 return to gameplay and move; phase8 is completion. CHECK1
now means the label check, NOT an old Hi-Res checkbox-toggle count.

Fresh software6500 ticks: phase8, CHECK1, CI frame3527, no OOM,640x480, graph on,
unpaused. See emulator-final.json/png. This software result is not hardware.

## N64 upload and fresh Elgato inspection (Phoenix, 2026-09-06)

First attempt worker17808: on09:39:36.515, upload13272 times out65s; OFF/status
09:40:55.010/.870. No test pass. Retry worker20820: on09:42:00.980, upload26820
09:42:13.100 to09:42:49.904 native0. Capture21520 starts09:42:49.960.
Fresh recording starts09:43:25; observation is bounded300s after45s startup.

Inspected hardware-retry stills:

- Segment1 12s: file menus after a swipe, full-screen blur and eyepiece.
- 40s: CI gameplay after file selection; 85s: L graph on.
- 118/125s: different paused menu pages with full-screen background, no old
  quarter-screen fragments. The current view faces a dark wall after movement.
- Segment2 10s: Video Options visibly reads 640x480i (fixed).
- Segment2 25s: returned to Perfect Menu; 65/100/145s: returned to gameplay,
  graph visible, changed view at the wall. No crash/timeout screen appears.

This establishes scripted hardware progress into and out of the menus with
the rendering fixes; it does not validate physical controller input on the
normal ROM or external save import, nor does composite capture pixel size by
itself prove internal render resolution.

Capture ended09:48:36.255, OFF/status09:48:37.697/38.362. Independently queried
Plug1 again after inspection: Relay0. No GameCapture/UNFLoader/host processes
remain. Only Plug1 was addressed; never the unrelated N64 outlet.

Five exact recording/metadata files (579409046 bytes) permanently deleted
after inspection09:50:03; only OverlayTimeline.json176bytes remains in
Timeshift. Retained full stills and small logs. Removed video hashes:

- segment1,290898604bytes:24346318c69902a06a6e303e1326a076f9b028252071bf4f58efec091a75db2b
- segment2,288345752bytes:19de847bbb183540e37b8ab0f2d786cde74c4830f3c0b6d42250a8916b6368f2

No Analogue v84 test has been reported yet. Hardware save import, multiplayer
and extended mission coverage are not established by this diagnostic.

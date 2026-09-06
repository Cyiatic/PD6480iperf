# v84: full-frame menu blur and honest fixed-resolution UI

Runtime commit 762b7e4914749151162d194d6c13a29a19af8ae8, based on normal v83.
Only src/game/menugfx.c and src/game/mainmenu.c change at runtime.

The old 40x30 pause texture sampled 8x8 blocks from only the upper-left 320x240
of a 640x480 framebuffer. Its drawing quad likewise ended at 320x240, leaving
old menu and HUD-piece pixels outside that area. Baseline v83 captures show
those stale fragments reappearing during horizontal swipes.

v84 maps the unchanged 320x240 sampling grid across the front framebuffer's
own bufx/bufy, sampling both axes at 640x480. Source reads use the uncached
alias to observe RDP writes. The averaging work remains 64 reads per output
pixel; no larger blur texture or framebuffer allocation is introduced.
The three overlay quads now span the current full screen. The existing
perspective menu/light effects remain; this does not disable their animations.

Both video menus replace the inactive Hi-Res checkbox with a non-interactive
"Hi-Res: 640x480i (fixed)" label. The stock saved Hi-Res bit remains intact;
there is no new save format or live framebuffer reallocation. The renderer
was already fixed at full resolution in v83 with either preference value.

Actual-C tests check all four quadrants at 320x240, 640x480, 640x240 and 576x432,
output guards, front/back descriptor independence and all three overlay
offsets. Quarter-sampling and quarter-quad negative controls fail. The v83
buffer-order regression test still passes 400 transitions.

Normal v84 cold Dark software boot reaches CI. Same-build states then exercise
Video Options, movement, pause, L off, right swipe, settling and left swipe.
Captured swipes no longer retain v83's stale menu/HUD-piece fragments. RDRAM
checks include the actual blur/UI code, 640x480 dimensions, HAF1 prepared VI
registers and no OOM. Normal N64 upload shows animated intro; isolated diagnostic
tests of the same two menu source files are documented separately in the
private distribution repo's evidence/v84-menu-blur-replay.

ROM SHA256: 401d5507968d5a37756dad280a43d89d481fbbdf21fc79eeaa0edccdfb98c6d7
ELF SHA256: c612d80948e0ecd2d43592ba0cc069f76db4639b366decb0e2540b4d124a6726
CRC1/2: 506e9497 / f674ce96.

Analogue retest, long sessions, multiplayer and broader mission coverage remain
open. Do not restore a v83 savestate into this build. The normal candidate has
no synthetic pad replay, RAM save or diagnostic watchdog linked.

# Normal v84 menu-rendering regression evidence

Runtime source: 762b7e4914749151162d194d6c13a29a19af8ae8,
experiments/v84-fullscreen-menu-blur. ROM SHA256
401d5507968d5a37756dad280a43d89d481fbbdf21fc79eeaa0edccdfb98c6d7.
No synthetic pad input, RAM save or diagnostic watchdog in this normal ROM.

Baseline v83 right-swipe image retains old menu/eyepiece fragments. v84's
pause.png, swipe-right.png, swipe-left.png and video-options.png show a
full-screen blur and fresh menu/HUD-piece image without those fragments.
The normal perspective projection and text reveal animation are still active.
These PNGs are emulator screenshots, NOT Elgato hardware evidence.

Reproduction: cold 5100 ticks with the existing
evidence/v81-v82-modern-memory/headless-cold-briefing.txt and stock Dark EEPROM;
1080 ticks with v83-warm-open-video.txt; 1050 with v84-ci-walk.txt; 300 with
v84-pause.txt; 36 with v84-swipe-right.txt; 180 idle; 36 with v84-swipe-left.txt.
Each continuation uses only the preceding state from THIS v84 ROM. Host uses
cached_interpreter/cxd4/Angrylion, 8 MiB. The eeprom-header test adapter changes
save identification in host memory, not the disk ROM. Pausing after graph-on
captures its green rectangle in the background texture, as stock does; that
single snapshot is distinct from the eliminated stale-frame fragments.

normal-ci-walk.json: CI frame 2219, unpaused, graph on, position
752.99994/483.99957/590.24725. normal-swipe-left.json: paused, graph off.
All checks show 640x480, no OOM, correct resident code and both prepared HAF1
VI slots (ctrl305e,width1280,vSync524,xScale1024,origins1280/2560,yScale1024).
The layout was freshly compiled from v84 headers and matches the previous
unchanged ABI. normal-* reports additionally verify the two blur functions
and fixed-resolution text function in resident RAM.

Actual-C blur tests pass four dimensions, four quadrants, output guards and
three quad offsets; both quarter-screen negative controls fail. Logo-buffer
test passes 400 transitions. Seven inspector tests and four stock-save tests
pass. Static audit: 1403 compressed streams valid, zero invalid; 608 raw assets
unchecked. All 60 pad-cover extents valid. Xdelta round-trip exactly matches.

## Original N64, 2026-09-06 Phoenix

First bounded attempt: Plug 1 on 09:32:42, USB upload timed out after 65 s.
OFF/status Relay0 at 09:34:01/02. No ROM/capture pass for this attempt.

Retry worker15728: Plug1 on09:35:12.989; upload PID29388 09:35:25.143 to
09:36:01.774, native0; GameCapture PID24468 starts09:36:01.815. Fresh video
starts09:36:36. Stills10s black,40s Joanna/city intro,65s spacecraft intro.
Thus normal ROM boots beyond product identification and animates; this does
NOT establish unchanged-ROM interactive hardware gameplay.

Observation ended09:38:02.901; OFF/status09:38:04.403/05.093, independently
rechecked Relay0 before the next run. Four exact recording/metadata files
(161335382 bytes) permanently deleted after inspection. Small stills retained.
Separate scripted hardware menu/gameplay test is in ../v84-menu-blur-replay.

Analogue v84, long sessions, multiplayer and on-device save import remain open.

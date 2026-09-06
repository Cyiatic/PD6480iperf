# v85 blur allocation and mission regression

Normal runtime commit: 21f656613b6e78c248d99dd0359b49b202ba591d,
experiments/v85-blur-allocation. Normal ROM SHA256
430f09bbe0b76bfe687881c52ac23ec4cfff0cc4a16b9ba5faecd602ffc037a4.
ELF81af590340c372b80d4d9c3bcada0056566505a2ce482de4ec11f618a8d0ad5a.
CRC37b134c9/fedfa470. Layout freshly compiled from v85 headers,
SHA2568a48ab7fa3f24dc9b2e9419d01cd150a1485cd8b6f6bb0f2d5b497c279a71d69.

## Change and reason

v84 fixes full-screen pause sampling/coverage and makes the fixed 640x480i
mode explicit in Video Options. Follow-up mission testing found a real v84
Defection preload failure (room167 missing,61328-byte request), recorded in
../v84-mission-regression. Preserve this failure alongside the earlier CI pass.

The sole blur producer and consumer both use40x30 RGBA16,2400bytes, but
menuReset reserved0x4b00,19200bytes. v85 shares the dimensions/byte count in
menugfx.h and allocates ALIGN16(BLURIMG_BYTES), returning16800bytes to the
stage heap. Blur appearance, full640x480 sampling/coverage, framebuffer/depth
size and room/weapon preload policy are unchanged. No resolution reduction.

## Normal-ROM software tests (not hardware)

Cached interpreter/cxd4/Angrylion,8MiB,eeprom-header host save-ID adapter.
Cold5100 ticks with the recorded cold-briefing input and stock Dark save.
All continuations use only this v85 cold state's lineage, never v84 states.
No RAM writes, synthetic in-ROM input, RAM-save shim or diagnostic watchdog.

At cold completion, Skedar Overview is open. B then five downward pulses
select Defection (v85-overview-to-defection.txt,450ticks). Mission selection
was visually verified. Launch with v84-launch-selected-mission.txt,1500ticks.

- Defection/Perfect Agent: stage48,frame223,unpaused,all167 expected rooms
  loaded,OOM0,4464bytes expansion-stage free. This fixes the v84 missing room.
- Defection move/fire/pause/both swipes:600ticks,frame372,pause3,OOM0,
  all167rooms,4176bytes free. Pistol ammunition8->5,position changes to
  337.00665/158.99957/-31.570055. The entire background is blurred.
- Resume/L/move/fire and idle:1500ticks,frame1194,pause0,OOM0,all167rooms,
  4176bytes free,ammo5->2,position788.99994/-441.00043/54.47029.
- Air Base selection: nine downward pulses from this v85 Defection list,
  visually confirmed. Same1500tick launch:stage39,frame174,pause0,all146
  expected rooms,OOM0,18688bytes free (v84 initial observation6240bytes).
- Air Base move/fire/pause/both swipes:600ticks,frame289,pause3,OOM0,
  all146rooms,15872bytes free; paused background covers the full viewport.

Exact stage/frame/health/ammo/rooms/VI/resident-code values are in the JSONs.
Both normal mission samples retain640x480 buffers and HAF1 VI settings.
These are short functional checks, not whole-level or whole-game completion.
Defection's remaining memory margin is small; long sessions and multiplayer
remain unverified. No Analogue3D v85 claim is made here.

## Code and asset tests

Actual C regression checks allocation2400bytes,4source dimensions,4quadrants,
output guards and3full-screen quad offsets. Deliberately restoring quarter
sampling, quarter coverage or0x4b00allocation makes the controls fail.
Actual logo routine passes400buffer-order transitions;7inspector and4stock
save tests pass. Compressed asset audit1403valid,0invalid,608rawunchecked.
All60pad-cover extents valid. Xdelta encode/decode exactly reproduces ROM hash.

## Normal ROM on original N64

Bounded worker7596,2026-09-06Phoenix: Plug1ON10:17:30.421; ED64 upload
10:17:42.606..10:18:20.248,native0; GameCapturePID10184 starts10:18:20.307.
Fresh segment begins10:18:55. Inspected still25s shows city/spacecraft,
55s shows Joanna at the skyscraper. Animated intro beyond product screen.
This is NOT unchanged-ROM interactive hardware gameplay proof.

Observation ended10:20:21.435,Plug1OFF10:20:22.885,statusRelay0
10:20:23.796,and independent status recheckRelay0. Four exact inspected
recording/metadata files permanently deleted,160842634bytes; small stills
and segment description retained. The unrelated N64-named switch untouched.

## Separate diagnostic development

Heavy diagnostic ROM ffaf5d9f5234144103e004327b67567eda1ca52c707b34ed9340c4d7d6bfe913,
source c4f981bcaf6ec9aae773fe3cded8c99fe92baed5. Fresh software7800ticks:
Defection1499frames,phase8,all167rooms, but OOM'p',8064-byte request,
1472bytes free. This is NOT a memory pass and was NOT uploaded to N64.
Its code/BSS increases the first heap address by14256bytes versus normal.

The lean diagnostic removes the old startup watchdog thread/8192-byte stack,
watchdog code and main-thread heartbeat calls. main.c, menu.c, menugfx.c,
bg.c and memp.c then match normal v85 source exactly. Replay/HUD/RAM-only
stockDark and Controller Pak write blocker remain diagnostic-only. The
heap-address overhead is3728bytes instead of14256.

Lean diagnostic704055eb04069696128703a833bbb6cdf194a61f3d200d0f035a590fb8bef8df,
source c5bedbd14dfefc04f6774fdda0065f03717b2e42, also reaches phase8 but
reports OOM'p'/8064bytes,720bytes free. Not uploaded to N64. A compiled-offset
probe finds room167's vtxbatches pointer is NULL in both diagnostics. Counting
non-NULL gfxdata alone overstates their room readiness. The normal v85 final
Defection dump has every room's batch pointer, including room167 at806e8320,
252batches (8064bytes), and OOM0. See room-batch-comparison.json. The failed
diagnostics do not validate Defection on hardware; normal-ROM software and
normal-ROM hardware-intro evidence remain separate.

The console menu test instead uses a separate CI diagnostic where memory is
not this constrained, based on v84's successful CI replay plus the exact v85
allocation change. Source cd49d53f915b58be90bf5a2ca8990ef4977ef38f,
diagnostics/v85-menu-blur-replay. Its menu.c,menugfx.c,mainmenu.c,menugfx.h
are identical to normal v85. ROM
9a10e80a1fe3d37095e84d0d5a25ad8fd194c133b804b78a0e2609a708b7c051,
ELFc307b10373e42bd999bcf911557e2e5c4cdf1d7e7ac34adfef42752a9c207a3e,
CRC58520ea1/7b22c6b5. This includes the old watchdog, RAM-only stock save,
programmatic setup and synthetic input; it is NOT the distributed normal ROM.

Fresh CI software6500ticks finishes phase8,CHECK1,stage38,frame3527,
pause0,OOM0,640x480,333776stage-heap bytes free. See diagnostic-ci-final.json/png.

## CI diagnostic on original N64

Worker24816,2026-09-06Phoenix: Plug1ON10:33:26.174; uploader28032
10:33:38.323..10:34:14.914,native0; GameCapture25632 starts10:34:14.971.
Fresh Elgato segment1 begins10:34:49; segment2 begins10:37:25; segment3
begins10:40:01. Bounded observation330seconds after45seconds startup.

Inspected stills in hardware-ci-attempt1:

- Segment1,12s: file-menu swipe, full-screen blur and eyepiece.
- 40s: CI gameplay with menu transition clearing;85s: L graph visible.
- 118/125/140s: changing pause-menu pages and normal perspective/reveal
  animation; full-screen dark blurred background, no stale quarter fragments.
- Segment2,10s: Video Options shows Hi-Res:640x480i(fixed).
- 25s: Perfect Menu;65/100/145s: resumed gameplay facing the wall, L graph.
- Segment3,15s: gameplay remains active, graph changes; no crash screen.

This is scripted CI hardware verification, not hardware Defection/Air Base,
not unchanged-ROM physical controller verification, and not save-import proof.
Composite capture dimensions alone do not establish internal render resolution.

Observation ended10:40:30.474; OFF10:40:32.153,statusRelay0
10:40:32.852; independently recheckedRelay0. No owned capture/uploader/host
process remains. Seven exact inspected recording/metadata files permanently
deleted,635107698bytes. Only177-byte OverlayTimeline.json remains in Timeshift.
Total recordings removed across this continuation:795950332bytes. Small
stills, segment descriptions, hashes in trial logs and OFF checks retained.

Analogue3D v85, long sessions, multiplayer and on-device save import remain open.

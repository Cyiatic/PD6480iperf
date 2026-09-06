# v82h buffer-order fix — original N64 reaches gameplay

2026-09-06 America/Phoenix. Private source b7bb32669,
diagnostics/v82h-preserve-buffer-order. Normal v82b remains separate; this is
a scripted-input/RAM-save/watchdog diagnostic. Fix: preserve front/back indices
when titleExitCheckControllers calls viConfigureForLogos mid-frame, initializing
0/1 once at boot. See v82g evidence for the exact hardware FIFO deadlock.

ROM SHA256 50ee8e8961375075c12e34728efa3cbbe693d294b9632e3b9cd2ef1564a71213.
ELF SHA256 214fb5b644b0e373085ecbefd759f19985f05ed2561eb255f57be54cb1154531.
CRC1/2 169f7d2e / c401bb29.

Compiled actual routine: 400 transitions for both parities and K0/K1 aliases,
old reset negative control rejected. Fresh emulator: 6900 ticks, phase 8,
three Hi-Res checks, Hi-Res/graph on, CI frame 4316, unpaused, no OOM. Full
640x480 and prepared HAF1 values are in emulator-final.json. This is software
state evidence, not proof from the composite capture's pixel dimensions.

## First bounded N64 run

Worker PID 15020 started 08:15:47. Plug 1 ON 08:15:49.802, uploader PID 24812
08:16:01.952 to 08:16:38.574 (native 0). Owned capture PID 7012 started
08:16:38.634; fresh recording began 08:17:11. Stills:

- 5 seconds: Carrington Institute menu, phase 2.
- 30 seconds: menu closed, phase 3, FPS graph visible.
- 65 seconds: different view/location by the blue bench after scripted movement.
- 95 seconds: Video Options, phase 5, before all three checks.

No timeout screen. This is direct physical progress past the previous
title-deadlock checkpoint into CI and movement, not merely a logo pass.
It uses synthetic pad samples and programmatic file/menu setup; it is not
unchanged-ROM physical-controller or external save-import validation.

Capture stopped 08:18:54.715, OFF Relay 0 08:18:56.171, status Relay 0
08:18:57.032 and independently rechecked 08:19:09. Recording 191973192 bytes,
SHA256 781d00b37949f2a4b074ed68ad580b0b40b984aadb0cbb1d2162c51ead942b4c.
Three inspected recording/metadata files permanently deleted, 192026900 bytes.

## Extended replay

A second bounded run of the SAME ROM began 08:20:15 as PID 22916 to observe
all frame-based toggle/movement phases. The updated worker allows a selected
360-second observation, hard overall deadline 660 seconds, and owns cleanup.
Disk headroom before start was 23933730816 bytes. Only Plug 1 is addressed.
Plug 1 ON 08:20:18.493. Upload 08:20:30.618 to 08:21:07.778 (native 0),
owned capture PID 14148 started 08:21:07.832; video began 08:21:41.

At segment 2 / 15 seconds, full still and nearest-neighbor enlarged HUD crop
show phase 7, HI 1, CHECK 3 after returning from Video Options to gameplay.
The crop is only an inspection enlargement of recorded pixels, not generated
text. Thus all three scripted Hi-Res menu checks have passed on original N64;
the replay remains a modified binary. Normal v83 applies only the VI fix and
must be tested separately. No Analogue compatibility claim follows yet.

Segment 2 at 90 seconds shows a different room view/position with phase 7,
HI 1/CHECK 3. Segment 3 at 25 seconds shows phase 8, HI 1/CHECK 3 and the FPS
graph. Phase 8 is replay completion; normal gameplay keeps rendering. This
bounded diagnostic completes movement, L-driven graph cycling and all three
Hi-Res checks on original N64, using the real game input/menu consumers but
synthetic inputs and RAM-only stock Dark save. No freeze/timeout appeared.

Observation ended 08:27:53.292; capture stopped. OFF command and status both
confirmed Relay 0 by 08:27:56.395, independently rechecked 08:28:00. Three
recording segments had bytes / SHA256:

- 290851040 / 431cb355ea8ec4c5bd33ffcb4c966cf148c65842e73687650e7cafc91f2e65ed
- 290813628 / 1c23a10d22d1cd286638088d0f0cce2601ed413e89e4f556c6733a893e43a3e7
- 110851004 / 0cd3af6dd82f510c2d37a32257a3fcf30c7c3a1edc1348116c85ea833f27813a

After inspection, all eight exact recording/metadata files permanently deleted
(692709953 bytes). Small stills, two labelled HUD enlargements, manifest and
power/worker logs remain. The normal v83 ROM test starts only after this cleanup.

# v86g scope and remaining verification audit

Rechecked September 7, 2026 UTC. This is an audit of the unchanged delivered
candidate, not a new version or declaration of completion.

Runtime HEAD is `26cb92ae9d0ae2cba172999c0d5c1762f32d5a50`.
Tracked runtime files are clean. The two untracked native build tools remain
untouched. Distribution source has unrelated dirty files; they are not part
of this audit or its commit. Normal ROM SHA256 remains
`79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`.

## Requirements and evidence

| Requested result | Current evidence | Status / limit |
| --- | --- | --- |
| Genuine 640x480i using Expansion Pak | Normal-ROM Deep Sea RAM report authenticates resident functions, two colour buffers at 8036a000/8076a000, depth at 80400000, active dimensions 640x480. Runtime video480i.h and vi.c contain full-size buffers and NTSC HAF1 interlaced field registers. | Implemented and software-observed. Elgato-processed output is not a direct VI-register measurement or an Analogue result. All 8 MiB is already available. |
| Newer performance code, not a lower-resolution substitute | Git confirms bf3245076d00fbbb29ca1e0906672381f2d43a52 is an ancestor. Compared with that base, chr.c, chraicommands.c, bondmove.c, dma.c and mtx.c are unchanged. Rendering/menu/memory/scheduler changes are separately documented. | Modern core retained. Extra buffers cost 1,280,000 bytes; retained texture warmup and budgeted room residency replace guaranteed whole-geometry preload. No measured console speedup is claimed. |
| L-toggle FPS graph | Normal-ROM Deep Sea frame-300/frame-600 images show hidden/shown graph. Labelled real-N64 replay images show both states. | Verified in those bounded scopes; normal physical-controller/Analogue v86g result is still missing. |
| Full-screen pause blur and correct horizontal menus | Normal Deep Sea pause image and labelled N64 pause images show full-view blur; menu directions exercised. Relevant actual-C tests are recorded. | Scaling/clearing fixes implemented; ordinary perspective/eyepiece animation remains intentional. Current-build Analogue confirmation is missing. |
| Stable resolution option | UI now states Hi-Res: 640x480i (fixed). Normal RAM reports full dimensions with saved hires preference zero. | No resolution transition or redundant checkbox. This must not be described as selectable low/high resolution. |
| Real-N64 boot into gameplay | Normal retail-ID ROM uploaded and rendered city/ship/rooftop intro. Separate labelled diagnostic reached Infiltration, alive pause/navigation/L and brief resume before ordinary combat death. | Partial: the diagnostic is not the normal ROM. Normal physical-controller gameplay is not proved. |
| Working on Analogue 3D | Earlier candidates had user feedback, including failures. No result has been received for this exact v86g hash. | Open external verification, not a pass inferred from software or original N64. |
| Stock-format 100% save named Dark | Packaged matching-name 2048-byte EEPROM, stock decoder/re-encoder and checksum tests; normal software load and RAM-only hardware diagnostic load. | Included and format-verified. Physical import is unverified; existing cartridge saves were not overwritten. |
| Private PD6480iperf repo | Private Cyiatic/PD6480iperf; runtime and distribution branches pushed. New bounded co-op/four-player evidence reached distribution commit 4746abfc914edfa8e79b226e59f50fef072c229f. | Delivered source/patch/save/evidence; normal ROM remains local, not in Git. |
| Plug 1 power workflow and recording cleanup | Exact device logs confirm ON/OFF around prior tests; latest completion power status is Relay0. No owned capture/uploader/test process remains and Timeshift holds only its 307-byte timeline. | No unrelated N64 switch control. This audit starts no new capture. |

The normal-ROM software matrix covers 21 mission initializations, not 21
playthroughs. Co-op/four-player and Deep Sea exercises are bounded checks.
Sustained play and a controlled performance comparison remain unverified;
they must not be implied by passing initialization or source ancestry.

## New finding: an idle console capture cannot close the gameplay gap

The unchanged normal runtime title path was inspected directly:

- `title.c:titleInitRareLogo` enables `g_IsTitleDemo`.
- `title.c:titleInitSkip` sends that demo to Defection rather than CI.
- `player.c:playerEndCutscene` sends a title demo back to `STAGE_TITLE` instead
  of entering normal movement. `chraicommands.c:aiEndLevel` also returns a
  title demo to the title stage.
- `lv.c` clears demo mode after a real controller button/stick event.
- Normal `joy.c` reads the physical N64 controller through
  `osContStartReadData`/`osContGetReadData`. It is unchanged from the modern base.

This explains why an intro followed by logos is consistent with normal attract
behaviour; it does not retrospectively prove the exact state of a captured
hardware frame. Repeating or lengthening an idle upload is not a substitute for
normal-ROM interactive evidence. Adding another ROM input shim would again be
a diagnostic, not the delivered normal candidate.

Current Windows enumeration shows both exact ED64 FTDI
`USB\\VID_0403&PID_6001\\AB0NWMD3` and Elgato
`USB\\VID_0FD9&PID_0051\\110B14E2A7` present/OK. Presence alone is not an upload
or video pass. The reviewed local trial worker offers upload/capture/power,
not physical controller input. No callable N64 controller transport was found
in the enabled tool inventory. This is a verification/control gap, not a
reason to request another USB cable or change the power switch.

After this read-only audit, exact Plug 1 was explicitly switched OFF again
at 03:36:05 UTC and independently reported Relay0 at 03:36:06 UTC. Logs are in
`completion-audit-power/`; no new recording or test process was created.

## Next discriminating evidence

Keep this exact candidate unchanged pending controller-driven v86g results:
normal gameplay, left/right menu navigation, pause blur and L on Analogue
and/or the normal original-N64 build. The nonblocking request for the v86g
Analogue result has already been sent; no affirmative reply is assumed.
If it fails, retain the exact ROM filename/hash and failure screen/context
before selecting another source change. No new defect was established by
this audit, and no additional idle capture was launched.

The overall goal remains active and unproven. The preceding goal turn verified
the completed private evidence push. This turn adds the source-grounded
attract-loop finding and requirement audit; it is not a verified wait on a
running process. All test handles are terminal or absent. The external
current-build hardware-result condition is recorded here for its first
explicit blocking audit; do not mark the goal blocked on this first audit.

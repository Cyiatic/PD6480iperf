# v86g completion-message reserve — development evidence

The v86f Extraction stall has an observed software failure chain. This is not
an Expansion Pak allocation failure. v86g changes only the scheduler's advisory
main-thread retrace notifier, reserving two slots for the two outstanding graphics
tasks' completion messages. No buffers, room budget, priorities, interrupt
handlers, task state bits, or emulated timing are changed by the ROM fix.

## Failure captured without modifying the game

The unmodified local build of ParaLLEl N64 commit
`2f3bf60dcd969ae13e60731eab681504256272db` reproduces the original normal-v86f
Extraction frame-3 stall. A bounded read-only observer added to that emulator
also reproduces it; the final 8 MiB RAM SHA256 is identical in both runs:
`42c3becbc18be3e7b99f870a6aa3761f8cc10977d481b8fcc846ab5372221d5e`.
Both complete the 3000-tick host run with native exit 0 and stale video callback
count 453. Native success is not game progress.

The observer authenticates the exact normal-v86f kernel enqueue instructions
and reads addresses from its ELF/compiler-derived ABI. It writes only bounded
host stderr. It does not alter guest ROM/RAM/registers, event queues, CP0 count,
RCP flags or retry/drop policy. The additional logging consumes wall time;
matching failure and RAM are the control for its relevance here.

The [machine-checked chain](observer/queue-chain.json), from
[the full bounded log](observer/queue.host.log), is:

1. Event 1158: the scheduler tries to send graphics DONE to main's 32-slot
   queue, already full. The existing blocking send parks the scheduler.
2. Events 1161–1168: eight VI/retrace notifications fill the scheduler's own
   eight-slot interrupt queue while main builds the next frame.
3. Events 1184–1190: the next graphics SP completion is raised and acknowledged,
   but the kernel's full-queue branch discards its notification. All eight slots
   contain retrace handler pointers, not completion messages.
4. DP completion is subsequently handled; no later SP handler appears in the
   bounded log. Final state is Extraction frame 3, graphics RSP state `0x12`,
   no current RDP owner, another graphics task queued, and no allocation/cache
   failure or CPU exception. The missing completion leaves the task outstanding.

The kernel branch was disassembled from normal v86f: at `0x80003230`, the
`validCount < msgCount` result selects enqueue or the existing discard return.
This identifies an actual game queue-loss mechanism in this software sample,
not a speculative missing emulator interrupt. It does not prove this precise
occurrence on N64/Analogue or exclude other failures.

The queue log reaches its 8192-event cap later in the stalled state. A separate
2308-event [first-frame trace](observer/frame1.host.log) captures the same SP
loss without reaching its cap. The first observer attempt included loading
frame zero and exhausted its cap before the failure; that attempt is not used
as negative evidence. An initial host launch without the runtime DLL PATH
failed before emulation (`0xc0000135`); the corrected runs above are distinct.

## Provenance and rebuild

Normal v86f ROM/ELF:
`bf219fa49620be957f366cb2b84ba255d67712bb36faf3e494ddfabfae7fa41e` /
`82d6a0e7ffe479c2eb2e2b11efa9b992c0493d58ca4688dbf9be5804328d2511`.
All observer runs use the same old v86f solo menu seed
`9b6e2347ffc3b67e62e8bea7f1e4b6268b9cac71b86811ba000aa8f3f85aec82`,
the 3000-tick extended input
`44381bb9e452cb978626d17a2f49a000929cf63398f5ad398733ff4510ef83df`,
controller mask 15, cached interpreter, Angrylion/cxd4, no RAM writes, and
SAVE `-`. The usual in-memory ED EEPROM header adapter is identical across
controls. No foreign-ROM state is restored.

Local baseline core SHA256:
`1d4347381543830be9027ec36ea817f74373d83d1194375aa5f7df4f5a38a3df`.
First-frame observer core:
`c6430305057b9b969d075dab0a0c66c5507cc748e794b09089084cd6042290c7`.
Queue observer core:
`319f701e2c475e2174cb4116e2efd50ab7e7ddba1ce95848a6530ac5045b4957`.
The [observer patch](observer/parallel-2f3bf60-pd-observer.patch) applies to the
exact public commit above. These core binaries remain local, not in Git.

Build from its checkout with native MinGW tools and NASM on PATH:

```powershell
make.exe -j 4 platform=win64 ARCH=x86_64 UNAME=MINGW64_NT-10.0 `
  HAVE_OPENGL=0 HAVE_PARALLEL=0 HAVE_PARALLEL_RSP=1 HAVE_THR_AL=1 `
  'SHELL=busybox.exe sh' CC=C:/msys64/mingw64/bin/gcc.exe `
  CXX=C:/msys64/mingw64/bin/g++.exe AR=C:/msys64/mingw64/bin/ar.exe NASM=nasm.exe
```

Set `PD_OBSERVER=1` only for the observed run. The original downloaded core
and local baseline are not bit-identical; the baseline reproduction is required
and recorded. The hardware candidate does not contain the observer.

## Fix and verification gates

Scheduler is the sole producer of main's queue; main is a consumer. Advisory
retraces stop at `msgCount - 2`, leaving room for both outstanding graphics
completions. A concurrent main receive can only increase available space.
Completion messages retain the existing lossless/blocking code path; this fix
does not invent completions, clear ownership early, or retry kernel interrupts.
Boot still gets retrace wakeups, and the existing main loop limits gameplay to
two outstanding graphics tasks. No additional queue storage is allocated.

[The actual-C invariant test](queue-invariant-tests.log) passes 93 slow-consumer
states, boot notification and 500,000 queue interleavings. Reducing the reserve
to one or zero fails the expected completion-capacity assertion. The existing
actual-C graphics-idle ownership/priority test also passes with its negative
control rejected. The freshly compiled v6 ABI is byte-identical to v86f:
`a62708d1ec9097dc0688cd43aff0b594513b7b7af92cf6cf6dcd6d590c5aabdd`.
The historical `audit_480i_elf.py` allocation-call scanner is inapplicable to
this fixed-address-buffer runtime and rejects it; this is not recorded as a
passed audit. Runtime dimensions and partition inspection remain required.

v86g source-header ROM/ELF:
`0474d95e44bb7dd1a47683e4f8bf484a2b1c54c8f4d4746566059ec0a0961e46` /
`07595b1d4c7466bf3ac53f1df29bc21779c8d494eb41978a2c47d735e84ac010`.
Retail-ID ROM:
`79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`.
Only header offsets `0x3c` and `0x3f` differ; the body is identical, as recorded
in [normalization evidence](retail-header.json).

## New results

The continuous cold-four software regression now reaches Extraction frame
**1436**, Solo/Perfect Agent, alive with full health, unpaused, out of the
cutscene, with the game confirming all four controllers connected. Both active
dimensions and player viewport are 640x480, graph enabled. No allocation,
room-load, heap or CPU exception is reported; room partition is valid and there
are no missing visible rooms. The final image was inspected: dark scope/HUD
view with the live graph, like the earlier passing controls. This does not
certify all visual effects, movement/combat or the whole mission.

This uses the original downloaded core (not the observer), no state restore,
no RAM writes, the unchanged Dark EEPROM and the exact prior 9150-tick cold
input (`7f6e87ef409672360b908244c43ded7b0777ea1b08036aa6d496eb031cef763d`).
The source-header ROM uses the same in-memory EEPROM adapter as prior controls.
Native exit 0; video callbacks advance to 7081 by host tick 9000. See
[RAM report](extraction-cold-four-report.json),
[ownership snapshot](extraction-cold-four-gfx.json),
[terminal log](extraction-cold-four.host.log) and
[final image](extraction-cold-four-final.png).
State SHA256 `f07501488211b01b738482b86c90bd6ffde230ff84f7975a2ea408110eabde77`;
RAM SHA256 `571a130bbb1289219378d318eec5603c8506d85c85093d1368b46e2f9902863f`.
The previous normal-v86f cold-four frame-3 failure remains a failure.

Normal retail-ID v86g uploaded to the original N64 in 35.81 seconds. Inspected
Elgato stills show moving city/ship/rooftop intro, then a Nintendo logo. This is
real rendered 3D past boot, **not interactive normal-ROM gameplay or Extraction
on hardware**. See [the exact hardware observations](hardware-normal/inspection.md).
Plug 1 OFF/status Relay 0 verified. The inspected recording and its two
sidecars were permanently deleted, reclaiming 157,349,816 bytes; small stills
and logs remain. No unrelated switch was controlled.

A v86g patch-and-Dark-save test bundle is now packaged after the later checks
below; this is not a full-game release. Sustained play, broader co-op/multiplayer,
normal-ROM physical gameplay and performance checks remain outstanding.
A same-layout zero-reserve control also passes this cold sequence;
see [the result and limitation](noreserve-control/README.md). Thus its pass
alone does not isolate the queue policy's effect; direct old-ROM queue-loss
evidence and actual-C saturation tests remain the basis of the change. The existing generated
stock 100% Dark EEPROM is unchanged.

## Labelled console replay and save-preserving regressions

A separate `V86G TEST` Agent replay was uploaded to the original N64. Inspected
Elgato footage shows alive Infiltration pause/navigation, full-screen blur,
the fixed-resolution label, L graph hiding/reappearing, and resumed 3D. Ordinary
enemy damage then kills the unattended player. This is a short labelled test,
not sustained play or uninstrumented physical-controller validation. The first
upload timed out; the successful retry is recorded separately. See
[hardware observations and cleanup](hardware-infiltration-agent-retry/inspection.md)
and [the software replay and static safety audit](replay-software/README.md).
Physical EEPROM is redirected to RAM and Controller Pak writes are blocked
only in that diagnostic; four deliberately unsafe audit controls are rejected.
Plug1OFF was verified and 403,517,894 bytes of inspected recording/sidecars
deleted. No recording is retained here, only small stills and logs.

A fresh normal-v86g four-controller cold boot produces an authenticated Solo
Mission Select seed with Defection visibly selected. The new matrix preserves
that seed's full 296,960-byte save image and connected-controller mask, rather
than silently substituting erased save memory. See
[seed provenance](solo-cold-four-seed/README.md). The ordinary-input Extraction
continuation reaches frame1586, alive/full-health, unpaused, no cutscene, full
640x480, graph on, no allocation/cache/CPU faults. Its initial frame106 sample
was still an opening cutscene, not the old frame3 stall. The initial sample is
retained. The completed [33-sample mission matrix](mission-matrix/README.md)
now has21/21 final initialization gates and unpaused samples,19/21 alive.
G5Building and Duel end in ordinary unattended combat death, retained as such.
All21 final images were inspected. This is startup coverage, not playthroughs.

The normal-ROM [Deep Sea exercise](deepsea-exercise/README.md) additionally
moves, fires(ammo8to5), pauses/swipes with full-screen blur, resumes, and hides/
shows the L graph. Finalframe1007, aliveHP1/unpaused, full640x480, no allocation/
cache/CPU faults. This is short software gameplay, not an Analogue or benchmark
result. Sustained-play and broader mode coverage remain outstanding; the
subsequent bounded co-op and four-player results are recorded below.

The expanded tool suite passes 52 unit tests, including rejecting changed save
images/controller identities and distinguishing initialized, alive and unpaused
samples. Actual-source C blur/reservation/scheduler checks pass again, and four
stock-Dark save tests pass. None of these substitutes for gameplay evidence.

## Candidate package and final shutdown

See [candidate instructions](../../artifacts/PD6480iperf-v86g-README.md).
The1,447,194-byte xdelta decodes against the user's clean USA1.1 ROM to exactly
the normal retail-ID v86g hash above. The normal `.z64` stays local; the ZIP
contains only xdelta, matching-name stock Dark EEPROM, README and manifest.
All four ZIP entries were read back and hash-compared with their source files.
ZIP size1,451,933bytes; SHA256
`f831a1335a425a62b5cdf89e6482a6b4f5bd903ebe89e3cbb73fdb8610417b93`.

Plug1 was explicitly switched OFF and status returned Relay0 again at
2026-09-07 02:52:10UTC. The exact action/status logs are in `candidate-power-off/`.
No owned uploader/capture/emulator test process remains. Timeshift contains only
the307-byte OverlayTimeline.json; inspected recordings were already deleted.
The unrelated N64 switch was not controlled.

## Additional checks on the same delivered ROM

The unchanged v86g ROM now passes the earlier
[AI-co-op Infiltration memory-pressure fixture](coop-watch/README.md):
finalframe635, Agent, one AI buddy, aliveHP1/unpaused,640x480, zero OOM/cache/
heap/CPU faults.17evictions,8idle reuses, no read-only failure-watch events.
The paused full-screen blur and final graph-hidden gameplay images were inspected.

A fresh same-ROM cold seed also passes a short
[four-player Skedar setup/movement/pause/resume/L check](four-player/README.md).
All four final players are alive/unpaused, with distinct viewports/positions,
full640x480 output buffers and no allocation/cache/CPU faults. These results
do not establish every arena, weapon, human co-op mode or sustained play.
No ROM or delivered ZIP was changed to obtain these additional results.

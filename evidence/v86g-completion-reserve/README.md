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

No release or new user-ready bundle is promoted by this document. Broader
regressions, sustained play, physical gameplay and performance checks remain
required. A same-layout negative control would further separate the new
runtime's code-layout shift from the tested queue policy. The existing generated
stock 100% Dark EEPROM is unchanged.

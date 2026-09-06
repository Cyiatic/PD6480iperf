# v86c — reserve all pending CI menu scratch

Based on normal v86b runtime ea2ad550b, docs b9cae2632. Code ab2c7e906.
Normal ROM 5c730fd1470b5fd98e27ea59ebf04d2db7d3716cb6176c8b16d4ff36fb694a2b;
ELF ccf19515ea7d7005bef2b49428802959878bd691f2f6a8a601e2a6f2b354c583;
CRC3012086e/06f2d148. Experimental; not distributed or hardware verified yet.

Normal v86b with four libretro controllers reaches Combat Simulator, all three
additional controllers waiting, Quick Team/Players Only and Game Setup without
OOM. Choosing Finished Setup invokes Quick Go menu contexts while CI still has
PLAYERCOUNT1. Its153600-byte reserve is enough for only one lazy menu buffer.
Final Quick Go snapshot is still CI38 and already has OOM'p'/153600; the later
Skedar arena50 retains that global error marker. It must not be misdiagnosed
as an allocation that first failed in the arena. Actual arena has only one
active player because the other menus could not open. No four-player pass.

menuReset configures all four g_Menus[].unk840 capacities in CI. menuPushDialog
allocates each lazily, independent of active gameplay player count. v86c's
bgGetLateAllocationReserve sums the aligned capacity of each still-unallocated
menu context, in addition to128KiB general headroom. Already allocated scratch
is not reserved twice. Other stages keep the same128KiB budget and runtime.
It does not change640x480 buffers, AI, gameplay, menu rendering or L behavior.

The actual extracted C helper passes all-four/pending-only/alignment tests and
leaves99 other stage IDs unchanged. The former one-player helper fails the
negative control. Normal build succeeds. Cold matching-build test with external
stock Dark and four real frontend ports passes CI startup; no foreign state is reused.
The software frontend has independently tested per-port inputs and a candidate-
compiled v5 read-only layout for every player. This is not hardware evidence.

Completed normal-ROM chain reaches four Quick Go panels with OOM0 and124976
bytes free, then Skedar with four living, unpaused players and four independent
viewports inside640x480. Subsequent per-port forward/Z inputs move all four
players without OOM. This is a short software sample, not a whole match.

The first mission-list seed was later proven to be CO-OP, not solo. Compiler-built
v6 bit-field probes identify cooperative=true and one AI buddy in the failing
Infiltration/Deep Sea continuations. Their original "solo-matrix" directory name
is misleading and retained only as provenance. They are not solo regressions.
Fresh, mode-verified solo Defection/Infiltration/Deep Sea samples pass short
unpaused initialization checks; Infiltration needed300 additional idle ticks to
exceed the100-frame threshold. These solo samples use Perfect Agent.

An isolated allocation diagnostic942e6a5ee reproduces the AI-co-op failure after
skipping Infiltration's intro: fileLoadToNew+0x90, file0x561/FILE_CHEAD_VD,
request52960, free43120; main thread faults at level-frame849. This is Velvet's
head model, loaded at buddy spawn after the room banks have been committed.
The model loader adds32KiB temporary space and later shrinks the allocation.
v86d tests prewarming this pending head before room budgeting. No release promoted.

Hardware attempts on2026-09-06: exact ED64 reset whileOFF returns1167/not connected.
Retry with Plug1ON also shows no present FTDI/COM device. Native uploader exits0
almost immediately with empty logs, which is NOT evidence of an upload. Elgato
enumerates, but produces no stream parts or TS frames. Worker confirms Plug1OFF
at21:14:33UTC and status Relay0 at21:14:34. No v86c console/Analogue boot claim.

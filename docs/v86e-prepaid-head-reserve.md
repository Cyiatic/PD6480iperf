# v86e: prepaid head allowance and read-only failure capture

Experimental source `3f6336d766aa7fcc86802d98e96cc3c5c028a275`, based on v86d.
ROM SHA256 `a9143f02981b7e44448f70638dd36ef679ad2a0d3ffcfd524f86e9c5e9d73bf3`;
ELF `716973dc5894b575355334474e5ca98ee6c04bec49b59e99ef0aa088f3d57f09`;
retail CRC `bcb684bc/0250ba5e`. No ROM replay or allocation trace is linked.

The default buddy's preloaded head retains21792 bytes in the measured v86d
sample, not the52960-byte temporary loading allocation. v86e returns its actual
`fileGetAllocationSize` from the prewarm helper and credits those retained bytes
against the128KiB late-stage allowance. Temporary EXTRAMEM, textures, already
cached heads, alternate buddies and unrelated modes receive no credit. Pending
CI menu capacities remain fully reserved. Oversized credit is rejected instead
of subtracting with unsigned underflow. Colour/depth buffers and the current-plus-
two-epochs room pinning rule are unchanged.

Actual-C guard/idempotency/retained-size/reserve-accounting tests pass, including
all15 alternate-cheat combinations and the old CI one-player negative control.
Native build and1403 compressed-asset validations pass;608 raw assets remain
outside that compressed-stream check.

Two normal cold10800-tick software runs use the same ordinary controller input
and external stock Dark save. Frontend watch captures at most8 counter increases;
it does not modify RDRAM or ROM code. The core's in-memory EEPROM header adapter
is still used. A VI yield can occur inside a game frame, so event samples are not
automatically stable allocator checkpoints. Final snapshots use the unchanged
strict inspector. No hardware/Analogue or benchmark claim follows from these runs.

- v86d: first watch event at frontend9780 / game frame305, visible rooms5/6
  absent,2160 cache bytes free, largest span1088. Loaded rooms were still pinned
  at epochs304/305. Final43 load failures,38512-byte bank, frame631 alive/OOM0.
- v86e: final12 load failures,54032-byte bank, frame684 alive/unpaused/OOM0,
  640x480, graph off; full-screen blur and inventory visible after pause/swipes.
  Event samples still show room6 missing at epochs299–301 and room32 at307–308;
  largest free span10880, below their17904/17584 load workspaces. The first event
  snapshot fails the strict partition validator (hole/overlap); this rejection
  is retained, not relabelled valid. Later event partitions and final partition
  validate, so mid-update sampling is a possibility, not a proven explanation.
- Another600 no-input ticks: frame1196, alive/unpaused, health0.93125, OOM0,
  graph0, no additional cache failures. No missing visible room in that final
  snapshot. Only12752 bytes of stage expansion-pool free space remained at10800;
  do not infer headroom for arbitrary later allocations or whole missions.

**Still not a clean candidate.** Do not promote an xdelta/ZIP from this branch.
The next investigation should establish actual submitted graphics-task lifetimes
and/or demonstrably reclaimable allocation costs. Do not simply reduce the
remaining reserve or weaken the two-epoch safety rule to hide these failures.
The broader solo/multiplayer/alternate-cheat/hardware/Analogue scope remains open.

No console power-on/upload/capture this experiment. Exact Plug1 status confirms
Relay0; the unrelated N64-named switch was not targeted. Elgato Timeshift contains
only the301-byte OverlayTimeline.json, no new recording. ED64's prior powered-on
absence remains a hardware transport issue, not a claim that a ROM booted.
Small reports/stills and provenance are in the private repository's
`evidence/v86e-prepaid-head-reserve`; ROMs, RAM and states remain local only.

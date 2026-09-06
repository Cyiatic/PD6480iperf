# v86: modern-core room memory experiment

Based on v85 / 21f656613, on experiments/v86-budgeted-modern-rooms.
The normal v85 21-mission matrix found 11 startup allocation failures or missing
room data. The Expansion Pak is already active: total RAM is 8 MiB. The two
614400-byte colour buffers plus 614464-byte depth allocation cost 1,280,000
more bytes than the upstream three 320x220 colour buffers plus depth.

This experiment changes residency, NOT resolution or the modern CPU/AI/DMA/
math core, compressed assets, framebuffer scheduling, menu fixes or L graph.
It is not a claim of identical full-preload behaviour or a measured speedup.

## Implementation

- Warm the existing modern mission-specific BG texture/dyntex set through one
  temporary room workspace, counting required hit-detection vertex batches.
  The always-rendered background room is also requested. No permanent geometry
  or batches are kept during warmup. Texture allocations remain on memp's right
  side; scratch is released only if it remains the last left-side allocation.
- Give the private room heap the actual remaining onboard and expansion bank
  allocations separately. Never treat the intervening stack/framebuffer region
  or memp's right-side allocations as unused RAM. Mema remains unchanged for
  file-manager and damaged-vertex allocations.
- Keep 128 KiB general stage headroom, plus CI's known lazy per-player menu
  model scratch capacity (0x25800 bytes per current player). The first v86
  experiment omitted that extra reserve and correctly fails its OOM gate.
- Opportunistically preload room graphics and batches into this heap. Retain
  them indefinitely when they fit; do not repeatedly evict during startup.
  Record skipped preloads separately from actual required-load failures.
- Load through onscreen selection, opaque/XLU/always-room/x-ray rendering and
  BG hit detection. Retain each room's original decompression/GBI workspace
  requirement for reloads, independently of its shrunken resident size.
- On demand, evict the least recently referenced eligible room. Free graphics
  and vertex batches together and clear stale colour/geometry pointers. The
  dyntex subsystem already retains relocatable room-relative metadata on unload.
- Pin current and two prior **submitted-frame epochs**, not the simulation
  clock or per-player portal counter. mainTick submits exactly one graphics
  task per epoch with at most two outstanding; this protects CPU-built and
  pending RSP/RDP references across pauses, slow motion and multiple players.

## Verification, in progress

The actual shared allocator C passes 100000 randomized fragmentation operations,
gap guards, full reclamation, overlap/double-free rejection and epoch-wrap/pinning
boundaries. The version-4 RDRAM inspector uses compiled candidate ABI offsets;
it accounts for every bank byte exactly once as live graphics, hit batches or
free space, and rejects holes, overlaps, out-of-bank spans and free-list cycles.
The cache-aware mission gate additionally requires every mission room warmed,
all visible geometry resident, exact vertex-batch counts, no allocation/cache
faults, normal CPU threads, active 640x480 and normal gameplay initialization.
An unloaded but successfully warmed room is explicit in reports, not silently
called a full-preload pass. This is still not a whole-mission playthrough.

Initial v86 ROM a8d1ecab3f0297614ad3331f4d88fd151788f9e70d53df052e8e874098d85c50,
ELF 506cb42e4175307c24f7e5171c651ac787e25da4329d22f0393081ed67f9d335:
cold stock-Dark software5100 ticks reaches CI frame3239 with valid room heap,
all CI preloads, no cache load failure, but memp OOM153600 from late menu scratch.
Do not distribute or count this as a pass; it was NOT uploaded to hardware.

v86b reserves that exact additional menu capacity. ROM
c33ec1459b3092d89f5a3b00f82f6b4dd8e59c294b479aa7d039dc7471455df7;
ELF a207b10b49eb024063751c403829e9fcf54416dac0026a8e1b3351ccdd2075f3;
CRC69c42a4a/7729ddf3. Compiled cache layout
d05a0af19e5587eb69c50e67d27fa5350121a8d7545c0335437d9b094463c3e2.
Fresh matching-build software results now cover all 21 stock solo missions.
All final samples are unpaused and pass the cache-aware initialization gate:
no OOM/cache load failure/allocator fault, complete live room data, exact hit
batches, valid heap partition and correct 640x480 mode. Five initial samples
were still in opening cutscenes; later ordinary Start inputs reach gameplay.
Seven other initialized pause samples resume with B. All 33 startup samples
and direct parent-state/RAM hashes are retained; no failed allocation is
superseded by a later pass. No foreign-build state or mission RAM poke is used.

Infiltration and Deep Sea additionally move, fire (loaded ammo 8 to 5), pause,
swipe menus left/right and resume gameplay. Full-screen pause blur is visually
verified in both. These are short software exercises, not full playthroughs.
Actual C allocator and blur tests pass; 25 Python inspector/input/provenance
tests pass. Room colours are gfxAllocateColours/per-frame or room-resident,
not separate mema allocations leaked on eviction.

Original-N64 validation is still pending. Multiple UNFLoader transfers stall;
fresh Elgato frames show the EverDrive menu, not a ROM handoff. One existing
serial-utility attempt printed Finished in 112.142 seconds but timed out on
process exit; no video was captured before power-off. A later serial transfer
stalled midway. Do not count those messages as a hardware pass. Plug 1 is OFF,
independently verified; inspected recordings deleted, small stills retained.
Private distribution branch mods/performance holds the detailed evidence in
evidence/v86b-budgeted-rooms. No v86 Analogue or benchmark pass is claimed.

Push source only to the private Cyiatic/PD6480iperf remote, never public origin.

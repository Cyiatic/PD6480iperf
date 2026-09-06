# v77: retained bounded cache, full 640x480i

Known mission-load failures; not a working or benchmarked performance release.

## Subsequent broader test: Infiltration and Rescue fail

Perfect Agent mission-load tests on September 5 found stage-pool allocation
failure before the first rendered level frame. Infiltration requested 44,000
bytes with 33,376 left; Rescue requested 33,632 with 32,320 left. In both cases,
the separately reserved 512,000-byte mema cache was completely unused. This
contradicts any broad claim that v77 is playable throughout the game.

Skedar Ruins was loaded through the actual menus and reached first-person play
on Perfect Agent, with 640x480 active buffers and no allocation failure. Further
tests injected only the stage/index/Perfect Agent/solo menu-selection word, then
used normal A input to invoke Accept Mission. Attack Ship and Duel reached normal
gameplay; Defection and Crash Site rendered but were still in cutscenes when the
short test ended. None of those narrower checks cures the Area 51 load failures.

## Changes from v76

- GCC `-fmerge-constants` with linker inclusion of `.rodata.*` shares identical
  read-only string/floating constants. This is not `-fmerge-all-constants`.
  Recompiling all source C objects saved 6,960 bytes before the cache-policy
  change; the final CI snapshot has 6,912 more free stage-pool bytes than v76.
- `bgTickRooms` retains old rooms while mema's largest free block is at least
  64 KiB. Below that threshold, the original two-rooms-per-tick eviction applies.
  Room-load and file-list requests retain explicit immediate garbage collection.
- Full 640x480 colour and depth storage, video allocation before level loading,
  minimum 256 KiB cache, larger original stage caches, and L graph are unchanged.

Whole-level room preloading is still disabled. Its geometry and permanently
loaded textures do not fit safely alongside the full-resolution buffers.
Retaining already visited rooms is a bounded replacement strategy, not a claim
to reproduce whole-level preloading or a measured framerate improvement.

## Verified on 2026-09-05

### Exact-ROM original N64 test

At 19:30 local time, Kasa's exact child **Plug 1** was switched on (Relay: 1).
The unrelated **N64** outlet was not operated. ED64 uploaded the ROM below in
36.13 seconds. The Elgato's fresh, growing capture segment began at 19:31:02;
decoded frames show EverDrive, product identification, logos and the animated
Defection 3D opening, including the aircraft over the city. A black early frame
was a transition, not the final result. This is a boot/intro pass only.

Plug 1 was switched off and Relay: 0 independently verified after inspection.
The capture process was stopped and its sole test recording (226,991,952 bytes)
deleted. Small stills remain locally in `../hardware-v77/`.
No interactive-controller hardware, console checkbox or Analogue pass is claimed.

### Emulator controller-input tests

Core: ParaLLEl N64 1.0 2f3bf60, cached-interpreter CPU, cxd4 RSP, Angrylion RDP,
8 MiB RDRAM. These are not N64 speed benchmarks. Save-dependent tests use the
documented in-memory ED/16-Kbit header adapter; executable code/assets are unchanged
and the disk ROM used on hardware is unmodified by that adapter.

- Cold start, 3,900 ticks: Dark selected, menu closed, CI movement and L graph.
- Pause, then stick-left to Options; stick-down and A to Video Options.
- Two separate stick-down inputs, then A, enabled the actual Hi-Res checkbox.
  After 900 further test ticks, 900 new frames were produced; matching RDRAM
  reports Hi-Res=1, active dimensions 640x480 and no allocation failure.
- From that menu state, A disabled the checkbox. Another 600 ticks produced
  600 frames; Hi-Res=0, dimensions unchanged and no allocation failure.
- A separate continuation from the enabled state closed the menu with Start
  and applied stick movement. It completed 1,200 ticks/1,199 new frames, changed
  the camera view, retained Hi-Res=1 and reported no allocation failure.

The Hi-Res checkbox deliberately changes only its stored option flag. Both
logical modes already render at the fixed full 640x480 resolution; enabling the
checkbox is not required to obtain 480i in this candidate.

CI snapshot: colour addresses 0x80400000 and 0x80496000, depth 0x80343800;
150,288 free bytes in the expansion stage pool and 8 onboard, plus capacity
inside the separately reserved mema cache. This is a snapshot, not proof of
adequate memory throughout every stage, multiplayer mode or extended session.

### Automated gates

- Both gameplay table entries are 640x480 with 640-pixel stride.
- Colour allocation 1,228,864 bytes; depth allocation 614,464 bytes, including alignment.
- All 1,403 compressed assets validate; 608 raw entries are not validated by that audit.
- All 12 existing allocation/asset/save regression tests pass.
- `test_bg_cache_policy.py` compiles the candidate's actual `bgTickRooms` with
  allocator stubs and checks threshold, two-eviction cap, visible-room protection,
  and young/unloaded-room behavior. It does not benchmark caching.
- Xdelta decode matches the exact ROM SHA256 below.

Changing compiler flags requires recompiling every source C object. The existing
Makefile does not automatically track CFLAGS changes. This test rebuilt source
C objects while preserving the previously validated generated assets. Local
Windows build adapters remain separate from the source commit.

## Identity / save

Source branch `candidates/v77-retained-cache`, commit `c100de617`.

ROM: `PD6480iperf-v77-retained-cache.z64`

SHA256: `98f30111d787d3ad0ff578e118a2933011eb05ecc81719704b9bf9d3ed3eb866`

CRC1/CRC2: `f00dbfc3` / `0b8a2473`.

Xdelta SHA256: `a9ccc89e2e592285997278caebea8ccbbe639e2c84d5c3587cf4508f9165ba91`

Base: stock NTSC V1.1, SHA256
`4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`.

The supplied 2,048-byte Dark save is the existing stock-format synthesized 100%
save (all unlocks, cheats inactive, Hi-Res off). It is recognized by stock V1.1
and this candidate in the emulator. Console import remains unverified. Back up
existing saves before importing it; no user's console save was overwritten.
Save SHA256: `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d`.

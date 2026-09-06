# PD6480iperf v86b — 640x480i / budgeted room-memory test candidate

Normal ROM: **PD6480iperf-v86b-budgeted-rooms.z64**. Expansion Pak required.

Fixed 640x480 colour and depth rendering, interlaced output, newer performance
code and L-toggle FPS graph. Video Options reads **Hi-Res: 640x480i (fixed)**;
there is no redundant resolution checkbox. Full-screen pause blur and menu
framebuffer fixes remain. Normal menu perspective/eyepiece motion is intentional
and remains enabled; the fix targets incorrect scaling and stale fragments.

The full 8 MiB was already in use. These larger colour/depth buffers cost
1,280,000 extra bytes versus the upstream layout. v85's later mission matrix
found 11 startup allocation/missing-room failures. v86b budgets the remaining
RAM: retain warmed textures, keep room geometry/hit data while it fits, evict
eligible old rooms and load them on demand. Graphics tasks' in-use rooms stay
pinned. This changes full-level preloading, not rendering resolution or the
modern CPU/AI/DMA/math improvements. No measured speedup is claimed.

## What was checked

- Normal-ROM software: all 21 solo missions reach unpaused gameplay initialization
  at640x480 with no OOM, required-room load, allocator or CPU faults. Infiltration
  and Deep Sea also move/fire/pause/swipe/resume. This is not21 full playthroughs.
- Normal-ROM original N64: native ED64 upload and fresh Elgato city/rooftop3D
  intro. Later logo/black frames were retained, not called interactive gameplay.
- Separate explicitly labelled original-N64 diagnostic: Infiltration/PerfectAgent
  gameplay, alive full-screen pause blur, horizontal menus, fixed-resolution
  label and L visibility changes. On resume, the unattended player is killed
  almost immediately; no sustained gameplay pass. Diagnostic1 died before its
  pause test and was rejected for that check. Neither diagnostic is distributed.
- Actual-C blur/allocation, input partition and RAM-save tests;25 inspection/
  input/provenance tests;4 stock-save tests; earlier100000-operation actual-C
  allocator stress. Xdelta roundtrip matches the exact normal candidate hash.

**Still a test candidate:** Analogue3D v86b, long sessions, full missions,
multiplayer pressure, controlled performance comparisons and physical save
import remain unverified. No synthetic controller input or RAM-save shim is in
the normal ROM. Cold boot; do not restore a different build's save state.

## Patch and 100% stock Dark save

ZIP contains xdelta, matching-name .eep, README and manifest, **no ROM**.
Apply xdelta to the supplied clean USA V1.1 big-endian .z64:

Base SHA256: 4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21
Output SHA256: c33ec1459b3092d89f5a3b00f82f6b4dd8e59c294b479aa7d039dc7471455df7

The matching .eep is a generated, checksummed2048-byte stock-format100% agent
and multiplayer player named **Dark**, not player-earned records or a save state.
Completion data covers solo/co-op, cheats, training/medals and challenges; stock
controls/options remain. Its Hi-Res preference is ignored by this fixed480i ROM.
The exact save bytes load through game decoding in RAM-only hardware diagnostics;
physical EverDrive/Analogue import has not been tested. Back up your existing
whole-cartridge save, then use your device's EEPROM import workflow with the
matching ROM/save basename. Do not overwrite a wanted save or use it as .mpk.

Private source: Cyiatic/PD6480iperf, experiments/v86-budgeted-modern-rooms,
runtime ea2ad550b4862cb9fe1451e0da8d42ea4a32c1ef. Detailed evidence on
mods/performance: evidence/v86b-budgeted-rooms and evidence/v86b-hardware-transport.
Only Plug1 controlled; OFF verified after testing. Inspected recordings deleted.

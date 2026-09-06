# Normal v82b gameplay and option checks — 2026-09-06

These are emulator checks, not physical-console or Analogue passes. Normal ROM
SHA256 `9da54bbde7d42be0441af6031de1711fe647f3a4036e5ca9da381ccc0cea30b1`,
source `24995c1c66eaa0e4ac5568f5711f7af7678b5561`, ELF
`3f7b1c5165585023087dddfe8b7fb2ee0cb523c520bbeb76f8a8c3b16b902fa8`.
There are no synthetic replay hooks or RAM save shims in this normal ROM.

ParaLLEl N64 2f3bf60, cached interpreter, Angrylion/cxd4, 8 MiB. The host's
in-memory EEPROM-header adapter is used; the disk ROM is unchanged. Inputs
are ordinary libretro controller events. There are no gameplay RAM writes.
Except for the previously documented cold root, runs restore states made by
this exact binary; they are not independent cold boots or cross-build restores.

## State provenance and results

- `cold.json`: previous 5100-tick fresh-Dark cold root, CI at Skedar briefing.
- `ci-options.json`: cold root + 600 ticks, B exits briefing and Start opens
  Perfect Menu. Player stays at (379.9, 484, 669.5), CI room 16.
- From ci-options, right-stick 180 ticks opens Options; down-stick/A 300 ticks
  opens Video. The scripts are included. D-pad navigation is ignored by this
  newer core's menu implementation; two exploratory D-pad runs were not passes.
- `hires-on-graph-off.json`: Video state + 450 ticks, down twice/A/L. Hi-Res=1,
  graph=0, 640x480, no OOM or main/scheduler exception. Screenshot shows checkbox.
- `hires-off-graph-on.json`: preceding state + 300 ticks, A/L. Hi-Res=0,
  graph=1; dimensions and allocation remain unchanged.
- `hires-on-ci-walk.json`: preceding state + 1050 ticks, A/Start/turn/forward.
  Hi-Res=1, graph=1, unpaused, alive; level frame advances from 1355 to 2191.
  Position changes to (753.0, 484.0, 589.65), still room 16. Final view faces a
  wall; movement is supported by position delta, not inferred from that still.
  Full 140/140 CI room geometries remain resident; expansion heap free 331040.
- `skedar-pause.json`: previous v82b accepted-mission state + 600 ticks of Start
  pulses skips the cutscene and pauses first-person gameplay, level frame 1347.
- `skedar-move-fire.json`: preceding state + 1200 ticks, Start/turn/forward/Z.
  Unpaused, not a cutscene, alive, full health, level frame 2489. Position moves
  from (-2307.3,159,-285.9), rooms [10,4], to (-2420,229,-970), room [9].
  Pistol reserve falls from 192 to 184; magazine is 8 after reloading. The host
  produces 1200 video frames. This is limited movement/shooting, not a mission
  completion. All 137/137 Skedar room geometries remain resident.

All reported endpoints use two full colour buffers at 0x8036a000 / 0x8076a000,
depth at 0x80400000, active 640x480 and no OOM marker. Both prepared VI modes
remain HAF1: ctrl 0x305e, width 1280, vSync 524, x/y scale 1024, alternating
field origins 1280/2560. This supports full render/interlace configuration in
software; an emulator output size or a composite capture alone is not an
independent measurement of physical console framebuffer resolution.

The gameplay layout is metadata compiled from the exact newer-core headers,
not code linked into the ROM. The inspector checks structure sizes and hashes
resident code before accepting a dump. Version 2 adds player position/room,
health and ammunition offsets while retaining version 1 support.

The normal Hi-Res preference is retained for stock save/UI compatibility.
Rendering remains fixed at full 640x480i whether that checkbox is on or off.
Multiplayer, broader level coverage, speed benchmarks, long sessions, physical
save import, physical-controller gameplay and Analogue validation remain open.

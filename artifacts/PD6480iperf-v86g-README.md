# PD6480iperf v86g — 640x480i performance test candidate

Normal ROM: **PD6480iperf-v86g-completion-reserve.z64**.
Expansion Pak required. Cold boot; do not restore an older build's save state.

This build retains the newer performance code and L-toggle FPS graph, with
full 640x480 colour/depth rendering and interlaced output. Video Options now
reads **Hi-Res: 640x480i (fixed)**, not a redundant resolution checkbox.
The pause blur samples and fills the entire framebuffer. Menu framebuffer
clearing/scaling fixes remain; ordinary menu perspective/eyepiece animation
is intentional and has not been disabled.

All 8 MiB is already enabled. The larger buffers cost 1,280,000 extra bytes versus
the upstream layout. Room data is budgeted within the remaining RAM, retaining
warmed textures and evicting eligible old geometry/hit data when needed. Rooms
still referenced by graphics tasks remain protected. This is not a guarantee
of whole-level geometry preloading, and no measured speedup is claimed.

v86g also reserves queue space for graphics completion messages after an old
Extraction freeze was traced to retrace traffic blocking the scheduler and
losing an SP completion. No additional framebuffer or reduced resolution is
used for that fix. The old-ROM trace and actual-C saturation tests support it;
a same-layout zero-reserve control also passes the cold input script, so that
script alone is not proof that the queue policy explains every observed freeze.

## Verified scope and limits

- Normal-ROM software: 21/21 Solo/Perfect Agent missions reach initialization
  with 640x480, unpaused final samples and no OOM/cache/heap/CPU faults. 19 final
  players are alive; G5 Building and Duel end in ordinary unattended combat death.
  All 33 initial/continuation samples are preserved. These are not playthroughs.
- Normal-ROM Deep Sea: movement, firing (ammo 8 to 5), full-screen pause blur,
  horizontal menus, resume and L hidden/shown. Final player alive, full health, unpaused;
  no recorded memory/cache/CPU faults. The inspected images are software output.
- Original N64, normal ROM: ED64 upload and Elgato city/ship/rooftop3D intro,
  later Nintendo logo. This is not physical-controller interactive-gameplay proof.
- Original N64, separate labelled diagnostic: alive Infiltration menus/blur/L
  and brief resumed gameplay, then ordinary combat death. It uses RAM-only
  Dark and a scripted controller replay. That diagnostic is NOT included here.
- 52 tool unit tests, 4 stock-save tests, actual-source C blur/reserve/scheduler
  tests and negative controls. 1,403 compressed assets validate; 608 raw assets are
  outside that decompression audit. Xdelta decode reproduces the exact ROM hash.

**Still a test candidate:** this v86g build has not been verified on Analogue 3D,
for full missions/long sessions, broader co-op/multiplayer pressure, controlled
performance comparison or physical save import. The normal ROM contains no
scripted input or RAM-save shim. Do not distribute it as a finished release.

## Patch and stock 100% Dark save

ZIP contains xdelta, matching-name 2048-byte `.eep`, this README and manifest;
no ROM. Apply the patch to the clean big-endian USA V1.1 ROM supplied for this
project. The local `.z64` supplied separately is already patched.

Base SHA256:
`4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`
Output SHA256:
`79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`

The save is a generated, checksummed stock-format 100% agent and multiplayer
player named **Dark**. Completion records are synthetic, not player-earned.
Stock controls/options remain; its Hi-Res preference is ignored by fixed 480i.
It is an EEPROM image, not a controller-pak file or Analogue save state.

Back up your existing whole-cartridge save before importing. Use your device's
existing Perfect Dark EEPROM import workflow, keeping the ROM and save basename
identical. This replaces all cartridge save slots, not just one agent. The
required save type is 16Kbit EEPROM (2048 bytes), not 16KB. Full save documentation
is in `artifacts/saves/README.md` in the private repository.

Private source: **Cyiatic/PD6480iperf**, experiments/v86g-completion-reserve,
runtime 26cb92ae9d0ae2cba172999c0d5c1762f32d5a50. Evidence on mods/performance:
`evidence/v86g-completion-reserve/`. Only Plug 1 is used for console power;
it is turned off after testing. Inspected Elgato recordings are deleted.

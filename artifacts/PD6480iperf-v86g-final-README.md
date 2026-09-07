# PD6480iperf v86g

The unchanged v86g build combines the newer Perfect Dark performance code
with full 640x480 gameplay rendering and 480i video output. Expansion Pak is
required. L toggles the FPS graph. Pause blur covers the whole view and menu
clearing/scaling fixes are included. Hi-Res is non-interactive because the
gameplay resolution is fixed; enabling a second resolution mode is unnecessary.

The user confirms blur, menu navigation and the L toggle work on their Analogue
setup and approves the skipped Hi-Res option. This bundle contains exactly the
same ROM patch and Dark save previously supplied; only these handoff notes
and the accompanying manifest are new. No ROM is included in the ZIP.

## Use

Apply `PD6480iperf-v86g-completion-reserve.xdelta` to clean big-endian Perfect
Dark USA V1.1. The separately supplied `.z64` is already patched. Cold boot;
do not restore a save state made with another ROM version.

Base SHA256:
`4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`

Patched ROM SHA256:
`79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`

## Included Dark save

The matching-name `.eep` is a generated, checksummed, stock-format 100% save
named **Dark**, including a multiplayer Dark player. Completion records are
synthetic; stock controls/options remain. It is 2048-byte / 16Kbit EEPROM,
not a controller-pak file, 16KB file or Analogue save state.

Back up your existing whole-cartridge save before importing: this replaces
all cartridge save slots, not just one agent. Keep ROM and save basenames
identical and use your device's existing Perfect Dark EEPROM import workflow.
The save's stock Hi-Res preference is ignored by fixed 480i. No existing
physical cartridge save was overwritten during this work.

## Verification and limits

- Normal ROM: software checks cover 21 solo mission initializations, short
  movement/fire/pause/menu/L exercises, AI co-op and four-player samples.
  These are bounded checks, not full playthroughs.
- Original N64: normal ROM uploaded through ED64 and rendered the 3D intro.
  A separate labelled replay of the same rendering/memory/scheduler code
  reached Infiltration gameplay and exercised blur/menu/L before ordinary
  combat death. It is not included and is not normal physical-input proof.
- Analogue: user-reported normal-build blur, menus and L confirmation.
- Patch decode reproduces the exact ROM hash. Save checksums and stock-format
  decoding are validated. Private source and detailed evidence are in
  Cyiatic/PD6480iperf; runtime commit 26cb92ae9d0ae2cba172999c0d5c1762f32d5a50.

All 8 MiB is available. Two colour buffers plus depth use 1,843,264 bytes,
1,280,000 more than the performance upstream layout. CPU/AI/DMA/math
optimizations remain; texture warmup and budgeted retained room geometry
accommodate the larger buffers. Guaranteed whole-level geometry preloading
does not fit every mission. No measured FPS increase, full-game endurance
certification or physical save-import result is claimed.

Only Kasa **Plug 1** was used for the test N64. It was switched off after
testing. Inspected Elgato recordings were deleted; small stills/logs remain.

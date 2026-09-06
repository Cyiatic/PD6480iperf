# v76: bounded-cache full-480i diagnostic

Development candidate, not a finished performance/480i release.

## What changed and why

v74's full 640x480 depth allocation exposed another memory-budget problem:
whole-level background room preloading left 1,185,552 bytes available for a
1,228,864-byte colour-buffer request. The request returned NULL and viReset
attempted to clear that address. This was reproduced in an 8 MiB emulator.

v75 used the existing streaming path with a minimum 500 KiB room cache.
It rendered Defection's opening sequence, but Carrington Institute ran out of
memory while loading (39,808-byte failed request, 33,264 bytes left).

v76 reduces that minimum to 256 KiB; existing larger stage-specific caches
remain larger. viReset runs before lvReset so video memory is reserved first.
Whole-level room preloading is disabled in this diagnostic. Other inherited
performance changes and the L graph remain, but performance is not benchmarked.
An adaptive preload strategy remains future work if it can fit safely.

Both colour images and depth storage remain full 640x480. There is no hidden
640x220 fallback. The legacy Hi-Res checkbox only stores an option flag: it
does not change the fixed framebuffer mode. This behaviour is deliberate and
is not a claim that the menu interaction has passed on Analogue.

## Evidence on 2026-09-05

- Original N64: exact Plug 1 relay, ED64 successful upload in 36.20 seconds,
  and fresh Elgato decoded video of the animated Defection opening after the
  logos. Small stills/contact sheet retained in `../hardware-v76/`.
- No interactive-controller console pass or Analogue pass is claimed.
- Plug 1 was switched off and Relay: 0 verified after the test. The N64-named
  outlet was not operated. Test video segments were deleted after inspection.
- The Elgato had entered Windows Code 22 (disabled) between tests; enabling
  its exact USB device restored Status OK and fresh video. Earlier v75 upload
  succeeded but had no fresh capture evidence, so it is not a console pass.
- Emulator: cached-interpreter CPU, cxd4 RSP, Angrylion software RDP, 8 MiB.
  Carrington Institute file-selection background animates, L graph displays
  FB 640x480, and the matching ELF/RDRAM dump reports no allocation failure.
  One CI snapshot has 143,376 bytes free in the expansion stage pool and
  8 bytes onboard, plus free capacity inside the separately reserved room cache.
- The Dark save is recognized by unmodified stock V1.1 in the emulator.
  Console save import is still unverified; back up any existing save first.
- This emulator build ignores its advertised save override for unknown ROMs
  and defaults them to 4-Kbit EEPROM. Save-dependent candidate tests use an
  explicit in-memory ED/16-Kbit header adapter; the on-disk/hardware ROM is
  unchanged. Such tests must be identified separately from exact-ROM tests.

The save-device adapter test subsequently recognized the EEPROM, selected Dark,
closed the menu and rendered an interactive CI view with the L graph. A direct
test of the Hi-Res setter's sole effect (`g_HiResEnabled = 1`) then ran for
900 emulator ticks with 900 new video frames, 640x480 active dimensions and no
allocator error. This tests the flag effect, not the actual checkbox UI action.
It is not an Analogue Hi-Res-toggle pass.
Restoring the flag to zero and running another 600 ticks likewise produced
600 new frames, kept 640x480 and reported no allocation error. Scripted stick
input changed the CI camera view across the runs.

All 1,403 compressed assets validate. Both logical gameplay table entries and
the active runtime framebuffer dimensions are 640x480. The ELF colour/depth
allocations remain 1,228,864 and 614,464 bytes including alignment.
The xdelta decode round-trip is byte-identical and all 12 existing asset,
allocation and save regression tests pass.

## Identity

Source branch: `candidates/v76-bounded256-cache`, commit `755ee8a7b`.

Base: stock NTSC V1.1, SHA256
`4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`.

ROM: `PD6480iperf-v76-bounded256-cache-diagnostic.z64`, SHA256
`e745e7aedeb3909a1f4eea363e5d2452758cac4ce655f89986cc51cd53dc1384`.

Xdelta SHA256:
`b085a845a0799b49182a15f66ed3544fd703f077fc481ba6269004355a0066c8`.

Dark stock-format 100% EEPROM SHA256:
`fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d`.

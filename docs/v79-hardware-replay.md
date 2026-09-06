# v79 hardware replay B — diagnostic only

This branch is **not a release candidate**. It adds a synthetic controller
replay, a RAM-only save image and a yellow diagnostic HUD to release source
`d21f1c8c9401b460ccc002c480d1caa08544ba0b`. Do not merge these hooks into a
normal candidate or distribute this ROM as the playable v79 download.

## Purpose and scope

Exercise original-N64 gameplay autonomously through ED64 upload and fresh
Elgato footage, using only the Kasa outlet named **Plug 1**. The unrelated
outlet named **N64** and the parent switch must never be operated. Turn Plug 1
off when testing stops or while building. Delete inspected recordings, retaining
only small evidence stills.

The existing joy sample-playback callback supplies Start, B, C-down, A, L and
stick inputs to the game's normal input consumption. Dark file selection and
opening Video Options are programmatic setup, not controller-driven navigation.
This is not physical-controller input testing or an unchanged-release-ROM test.

The replay starts from a fresh boot, chooses its sole RAM-backed Dark profile,
enters Carrington Institute, toggles the L graph, moves, opens Video Options,
uses normal A inputs to switch Hi-Res on/off/on, closes menus, toggles L off/on,
and moves again. It then enters phase 8 and idles. Phase 99 means a replay
navigation/state assertion failed; it does not by itself mean a game crash.

Diagnostic A reached CI but entered phase 99 because it used D-pad down in a
menu that consumes C-down. B corrects that test-driver error. A was not uploaded
to the original N64.

## Save isolation

`pakProbeEeprom` reports a RAM-backed device. `pakReadEeprom` and
`pakWriteEeprom` call only the bounds-checked `pdHwEeprom` RAM-copy function.
The embedded 2,048-byte seed is the generated stock-format 100% Dark save:
SHA256 `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d`.
The ROM's seed resets on every fresh boot; no changes persist.

`__osContRamWrite` returns `PFS_ERR_NOPACK` immediately, blocking the common
physical Controller Pak/Transfer Pak/rumble memory-write path. The compiled B
ELF contains exactly `03e00008 24020001` for that function. The EEPROM access
functions have only the expected direct call to the RAM shim; probe and shim
have no external calls. These checks cover the defined save paths, not arbitrary
memory-corruption behavior. This does not validate real EEPROM import/writes.

The distribution branch supplies `tools/emulator/audit_hw_replay.py` for those
ELF checks and final emulator state inspection, and
`tools/emulator/test_hw_shadow_save.py` to compile and exercise this actual
RAM-copy routine (round trips, last block, overrun, null and unchanged guards).

## Exact build identity

ROM: `PD6480iperf-v79-HW-REPLAY-B-NOT-RELEASE.z64`

- ROM SHA256: `8886703fba772fc96984bf7448e3f16d0221df228a8d08eba37c9604b64a0366`
- ELF SHA256: `f5c6bccf04a1cab005cede86220e0ddfcf29b47737d26b62e1ca1f3b1d80dc32`
- CRC1/CRC2: `d8d2ae55` / `52de9f43`
- Both gameplay mode entries: 640x480, stride 640.
- Colour/depth storage: 1,228,864 / 614,464 bytes.

Build with the existing NTSC-final GCC workflow. The explicit linker object
list contains both new objects. Force the linker-script dependency with
`make -W ld/pd.ld ... rom` after changing that list; an incremental build does
not otherwise necessarily track the included list. Apply the existing retail
header/CRC step after building. Local Windows toolchain adapters were preserved
but are not part of this diagnostic source change.

## Results, 2026-09-05

A cold 6,600-tick emulator run without an external input script, supplied save
or savestate completed phase 8, with three Hi-Res checks, Hi-Res enabled, graph
enabled, 640x480 active buffers, CI unpaused and no allocation-failure marker.
It produced 5,702 video frames. This is separate from console evidence.

The exact B ROM uploaded to ED64 in 36.48 seconds. Fresh original-N64 Elgato
footage shows CI movement, the checked/unchecked/checked Hi-Res checkbox at
94/100/110 seconds in segment 1, graph hidden at 125 seconds and visible again
at 136 seconds with a changed view. Segment 2 shows further movement and the
final phase-8 HUD. No freeze was observed during this limited sequence.

Two recording segments total 269.711289 seconds. Inspection must include both:
Elgato rolls to `_0002.ts`; rereading `_0001.ts`'s final frame is stale evidence.
Plug 1 was off after testing and independently returned `Relay: 0`. Recordings
and their four metadata files were deleted after inspection (502,338,088 bytes).

See `docs/PD6480iperf-v79-hardware-replay.md` and
`artifacts/tests/v79-hardware-replay-B/` on the private repo's `mods/performance`
branch for retained stills and the emulator report. No Analogue test, broad
physical-controller playthrough, native-framebuffer measurement from capture,
real-save import, or unchanged-release interactive console pass is claimed.
Whole-level preloading remains disabled; performance is not benchmarked.

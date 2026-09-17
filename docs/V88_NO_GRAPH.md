# v88: no graph, stock L and D-pad controls

[Download this alternative](https://github.com/Cyiatic/PD6480iperf/releases/tag/v88-no-graph)
· [Installation and edition chooser](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/INSTALL.md)
· [Verification evidence](../evidence/v88-no-graph/README.md)

Runtime source: [`cb4e30de6433bbd4cc47e4f0b739700db15efb96`](https://github.com/Cyiatic/PD6480iperf/commit/cb4e30de6433bbd4cc47e4f0b739700db15efb96)
on [`fix/v88-stock-controls-480i`](https://github.com/Cyiatic/PD6480iperf/tree/fix/v88-stock-controls-480i).
Later commits package the candidate and documentation without changing runtime code.
This is a prerelease alternative: **Analogue 3D testing is still pending**.

## Why

Players holding the D-pad and analogue-stick grips can use scheme 1.2 with
their right hand aiming and their left hand moving. The L shoulder is their
accessible aim button. v87's performance foundation reserved L for the graph
and zeroed the original L/D-pad masks. Hiding the graph did not restore them.

v88 is a separate alternative. The v87 release and its graph toggle are kept
unchanged. Nothing mirrors the levels or changes the selected control style.

## Source scope

Base: `82d704d0154ea86f9e5d0fb98541907806f31960`.
The original graph input changes came from
`5430099310f52d0e34aae4f8af4ca7222358c18d`.

84 surviving mask edits are reversed across `activemenutick.c`, `bondbike.c`,
`bondeyespy.c`, `bondmove.c`, `bondview.c`, `credits.c`, `menu.c`, and `player.c`.
The old menu-model debug path and old end-of-level path were already removed
before v87 and are not reintroduced. `lv.c` no longer reads graph hotkeys,
collects graph samples, or draws graph/statistics. Its legacy profiler-visible
state remains initialized to zero. No rendering geometry, framebuffer,
scheduler, room-cache, or CamSpy aperture code is changed.

## Build provenance

This checkout was created from the exact public v87 source. Worktrees inherit
sparse-checkout settings; disable sparse checkout in a new build worktree.
Supply the clean USA1.1 ROM and run `tools/extract` before building.

The successful host setup used MIPS GCC 12.2.0, native make with
`SHELL=C:/msys64/usr/bin/bash.exe`, `MAKE=make.exe`, `HOST_EXE=.exe`,
`MIPS_BINUTILS_PREFIX=mips64-elf`, `ROMID=ntsc-final` and the bundled Python.
MSYS utilities must precede old BusyBox utility aliases. The archived original
`mkrom.exe` (SHA-256
`eeec0ac52accb95e7221f2dd381204c0ff3291d51941916f638e5c00253bdb3f`)
was recovered locally; it is not distributed. Building that helper afresh is
still a toolchain documentation gap: the unmodified helper includes `crypt.h`.

Before changing runtime code, the rebuilt v87 had identical bytes for all
8,443 readable matching ELF symbols. Of 2,081 allocated file-backed ELF
sections, 2,079 were byte-identical; two compressed asset streams differed
but decompressed to identical data (72,048 and 528,832 bytes). The rebuilt
baseline ROM is therefore not byte-identical to the release. Do not claim
the old published hash for it. These compression differences carry into v88.

Candidate source-header ROM SHA-256:
`2d418f2a010eb99d3d36cf1d28df6494236f70dd89c7562d8b13b3fa51ea0cc9`.
Retail-header ROM SHA-256:
`7971eb42e66ba1d5773e7a5c557f4ea578e7800e862f350b2ce5908b21223891`.
Candidate ELF SHA-256:
`7a8873ebae5626c6e02ea76c64c4bc45a4d80055991728da8638bc947bb40e8b`.
Retail header normalization changes only bytes 0x3c and 0x3f, as in v87.

## Verification

- `tools/test_stock_controls.py`: exact inverse of every surviving historical
  input edit; old input and old graph entry point rejected as negative controls.
- `tools/test_eyespy_480i.py`: 193,800 actual-C math/GBI-argument cases pass;
  original broken aperture is rejected with exit 17. Not an RDP/hardware test.
- Compressed-asset audit: 1,403 valid, zero invalid; 608 raw assets unchecked.
- Xdelta decode onto clean USA1.1 matches the candidate exactly.
- Emulator cold boot: normal file selection into live Carrington Institute.
  The old seed's D-Up at tick 2400 was deliberately removed: it used to be
  ignored, but now correctly changes the file-menu selection. The first old
  replay reached name entry and was rejected as a gameplay test seed.
- `tools/test_stock_controls_runtime.py`: scheme 1.2 D-pad movement in four
  directions, analogue camera on both axes, L hold/release, L toggle on/off,
  R hold, and graph staying off all pass. These are real emulated inputs;
  aligned RAM writes change only the existing style/aim settings. A compiled
  matching-ABI probe supplies offsets. The core's EEPROM-header adapter is
  applied only in memory; it is not part of the distributed ROM.
- Original N64: ED64 upload completed in 36.48 seconds. The exact candidate's
  80.962-second Elgato recording contains a progressing intro (ship/Joanna),
  proving boot beyond product identification. UI capture itself was black;
  decoded H.264 frames, not that UI snapshot, provide the visual evidence.
  Capture is 640x480/29.97; capture dimensions alone do not prove framebuffer
  resolution. The matching emulator inspection supplies 640x480 render proof.
  Plug 1 OFF and Relay 0 were confirmed at 03:13:04 UTC on September 17.

Physical-controller gameplay, Analogue 3D, long sessions and multiplayer have
not been retested. Menu/CamSpy/hoverbike control restoration has source proof,
not a complete live-input matrix. The temporary hardware recording is removed
after inspection; retain the compact contact sheet and reports, not videos.

The software frontend/controller mapping is documented by the
[libretro core](https://github.com/libretro/parallel-n64/blob/master/mupen64plus-core/src/plugin/emulate_game_controller_via_libretro.c).

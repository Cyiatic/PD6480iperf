PD6480iPerf v88 - No Graph / Stock Controls candidate

Alternative to v87, not a replacement for its L-toggle graph edition.
480i, performance improvements and the v87 CamSpy rendering fix are retained.
The FPS graph and its hotkey are removed. Stock L and D-pad bindings are restored
for gameplay, active menus, pause menus, EyeSpy/CamSpy and hoverbike controls.

Mirrored 1.2 controls: choose controller style 1.2 in the game's options. Use
the D-pad to move, the analogue stick to look, and L to aim. R and C-buttons
remain available. The existing hold/toggle aim option applies to L as normal.
This does not mirror levels. There is no FPS-graph toggle in this edition.

PATCHING
Apply PD6480iperf-v88-no-graph-candidate.xdelta to a CLEAN big-endian USA v1.1
ROM, not to v87 or another patched ROM. Expansion Pak / 8 MiB is required.
Input SHA-256:
4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21
Patched ROM SHA-256:
7971eb42e66ba1d5773e7a5c557f4ea578e7800e862f350b2ce5908b21223891
The patch has been decoded onto the clean base and byte-verified.

SAVE
The optional .eep is the unchanged 2 KiB stock-format 100% Dark save supplied
with v87. Match its filename to the ROM and install in your device's save
folder. Back up existing progress; do not overwrite your save unintentionally.
Control style remains user-selectable; this save does not force 1.2.

TEST STATUS - 2026-09-16
- Emulator: cold boot into Carrington Institute at 640x480; all four D-pad
  directions move the player, both stick camera axes work, L aim hold/release
  and toggle-on/toggle-off work, R aim works, and graph remains off.
- Emulator input tests instrumented only the existing control-style/aim-mode
  settings. An emulator-only EEPROM header adapter was used to load the Dark
  save. Neither changes the distributed on-disk ROM.
- Source: all 84 surviving input edits from the original graph modification
  are reversed; two removed legacy code paths are not reintroduced.
- CamSpy: 193,800 source-math/graphics-argument regression cases pass.
- Original N64: exact candidate uploaded over ED64; Elgato recording confirms
  sustained animated intro beyond startup. This is boot/intro proof, not a
  physical-controller gameplay or completed-mission test. Plug 1 powered off.
- This new variant has NOT yet been tested on Analogue 3D. v87 feedback does
  not establish v88 compatibility. Multiplayer and long sessions not retested.

Original project: https://github.com/Cyiatic/PD6480iperf
Original v87 release remains unchanged. No ROM is included in the patch ZIP.

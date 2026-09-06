# PD6480iperf v84 — full-screen menu blur candidate

Normal ROM: PD6480iperf-v84-fullscreen-menu-blur.z64.

Fixes the pause blur sampling only the upper-left quarter and drawing only
that quarter of the screen. The resulting stale menu/eyepiece fragments during
left/right swipes are gone in the tested captures. Normal menu projection and
light animations remain enabled.

Video Options now reads **Hi-Res: 640x480i (fixed)** instead of offering an
inactive checkbox. v83 already rendered full 640x480i with either checkbox
value; v84 makes this explicit. Stock saved preference data stays compatible.
The newer performance code, two-framebuffer boot fix and L FPS graph remain.
This is not a claim that 480i is faster than stock low-resolution rendering.

## Validation

- Normal ROM: cold software boot with Dark, CI movement, L toggle, Video
  Options and both pause-menu swipe directions; actual resident code checks,
  full 640x480 buffer dimensions/HAF1 timing and no OOM.
- Normal ROM on original N64: USB upload followed by different animated intro
  frames through Elgato. Not an unchanged-ROM interactive hardware test.
- Separate scripted hardware diagnostic: file/pause menus, full-screen blur,
  swipes, CI gameplay and the fixed-resolution label. It uses synthetic pad
  samples, programmatic file/menu setup and a RAM-only Dark save. Its menu
  source files are identical, but it is NOT the distributed normal ROM.
- Actual-C blur regression tests, 400 buffer-order transitions, seven RDRAM
  tests and four stock-save tests pass. 1403 compressed assets and 60 pad-cover
  extents pass; 608 raw assets are outside the compressed-stream audit.
- Xdelta decode reproduces the exact candidate SHA256.

Analogue3D retest, long sessions, multiplayer and on-device save import remain
unverified. Cold launch v84; do not restore an older build's savestate.

## Patch and Dark save

The ZIP contains only xdelta, matching-name .eep, README and manifest, no ROM.
Apply to the user's clean USA V1.1 big-endian .z64:

Base SHA256: 4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21
Output SHA256: 401d5507968d5a37756dad280a43d89d481fbbdf21fc79eeaa0edccdfb98c6d7

Back up existing saves before import. The .eep is a synthesized, checksummed,
2048-byte stock-format 100% agent named **Dark**, not a savestate or embedded
ROM modification. Follow your device's normal EEPROM import procedure; keep
the save and ROM basenames matched. No existing user save was overwritten.

Private source: Cyiatic/PD6480iperf, experiments/v84-fullscreen-menu-blur,
runtime commit 762b7e4914749151162d194d6c13a29a19af8ae8.
Detailed results: evidence/v84-fullscreen-menu-blur and v84-menu-blur-replay.

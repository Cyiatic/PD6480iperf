# PD6480iperf v85 — full-screen menu blur / allocation candidate

Normal ROM: PD6480iperf-v85-blur-allocation.z64.

Includes v84's fixes for upper-left-quarter pause blur and the stale
menu/eyepiece fragments during horizontal menu swipes. Normal menu perspective
and light animations remain enabled. Video Options explicitly reads
**Hi-Res: 640x480i (fixed)**; there is no inactive checkbox. The full640x480
render/depth buffers, newer performance code, boot fixes and L FPS graph remain.
This is not a claim that480i is faster than stock low-resolution rendering.

v85 additionally reduces the pause texture reservation from19200 to its actual
2400bytes. Its40x30RGBA16 texture, full-screen sampling and full-screen coverage
are unchanged. The saved16800bytes fix a Defection room-preload failure found
after the earlier v84 Institute checks, without removing preloaded rooms.

## Checks and limitations

- Normal-ROM software: fresh stockDark boot, Defection and Air Base selection,
  movement/firing/pause/both menu swipe directions. Defection also resumes,
  moves/fires again and toggles L. All required room geometry is present;
  Defection's vertex-batch allocations were separately checked. OOM0 in these
  normal tests; resident code and640x480/HAF1 configuration verified.
- Normal-ROM original N64: ED64 upload and fresh Elgato animated intro beyond
  product identification. Not unchanged-ROM interactive gameplay evidence.
- Separate CI diagnostic on original N64: file-menu swipes, CI gameplay and
  L graph, pause swipes/full-screen background, fixed-resolution label and
  return to gameplay observed through fresh Elgato footage. It uses synthetic
  input, programmatic setup and RAM-only Dark, NOT the normal ROM. Its actual
  menu-rendering/allocation sources match v85. Software replay also finishes
  with OOM0. Diagnostic ROMs are not included in this bundle.
- Actual-C blur/allocation checks,400buffer-order transitions,7RDRAM tests,
  4stock-save tests,1403compressed assets and60pad-cover extents pass.
  The608raw assets are outside the compressed-stream audit. Xdelta roundtrip
  exactly reproduces the candidate hash.

This remains a test candidate. Defection has little spare memory in these
samples; long sessions, other mission coverage, multiplayer, Analogue3D v85
and on-device save import remain unverified. Two separate Defection diagnostics
failed a vertex-batch allocation because their memory layout differs; neither
was called a hardware pass. See the detailed evidence rather than equating
an intro, emulator sample or synthetic replay with complete game validation.

Cold boot this candidate; do not restore another build's savestate.

## Patch and stock Dark save

The ZIP contains xdelta, matching-name.eep, this README and manifest, no ROM.
Apply to the user's clean USA V1.1 big-endian.z64:

Base SHA256:4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21
Output SHA256:430f09bbe0b76bfe687881c52ac23ec4cfff0cc4a16b9ba5faecd602ffc037a4

Back up existing saves before import. The.eep is a synthesized, checksummed,
2048-byte stock-format100% agent named **Dark**, not a savestate or embedded
ROM modification. Use your device's EEPROM import process and keep save/ROM
basenames matched. No existing user save was overwritten.

Private source:Cyiatic/PD6480iperf,experiments/v85-blur-allocation,
runtime commit21f656613b6e78c248d99dd0359b49b202ba591d.
Detailed results:evidence/v84-mission-regression and evidence/v85-blur-allocation.

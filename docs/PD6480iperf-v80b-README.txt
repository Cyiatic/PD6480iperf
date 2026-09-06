PD6480iperf v80b - DEVELOPMENT CANDIDATE, not a verified full-game release

Fixed full 640x480i colour/depth buffers with inherited performance changes.
L toggles the FPS graph, including the FB 640x480 readout.
The legacy Hi-Res checkbox changes only its stored option: full resolution is
active either way, with no live video-buffer reallocation.

v80b adds a yielded RSP/RDP task-ownership fix and waits for complete boot
graphics tasks before reusing descriptors. It retains v79's pad-cover fix.
This is NOT the rejected first v80 build and is NOT the diagnostic replay ROM.

Exact normal ROM: emulator cold boot, L graph, Hi-Res on/off, movement with it
enabled, and short Perfect Agent Defection/Skedar/War checks pass. The exact
downloadable ROM also reaches the animated 3D intro on original N64 via ED64.
A SEPARATE instrumented N64 replay shows synthetic CI movement, Hi-Res
checked/unchecked/checked, and graph off/on. That is not an unchanged-ROM
interactive-controller or physical-save-import pass. See TEST-NOTES.md.

Analogue 3D, broad/extended play, multiplayer, normal interactive console
controls and console save import remain UNVERIFIED. Cold-launch this ROM;
do not restore an emulator or Analogue state from an earlier build.

The candidate retains the older performance core plus selected later fixes;
it does not yet include all 75 later commits in the newer pd-perf lineage.
Whole-level room preloading remains disabled to fit memory; a bounded/adaptive
cache is used. Speed gains are unbenchmarked. Full newer-patch integration
remains work in progress, not an omitted requirement.

Includes a synthesized stock-format 100% save named Dark, 2048-byte EEPROM.
Back up your existing save before import. If you rename the ROM, rename the
.eep to the same base filename. Tests did not overwrite a physical game save.

ROM: PD6480iperf-v80b-rsp-rdp-yield.z64
ROM SHA256: adfe018ce716d168584326c47f16992ef015a3ea91eec46f7ebabe0442a311c0
Xdelta SHA256: 42664dd3fe6f3089a970e0bb1165211d937e35f79f940d271cf8cd7d07d42cce
Patch base: Perfect Dark (U) (V1.1) [!].z64
Base SHA256: 4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21
Save SHA256: fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d
Xdelta decode was verified byte-for-byte against the packaged normal ROM.
Private source: Cyiatic/PD6480iperf, commit c76b706cbba427324698d4bbc65b7fc74d437528.

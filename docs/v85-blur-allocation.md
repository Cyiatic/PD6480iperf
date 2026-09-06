# v85: right-size the pause texture allocation

Runtime commit21f656613b6e78c248d99dd0359b49b202ba591d on
experiments/v85-blur-allocation, built2026-09-06Phoenix.

The v84 pause fix samples the complete640x480 framebuffer into the existing
40x30RGBA16 texture and draws a complete viewport quad. menuReset still
reserved0x4b00bytes, although both actual producer and RDP consumer use2400.
Share width/height/byte count in menugfx.h, use them in the consumer, and
allocate ALIGN16(BLURIMG_BYTES). This saves16800stage-heap bytes without
changing visual quality, render/depth resolution or room/weapon preloads.

The normal ROM retains all previous modern performance, L graph, logo
buffer-ownership and full-screen menu fixes. Video Options says
Hi-Res:640x480i(fixed), with no inactive checkbox. Stock saved preference
data and external stock-format Dark EEPROM remain compatible.

Normal-ROM software regression found v84 Defection missing room167 after a
61328-byte allocation failure. v85 loads all167rooms AND their vertex batches;
room167 has252batches,8064bytes. Movement/fire/pause/both swipes/resume/L pass,
with OOM0 and4176bytes expansion-stage free at the final1194frame sample.
Air Base also passes load/move/fire/pause/swipes, all146rooms,OOM0,15872bytes
free. Memory margin remains small; these are not whole-game stability claims.

Normal v85 original N64 USB test showed distinct animated intro frames past
product identification through fresh Elgato capture. This alone does not
verify unchanged-ROM interactive gameplay. Separate diagnostic evidence and
all current limitations are maintained in the private distribution branch:
evidence/v85-blur-allocation. Two Defection diagnostics consume enough extra
memory to fail a vertex-batch allocation; neither was uploaded or called a
hardware pass. CI diagnostic is tracked separately, not a release ROM.

Actual-C blur/allocation tests,400buffer-order transitions,7RDRAM tests and
4stock-save tests pass. Compressed ROM assets1403valid,0invalid,608rawunchecked;
60pad-cover extents valid. Xdelta roundtrip is exact. No synthetic input,
RAM-only save or watchdog is linked into the normal candidate.

Normal ROM SHA256430f09bbe0b76bfe687881c52ac23ec4cfff0cc4a16b9ba5faecd602ffc037a4.
ELF81af590340c372b80d4d9c3bcada0056566505a2ce482de4ec11f618a8d0ad5a.
CRC37b134c9/fedfa470. Patcha103d3623b0d69769003fced937c279d13764e31911069f5ba354082882c414b.
Analogue3D retest, long sessions, multiplayer and physical save import remain
open. Cold boot; do not restore a prior build's savestate.

Push only to private Cyiatic/PD6480iperf, never the public origin.

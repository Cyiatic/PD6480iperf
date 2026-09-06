# v82b: shared menu scratch before callbacks

Fixes the v81b/v82 lazy-menu integration regression. The 153600-byte per-menu
storage is used for briefing setup/language data and multiplayer challenge
descriptions as well as model previews. Allocation now occurs on first CI
menuPushDialog, before reset, focus, sibling or dialog callbacks. A failed
allocation returns before opening a dialog with a NULL buffer. Unused player
menus remain unallocated. No physical save, input or diagnostic hooks added.

ROM SHA256 9da54bbde7d42be0441af6031de1711fe647f3a4036e5ca9da381ccc0cea30b1
ELF SHA256 3f7b1c5165585023087dddfe8b7fb2ee0cb523c520bbeb76f8a8c3b16b902fa8
CRC1/2 3387f33c / 891c1995

Fresh 5100-tick cold emulator test: CI frame 1178, all 140 room geometries
resident, 331040 expansion stage bytes free, OOM=0 and both inspected threads
have no exception flags. The L graph is visible. Final screenshot shows the
Skedar Ruins mission overview with objectives, Accept/Decline and the animated
model. Both prepared VI slots have ctrl=305e, width=1280, vSync=524,
xScale=1024, origins=1280/2560 and yScale=1024/1024. Logical image is 640x480,
colour pointers 8036a000/8076a000; depth is a full 614464-byte allocation.

These facts are emulator observations, not a console/Analogue pass, not an
FPS benchmark and not complete newer-patch parity (triple buffering has been
adapted to double buffering). Hi-Res option interaction, mission transitions,
larger levels, multiplayer and extended play need further testing. All 1403
compressed assets pass; 608 raw assets remain unchecked. Earlier v80b package
is unchanged. Hardware observations are recorded in the distribution repo.

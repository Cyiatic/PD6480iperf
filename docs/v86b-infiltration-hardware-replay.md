# v86b Infiltration hardware replay — diagnostic only

Based on modern v86b (`ea2ad550b`, documentation update `ca431f547`). The normal
candidate remains the immutable c33ec145... ROM; this branch must never be
distributed as that candidate or merged into its runtime branch.

Reuse the previously reviewed lean v85 input/save diagnostic, not its old
runtime files. Select stock Dark and Infiltration / Perfect Agent through actual
menu handlers, then exercise ordinary input consumers for movement, L graph and
menu swipes. Video Options must contain the fixed-mode label; no resolution
checkbox toggling is claimed. Sample injection occurs only in the main thread's
newly acquired controller partition, preserving physical presence/error status.

The 2048-byte stock Dark EEPROM is embedded as mutable RAM. Physical EEPROM
access is replaced only in this diagnostic. Controller/Transfer Pak writes are
blocked. No watchdog task is linked. An always-visible V86B TEST label includes
phase, stage, difficulty, OOM, required BG-load failures, eviction/miss counts,
framebuffer size, RAM save counters and position. It remains visible when L hides
the normal graph, so synthetic footage cannot be mistaken for an unmodified ROM.

Actual input-partition and RAM-EEPROM C tests pass. Build from 89e484caa succeeds.
Diagnostic ROM SHA256 39082bc3857e1f1728e3f3dcfe2e733815774061d3b34f5469a617cb2bb09e59;
ELF a0f982ffc05213b64f43f3d8a4b300c3e0360d75741a747946b537080fb3405a;
CRC e78d0222/5292c950. These are NOT the normal c33ec145... candidate.

Cold 7500-tick software replay (no external save, state or controller input)
reaches Infiltration / Perfect Agent. Visually inspected frames 3900, 4800 and
5700 show movement, L graph changes, full-screen menu blur and resumed 3D,
with V86B TEST / ST47 D2 / FB640x480 / OOM0 / BGFAIL0 / EVICT6 identification.
The final RAM sample is phase8, one fixed-label check, save R56/W24, valid room
heap, six evictions and zero allocator/load/CPU faults. However the unattended
player has subsequently died (player_dead=2, health<0, pause3, level frame1673).
This is normal combat death, NOT a sustained-unpaused-play pass. Do not hide
that final condition or claim a full mission clear from the earlier frames.

Hardware diagnostic 1 reached CI and Infiltration with OOM0/BGFAIL0/EVICT6,
but died before the pause test and incorrectly continued through death menus.
That result is not an alive pause-blur pass. Normal c33ec145... separately
reached the animated 3D city/rooftop intro via ED64 and fresh Elgato capture.

Revision 2, source fa662646b, shortens phase3 from 720 to 180 ticks, checks death
before/through pause tests and phase7, and adds DEAD to the HUD. No gameplay
health, AI, difficulty or normal rendering/cache code is changed. Actual input
partition and RAM-save C tests still pass. ROM
a200942799b7b9ed02b3513763dc1bc00f381ea22682f5d63b553b4a10734fc9;
ELF e348b1d7f09f946714db525434d86f791140639776acaec5642286597d21a008;
CRC de8153dd/81df8378. Exact FTDI reset while OFF plus 35-second dwell gives
native upload exit0 in36.8s, then fresh Elgato confirms alive Infiltration,
full-screen pause blur, both menu directions, fixed640x480i label and L changes.
The menu closes back to3D only briefly before enemies kill the player; phase99
correctly stops the replay. This is NOT a sustained/full-mission pass.

Matching software6000 also performs alive pause and label tests, then dies:
phase99, DEAD2, pause3, frame762, OOM/cache/allocator/CPU faults0, evictions6,
valid heap and640x480. RDRAM4c16a0f2f0004a5f4c19f28c88875923d0503ee7026148130cde8340e1ab4472.
Final failures/death conditions are retained. No physical save writes occur.
Plug1OFF confirmed20:16:59/20:17:00UTC. Detailed hardware evidence lives in
the private distribution branch evidence/v86b-hardware-transport. Diagnostic
ROMs are not user candidates and must not be merged into the normal branch.

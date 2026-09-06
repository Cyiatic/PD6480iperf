# v82b — newer performance core, full 640x480i

Development candidate, not a finished full-game or Analogue-verified release.
Normal source: `24995c1c66eaa0e4ac5568f5711f7af7678b5561`, private branch
`experiments/v82b-menu-scratch` in Cyiatic/PD6480iperf.

## Integration

Unlike v80b's older core with selected backports, v82b starts from newer
performance commit `bf3245076d00fbbb29ca1e0906672381f2d43a52`, including its
75 intervening commits. Newer AI/math/DMA optimizations, uncached writes,
whole-level room geometry preloading and weapon preloading remain enabled.
This is not byte-identical to upstream: fitting genuine full-resolution
buffers required adapting its three colour buffers to two and allocating
CI's shared per-player menu scratch only when each player's menu is opened.
No claim of measured speed gains or identical triple-buffer performance.

Two full 614400-byte colour buffers, full 614464-byte aligned depth storage,
640x480 logical geometry and HAF1 alternating-field VI registers are used.
Both game/VI tables are configured consistently. Dispatch gates protect
current/next VI and scheduled/queued image ownership; retrace retries delayed
work. Boot submits only after previous copyright graphics work has completed.

The first lazy-menu attempt caused a separate regression: briefing/challenge
callbacks also need that scratch before any model preview renders. v82b
allocates before dialog callbacks. This fixes the reproduced v82 NULL-buffer
briefing exception. It is not proof of the cause of every earlier Analogue
crash reported in this task. Failed v81/v81b/v82 builds are not candidates.

L toggles the FPS graph. The stock Hi-Res checkbox is retained as a stored
preference, but rendering stays full 640x480i in either state; toggling it
does not resize/reallocate video buffers.

## Checks performed on the normal binary

- Fresh emulator boot using the synthesized stock Dark save reaches CI and
  Skedar's briefing, with all 140/140 CI room geometries resident, no OOM and
  no main/scheduler exception. 331040 stage heap bytes remain available.
- A matching-state mission transition loads all 137/137 Skedar room geometries
  and reaches its cutscene. Further ordinary Start/stick/Z inputs reach actual
  first-person play, move rooms [10,4] to [9] and consume eight pistol rounds.
  The player finishes alive, full health, unpaused and outside a cutscene.
- Matching-state Video menu inputs switch Hi-Res on/off/on and L off/on.
  Returning to CI gameplay with Hi-Res enabled advances the level from frame
  1355 to 2191, with position movement and unchanged 640x480 buffers, no OOM.
- These use ParaLLEl N64 2f3bf60, cached interpreter, cxd4, Angrylion, 8 MiB
  and the documented in-memory save-header adapter. No gameplay RAM edits.
  Warm states are from this exact binary, not an earlier candidate.
- Original N64: this exact normal ROM was separately uploaded and observed
  rendering different city/rooftop intro frames on 2026-09-06. This proves
  progress beyond product identification, not unchanged-ROM interactive play.
  See evidence/v81-v82-modern-memory for timestamps, stills and limitations.
- All 1403 compressed assets and 60 pad-cover extents pass static checks;
  the 608 raw assets remain outside the compressed-stream audit.

Emulator screenshots or composite capture dimensions alone do not prove native
console render resolution. Full buffer dimensions and prepared interlaced VI
registers are checked against the compiled source/ELF and emulator RDRAM.

## Separate synthetic replay

Private diagnostic source `62b586382` on `diagnostics/v82b-console-replay`
adds scripted input, programmatic file/menu setup, a RAM-only Dark save and
an always-visible yellow V82B TEST label. Physical Controller Pak writes are
blocked. It is a separate binary and must not be distributed as the candidate.

Fresh 8400-tick emulator replay completes phase 8, all three Hi-Res checks,
Hi-Res=1, graph=1, CI unpaused at level frame 5815, no OOM. It produces 7479
video frames. RAM-only save reads/writes are 56/24. The save transfer routine
passes boundary/null/round-trip tests; seven newer-core inspector tests and
four stock-save tests pass. Hardware results belong in a separate evidence
record and must not be inferred from this software test.

Hardware follow-up: the separate v82b replay repeatedly blackscreens after
product identification. A v82c replay-only change preserves physical controller
status; it passes the software tests but does not fix that hardware failure.
The normal v82b control still reaches the animated city intro. These facts
do not establish normal-ROM in-game hardware compatibility. See the separate
evidence/v82b-console-replay and evidence/v82c-console-replay records. No new
candidate package was created during these unsuccessful physical replays.

## Identity and open validation

- Normal ROM SHA256: `9da54bbde7d42be0441af6031de1711fe647f3a4036e5ca9da381ccc0cea30b1`
- Normal ELF SHA256: `3f7b1c5165585023087dddfe8b7fb2ee0cb523c520bbeb76f8a8c3b16b902fa8`
- ROM CRC1/CRC2: `3387f33c` / `891c1995`
- Patch base: stock Perfect Dark USA V1.1, SHA256
  `4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`.
- Synthesized stock-format 100% Dark EEPROM (2048 bytes), SHA256
  `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d`.

Back up existing saves before importing Dark. Rename the .eep to match the ROM
basename if renaming the ROM. Cold launch; do not restore an older build's
emulator or Analogue state. Physical save import remains unverified.

Analogue, unchanged-ROM physical-controller gameplay, broader missions,
multiplayer, extended play and performance comparisons remain open. The
recovered heap margin is not a multiplayer guarantee; multiple simultaneous
CI menus require further testing. Do not mark the overall goal complete.

# v79: correct emitted pad-cover counts

Development candidate with limited original-N64 intro evidence; not a verified
full-game or Analogue 3D release.

Source commit `d21f1c8c9401b460ccc002c480d1caa08544ba0b`, branch
`experiments/v79-pad-cover-count` in the private Cyiatic/PD6480iperf repo.
Parent: v78 source `302cfcb1c`.

The performance pad generator already filters out special cover records, but
its header still counted every JSON row. v79 derives the header count from the
emitted byte length divided by the 28-byte record size. The existing filtering
behavior is unchanged; this does not claim full stock AI equivalence.

The exact v78 ROM fails structural bounds checks for four pad files: mp1, pam,
sho and stat. War uses stat. Its setup normalizes vectors past the loaded cover
data and corrupts the neighboring model bindings, leading to a debris-model
fault. See [v78's failure evidence](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/PD6480iperf-v78.md).

The corrected actual generator passes in-memory count/bounds checks for all 60
NTSC-final pad sources, including the four with filtered records. New exact-ROM
checks independently read the ROM file table, inflate its pad assets and verify
their declared cover extents. Unit tests reject overstated/understated counts
and truncated headers.

The rebuild completed successfully with the four affected JSON inputs forced
newer via make's `-W`. Dependent C objects were also recompiled.

ROM: `PD6480iperf-v79-pad-cover-count.z64`, SHA256
`c618b23fc61cf21e4221221544bacaf6a6749d6863a237a3118daa511cef12b6`.
CRC1/CRC2: `9b29266a` / `8f47148e` (unchanged; these do not cover the changed
assets, so use SHA256 to distinguish the builds).
ELF SHA256: `56a27fda97279dfcbfd70173ccd9efb7f8bf2269a9170f9b0b4cae9cf496dda1`.

The exact ROM passes all 60 pad cover-count/bounds checks and all 1,403
compressed-asset checks. The two mode entries remain 640x480, colour storage
1,228,864 bytes and depth storage 614,464 bytes.

The file table and ROM bytes before/after the asset area are unchanged. Four
pad streams differ only in their inflated header count word. One additional
regenerated asset, `FILE_UMP_SETUPDAM`, has an identical 1,341-byte prefix but
omits the previous three trailing zero bytes. All other file payloads are
byte-identical. Do not describe this as a four-file-only binary change.

A fresh 5,100-tick emulator boot selected Dark, entered CI, enabled the L graph
and navigated to the Skedar briefing. Its active dimensions are 640x480, with no
allocation-failure marker. This state was not reused from v78.

## Targeted runtime regression

From that fresh matching briefing state, instrumented mission selection plus
normal Accept Mission/Start/stick inputs pass initial gameplay checks in War,
Skedar Ruins and Air Base (2,100 ticks each). The resident code matches the v79
ELF, active buffers are 640x480 and all three have no allocation-failure marker.
War finishes that sequence in its pause menu after reaching level frame 491.

A separate continuation closes War's menu and applies stick movement for 1,200
ticks. It produces 1,198 frames, advances the level-frame counter to 1,333,
changes the view, retains 640x480 and records no allocation failure. This tests
past the v78 frame-165 fault; it is not a full War playthrough.

## Broader initial-mission matrix

All 21 solo missions pass the initial-load gate on this exact v79 ROM, at
Perfect Agent difficulty and 2,100 host ticks each. The other 18 missions use
the same fresh v79 briefing state and selection instrumentation as the three
targeted tests. This supersedes v78's 20-of-21 initial-load result; it does not
reuse v78 RAM states or claim completed missions.

The collected `artifacts/tests/v79/mission-results.json` rechecks the exact
ROM/ELF hashes, resident code, final RAM and unique 21-stage count. Every final
snapshot has 640x480 active dimensions, no allocation-failure marker, gameplay
tick mode, cutscene mode off and a level-frame count above 100. Seventeen final
snapshots are unpaused. War, Maian SOS and Mr. Blonde's Revenge finish in pause
menus; The Duel finishes in a retry menu. These four remain initial-load
passes, not active-play or completion claims. War's separate continuation
described above clears the pause state and advances from frame 491 to 1,333.

All 18 new final images were visually inspected. Some stick-input sequences
leave the camera against a wall; they do not establish room-by-room traversal.
The pause fields were measured with the candidate MIPS ABI, not inferred from
old source offset comments. The collector rejects incomplete coverage and a
mismatched v78 ROM without producing a result file.

## Menu, patch and automated checks

The V1.1 xdelta decodes byte-for-byte to the candidate ROM. Patch SHA256:
`e44df2d383c51cbf7dcd01efd9cfca6873e8d074fc020e529c015891b2350a4f`.

Actual CI Video Options inputs enable Hi-Res in a fresh v79-derived state. From
that enabled state, A disables it over a 900-tick continuation (900 frames,
Hi-Res=0, 640x480, no allocation failure). A separate 1,200-tick continuation
keeps Hi-Res enabled, closes the menu and applies stick movement. It produces
1,199 frames and advances the level-frame counter from 603 to 1,158, retaining
Hi-Res=1, 640x480 and no allocation failure.

Additional automated gates: 23 Python allocation/asset/save/code-identity/cover
bounds/pause-state tests pass; the actual pad generator passes all 60 source
inputs; the actual mema allocator passes 10,000 fragmented operations; and the
bounded room retention-policy tests pass. These do not benchmark real N64 speed.

## Original N64 / ED64 / fresh Elgato evidence

On 2026-09-05, the exact v79 ROM was successfully uploaded twice in 36.53 and
35.92 seconds. Two earlier attempts stalled while the EverDrive menu remained
visible. Recovery included switching only Plug 1 off, restarting the exact
FTDI device `USB\VID_0403&PID_6001\AB0NWMD3`, powering Plug 1 on and uploading
with GameCapture closed. The driver restart and capture closure were changed
together; this does not establish which action resolved the stalls.

The first successful capture showed logos only. The second run's fresh
102.594-second Elgato recording, created at 21:12:11 America/Phoenix, showed:

- 50 seconds: aircraft among city buildings (`n64-intro-50s.png`).
- 65 seconds: a different city/traffic camera view.
- 80 seconds: the rooftop sequence.
- 95 seconds: Joanna on the rooftop (`n64-intro-95s.png`).
- 97 and 99 seconds: black frames.
- 101 seconds: the Rare logo (`n64-logo-101s.png`).

These changing scenes establish progression past the logos through an animated
3D opening. The black interval was not a persistent black screen in this
recording. They do not establish interactive console gameplay, successful
console Hi-Res toggling, measured native framebuffer dimensions from the
capture alone, or operation on Analogue. No physical controller input was
automated during these console runs. A logo frame must not be described as a
level scene.

The source's `aiEndLevel` explicitly sends title-demo playback back to
`STAGE_TITLE`; returning to a logo is consistent with that path, although the
capture does not reveal the executing CPU state.

Plug 1 was switched OFF at 21:13:56 and independently reported `Relay: 0` again
at approximately 21:19. The unrelated N64 outlet and parent switch were not
operated. GameCapture was stopped. This recording and its three metadata files
were permanently deleted after inspection (191,254,374 bytes); small evidence
stills were retained. Earlier v79 run recordings/metadata were also deleted
(568,882,388 bytes from stalled attempts and 106,080,650 bytes from the short
successful capture). No existing console save was overwritten.

## Remaining gates

A subsequent **separate instrumented v79-based ROM** passed a limited
original-N64 synthetic-input CI movement / Hi-Res on-off-on / L off-on sequence.
See [the diagnostic report](PD6480iperf-v79-hardware-replay.md). That test uses
RAM-only saves and programmatic setup, and does not upgrade this unchanged
candidate to an interactive-console or Analogue pass. Its download is unchanged.

Use a fresh ROM launch, not a v78 emulator/Analogue state: resident code may be
unchanged while loaded asset contents are old. Long play, multiplayer,
interactive console controls, console save import and Analogue remain
unverified. Whole-level preloading is still disabled and real N64 performance
has not been benchmarked.

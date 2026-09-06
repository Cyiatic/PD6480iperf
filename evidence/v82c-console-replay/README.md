# v82c diagnostic — software pass, hardware FAIL

2026-09-06, America/Phoenix. Isolated private branch
`diagnostics/v82c-preserve-controller-status`, source `554a82ae7`.
Normal v82b ROM/source are unchanged. This is not a user candidate.

ROM SHA256 `c5326346c1fcab27913f4b6b3ddde9c2b726fd0c96e4c35349958117069e3d9f`.
ELF SHA256 `a0811c72c3c06e59c982ed16da27653f01f3a1a37c3163e9decbb359478731cd`.

Changes from previous diagnostic: preserve physical pad errno status while
injecting button/stick inputs, plus V82C TEST label. No rendering, scheduler,
save format or memory-allocation changes. See source-notes.md.

## Software

The actual input-partition writer passes all 400 first/last boundary pairs,
preserves prior/next partitions and controller-presence status, and rejects
the negative control that reintroduces errno=0. Actual RAM EEPROM routine
passes round-trip, overrun/null and guard checks. Inspector suite: seven pass;
stock-save suite: four pass.

Fresh 6900-tick emulator replay completes with 5980 video frames, phase 8,
three Hi-Res checks, Hi-Res=1, graph=1, CI unpaused, OOM=0; attached final JSON
contains exact state/code hashes. The same cached interpreter/Angrylion/cxd4,
8 MiB and save-header adapter were used. No input/state/save file or gameplay
RAM edits; the diagnostic embeds its scripted input and RAM save.

Both this and the older failed diagnostic have connected controller mask 1
in emulator RAM, despite the startup log listing four Standard controllers.
The fixed status overwrite is real but was not proved to cause the blackscreen.

## Original N64 — failed after product identification

Only Plug 1 was used; unrelated N64 outlet and parent untouched. Plug 1 ON /
owned GameCapture PID 13760 started 00:59:11. Recording began 00:59:48. Fresh
3-second still shows EverDrive before upload. Diagnostic upload began
01:00:17.902, ended 01:00:54.139, native exit 0 (36.237 s), capture running.

Video mode transition made a new segment at 01:01:06. Its 2-second still shows
product identification with Expansion Pak detected. Stills at 10, 45 and 100
seconds are black. No CI, diagnostic HUD or toggles observed. Preserving
controller status did NOT resolve this hardware failure. Do not reuse the
normal v82b intro pass as an in-game diagnostic pass.

Capture stopped and Plug 1 OFF confirmed 01:03:39. Segments lasted 74.562 and
152.236667 s, sizes 138954372 and 284167076 bytes, SHA256 respectively:

- `944f3e981525c3cb68bad2ab1e8ffea3f833addf796db104d643854f95fda1d9`
- `bb2c8bef3a13d846ba4ef3bd83caffaf7bd0f0e3b527b2bc26fbca1f581ecf33`

Both recordings and four associated metadata files were permanently deleted
after inspection, reclaiming 423241618 bytes. Small stills remain. Across
this work interval, inspected capture cleanup reclaimed 1464589204 bytes.

Next investigation: isolate replay, RAM-save and Pak-write blocker effects
before attributing this diagnostic-only observed failure to the normal render
code. The exact normal v82b has emulator gameplay/toggle checks and physical
intro progression, but still lacks unchanged-ROM interactive-console and
Analogue validation. No new ROM/xdelta package was created here.

After testing, the source worktree was switched back to the clean normal
experiments/v82b-menu-scratch branch and rebuilt with a forced link-script
refresh. The retail-header ROM exactly reproduces normal SHA256
9da54bbde7d42be0441af6031de1711fe647f3a4036e5ca9da381ccc0cea30b1;
ELF exactly reproduces 3f7b1c5165585023087dddfe8b7fb2ee0cb523c520bbeb76f8a8c3b16b902fa8.
No pdHw / g_PdHw / g_PdAlloc symbols are present. Diagnostic branches and named
diagnostic ROM/ELF files remain separate for investigation. No active capture,
uploader or emulator run remains after this interval.

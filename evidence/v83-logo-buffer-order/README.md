# Normal v83 validation — 2026-09-06 America/Phoenix

Source 144053982f2b42389946814d94d15633bc69c89b, private branch
experiments/v83-logo-buffer-order. Only runtime change from normal v82b is
preserving VI front/back index parity through logo reconfiguration. ROM/ELF
identities in artifacts/PD6480iperf-v83-manifest.json. No pdHw/g_PdHw/g_PdAlloc
symbols in the ELF. The separately tested v82h replay is not this binary.

## Exact binary, software

Fresh 5100-tick cold boot using stock Dark EEPROM and the included previous
headless-cold-briefing controller script: CI frame 1178, 4179 video frames,
640x480, no OOM; 331024 expansion heap bytes free. Cached interpreter,
Angrylion/cxd4, 8 MiB, host save-header adapter only, disk ROM unchanged. No
gameplay RAM edits. Cold screenshot/JSON attached.

From this exact v83 state, concatenated ordinary menu inputs (1080 ticks) open
Video. Subsequent same-binary states: 450 ticks Hi-Res on/graph off; 300 ticks
Hi-Res off/graph on; 1050 ticks Hi-Res on, unpause, turn and walk. All expected
states pass. Final CI frame 2191, unpaused, alive/full health, position
(752.99994,483.99957,589.69794), full 640x480, Hi-Res=1, graph=1, no OOM,
331024 expansion heap bytes free. JSON records check code hashes, buffers,
thread exception fields and both prepared HAF1 VI modes. These warm-state
checks are not independent cold boots or cross-build saved states.

Static compressed asset audit: 1403 valid, none invalid, 608 raw unchecked.
Pad-cover extents: all 60 valid. Actual compiled logo-order routine passes 400
parity/alias transitions; old reset negative control fails. Stock-save four
tests and newer-core inspector seven tests previously passed unchanged code.
Patch application to clean USA V1.1 exactly reproduces the output ROM hash.

## Exact binary, original N64 intro only

Bounded worker PID 24836 started 08:29:06 after prior diagnostic cleanup.
Plug 1 ON 08:29:08.799. Upload PID 14152, 08:29:20.945 to 08:29:57.563,
native exit 0. Owned capture PID 4940 started 08:29:57.602; video began
08:30:31. The fresh 5-second image is black; 30 and 65 seconds show different
animated city intro frames without diagnostic HUD. This confirms the exact
normal candidate progresses beyond product identification, NOT interactive
physical-controller gameplay or Analogue compatibility.

Capture stopped 08:31:58.821, Plug 1 OFF 08:32:00.109, status Relay 0 at
08:32:00.948 and independent recheck 08:32:48. Only Plug 1, not N64/parent.
Recording 163320488 bytes, SHA256
df83f79a48305b789c84f1725c76e09065962a23d4fd70fb74210ec214ecb81f.
Four inspected recording/metadata files permanently deleted (163366534 bytes).
Small stills and logs retained. No capture, uploader or emulator test remains
active when packaging. See separate v82h record for physical scripted gameplay
and all three Hi-Res checks; do not conflate those tests with this normal ROM.

Analogue, unchanged-ROM interactive controller test, physical EEPROM import,
multiplayer, extended sessions and broader missions/performance remain open.

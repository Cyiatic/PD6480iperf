# v79-based original-N64 controller replay B

**Limited diagnostic hardware pass, not release acceptance.** On 2026-09-05,
fresh Elgato footage from the original N64 showed CI gameplay movement, Hi-Res
on/off/on, return to gameplay, L graph off/on and further movement without an
observed freeze. The ROM is separately labeled `HW-REPLAY-B-NOT-RELEASE`; the
normal v79 candidate and its download were not changed.

## Identity and test method

Diagnostic source commit `72c02046c9fd042b89baba87d06f2e8132ba0e75`, private branch
`diagnostics/v79-console-replay`, based on v79 `d21f1c8c9`.

- ROM `PD6480iperf-v79-HW-REPLAY-B-NOT-RELEASE.z64`, SHA256
  `8886703fba772fc96984bf7448e3f16d0221df228a8d08eba37c9604b64a0366`.
- ELF SHA256 `f5c6bccf04a1cab005cede86220e0ddfcf29b47737d26b62e1ca1f3b1d80dc32`.
- CRC1/CRC2 `d8d2ae55` / `52de9f43`.

Synthetic pad samples use the game's existing replay interface and normal
input consumption for Start, B, C-down, A, L and sticks. Dark file selection
and opening Video Options are direct setup-handler calls, not physical button
navigation. This does not test physical controller polling end-to-end.

The embedded 2 KiB stock-format Dark image lives in RAM only. Game EEPROM
probe/read/write routines are redirected to that RAM array, and the common
Controller Pak/Transfer Pak write routine returns `PFS_ERR_NOPACK`. Static ELF
checks verify those paths; a host-compiled test of the actual copy function
checks round trips, final-block bounds, oversized transfers, null buffers and
unchanged RAM on rejection. These checks do not prove safety against arbitrary
memory corruption and do not validate real EEPROM save import.

Diagnostic A failed its emulator navigation guard because it used D-pad down;
B uses C-down. A was not sent to hardware. The guard's phase 99 denotes a replay
failure, not an automatic game-crash diagnosis.

## Separate emulator evidence

A fresh 6,600-tick run used no external input file, savestate, supplied EEPROM
or save-header adapter. It produced 5,702 frames and completed the sequence:
phase 8, three Hi-Res checks, Hi-Res=1, L graph=1, CI unpaused, level frame 4,028,
640x480 active buffers and no allocation-failure marker. The RAM save recorded
56 reads and 24 writes. The final cache reserved 262,144 bytes, with 244,560
free; stage-pool free space was 137,424 bytes. Only rooms 12–16 were resident;
this is not broad CI traversal or a playthrough.

`artifacts/tests/v79-hardware-replay-B/emulator-report.json` contains the exact
ROM/ELF hashes, checks and final snapshot. Its `hardware_verified: false` fields
are intentional: RAM inspection and ELF dimensions are emulator/static facts,
not measurements taken from console memory.

## Original N64 and fresh capture

Both the exact FTDI ED64 device `USB\VID_0403&PID_6001\AB0NWMD3` and Elgato
`USB\VID_0FD9&PID_0051\110B14E2A7` reported OK. Only **Plug 1** was powered on,
with `Relay: 1` confirmed at 22:06:05 America/Phoenix. GameCapture stayed closed
during `UNFLoader -b -f 3 -r <exact B ROM>`; upload succeeded in 36.48 seconds.
GameCapture was then started at 22:07:03, and its new recording began at
22:07:36. That startup delay means the recording does not show the entire
profile-selection sequence.

Elgato split the recording into two segments. Retained full-frame stills are
under `artifacts/tests/v79-hardware-replay-B/`:

| Segment / time | Directly observed |
| --- | --- |
| 1 / 2 seconds | CI terminal/ceiling view, yellow diagnostic label |
| 1 / 50 seconds | Different CI room view after synthetic stick input |
| 1 / 94 seconds | Hi-Res checkbox checked |
| 1 / 100 seconds | Hi-Res checkbox unchecked |
| 1 / 110 seconds | Hi-Res checkbox checked again |
| 1 / 125 seconds | Menus closed; green FPS graph hidden, yellow label remains |
| 1 / 136 seconds | Graph visible again, changed CI camera view |
| 2 / 85 seconds | Further gameplay, phase-8 diagnostic HUD |
| 2 / near end | Phase-8 HUD remains; no error screen observed |

Menu checkbox interpretation was checked in faithful nearest-neighbor enlarged
crops; the stored evidence images are unedited full frames. Exact tiny numeric
position/frame-counter readings are not asserted from the composite capture.
The second segment also contains further camera movement before phase 8.

An intermediate live check accidentally reread the end of segment 1 after
Elgato rolled over. `live-3.png` and `live-4.png` in the working directory are
duplicates, not evidence of later progress. The table above uses explicit
segment/time extraction, and the final still is from segment 2.

Segment 1: 156.247333 seconds / 290,874,540 bytes, SHA256
`008088f92f61c26c3931652a691fce658dd213a9cd1d6a561e45667d9b4af989`.
Segment 2: 113.463956 seconds / 211,322,904 bytes, SHA256
`17bf482be0dced94f8e16138889d1ab59fcdf149dc1bb559835b33f01fe5aded`.
The 269.711289-second combined duration is capture duration, not a benchmark.

GameCapture was stopped after the run. Plug 1 was switched off and independently
reported `Relay: 0` at 22:15:37 and again after cleanup. The N64 outlet and parent
switch were not operated. Both recording segments plus their two `.meta`,
`.desc` and `.info` files were permanently deleted after inspection: 502,338,088
bytes total. Small stills remain; no physical save overwrite was performed by
the diagnostic's defined EEPROM/write paths.

## What remains open

This is stronger evidence than logos or an attract sequence, but it is not an
unchanged-candidate interactive hardware pass: code, memory layout, input
source and save I/O differ in the diagnostic. Analogue compatibility, physical
controller controls, real save import, broad gameplay and multiplayer remain
unverified. Static ELF modes and emulator active buffers are 640x480; composite
capture dimensions alone do not establish native rendering resolution.

Whole-level preloading remains disabled. The bounded/adaptive room cache is
retained, but real performance improvement has not been benchmarked. This turn
did not restore preloading or change performance behavior. Full patch goals
remain open; do not promote this diagnostic as the final combined patch.

The normal v79 ZIP with the stock-format 100% Dark save remains SHA256
`88ad1d677ca212def50f7cb9fa8a498bae95cd00ef0e8db9168b9f4286c6bc2a`.

# v82d isolation — no verified boot on original N64

2026-09-06, America/Phoenix. Source 3fb5e0a5434e517f1afafe128270d371ec43a8ba,
private branch diagnostics/v82d-no-input-hook. Remove only pdHwReplay call
from v82c; RAM EEPROM, physical Pak-write blocker and unused replay/HUD stay.
Not a candidate; normal v82b is unchanged.

ROM SHA256 cd5e708fda8f86162bcebbc015b6638fd58d2b5c2575f8c076fd431b4d6d75f6.
ELF SHA256 04d86c7e735f579e27cb950efdd972e05d08d32d448802d08b4f5b3f53cc49a9.
CRC1/2 c8a2c5bb / 799b04bf.

Software: fresh 1500 ticks, title stage 90, level frame 1181, 1296 video
frames, phase 0/ticks 0, 25 RAM save reads/zero writes, no OOM. Attached JSON
and screenshot are software evidence only.

## Interrupted original-hardware run and storage cleanup

Plug 1 and owned capture PID 24060 started 01:10:34. Upload 01:11:30.260 to
01:12:06.475, native exit 0. Early segments started 01:11:10 and 01:12:18.
An interrupted agent continuation resumed at 07:30:23 with that capture still
running. Stopped it and confirmed Plug 1 OFF at 07:30:52. This was a lifecycle
failure, not an intended extended test. Earliest segments had rolled away;
do not claim an observed startup sequence from the remaining late footage.

Retained segment 107 at 10 seconds and 147 at 5/90 seconds were black.
Segment 147 SHA256 903e13993dd3ed7d5eef5ac4d9655204063c8d06ce4db361ad09b704dc284e7a.
Kept stills/segment manifest, permanently deleted exactly 84 inspected capture
and metadata files (segments 107–147), reclaiming 11,848,605,756 bytes.

## Tested independent cutoff

Added bounded hidden helper pd_test_watchdog.ps1. Plug 1 ON and owned capture
PID 19676 at 07:37:28; watchdog PID 11156. Deadline shut capture and confirmed
Relay 0 at 07:40:31.759. This verifies the cleanup helper, not the ROM.

Upload started 07:38:39.783 but exited only at 07:40:32.052, after power cut.
Its native exit 0 is NOT a successful transfer. Video remained EverDrive at
140 seconds, no game transition. Recording SHA256
fad0dec19b8f64ee30c83e925d488735a54482adf02b4dc4c592a55acfb8800a.
Inspected recording and three metadata files permanently deleted (276,964,463
bytes). Small menu stills and watchdog log remain.

## Full bounded worker, capture closed during transfer

pd_hardware_trial.ps1 launched independently as PID 22300 at 07:45:25.
Only Plug 1 was addressed. ON confirmed 07:45:27; uploader PID 22284 started
07:45:39, native exit 0 at 07:46:16 before power-off. Owned capture PID 10768
then started. Its fresh recording's 5-second and 75-second images are black.
The camera starts late here, so this run does not document the product screen.
It does show no visible intro at the sampled post-upload times.

Observation ended 07:48:17; capture stopped, Plug 1 OFF at 07:48:18 and status
Relay 0 rechecked. Worker completed. ROM upload is not a boot pass.
Recording SHA256 db96f21625c13b36d2b77c7c26b8c14ced9f55801a8fbe7d5ced655b56dc53fb.
Four inspected recording/metadata files permanently deleted (166,569,302 bytes).

Removing input execution alone did not restore a visible intro in these
observations. RAM-save/blocker/layout/timing causes remain unproved. The next
separate diagnostic adds startup checkpoints and a CPU-rendered timeout state
screen, not another speculative candidate. Normal v82b's previous intro pass
must not be relabelled as diagnostic or unchanged-ROM in-game hardware proof.

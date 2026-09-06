# v82f replay — software completes, hardware timeout localized

2026-09-06 America/Phoenix. Private branch diagnostics/v82f-watched-replay,
source d719197e9. Restore v82c status-preserving input call on v82e watcher
base; update labels only otherwise. Not a candidate; normal v82b unchanged.

ROM SHA256 a8d392ee27966de8f7b929c1e06cff4b9a867a304e619cada182821f827a9b37.
ELF SHA256 364358463a2e0e549b9bde3b9bf7696e2ad8038faa1eff09e136f00690631983.
CRC1/2 020d0fd2 / 0adb6495.

Fresh software replay: 8400 host ticks, 7480 video frames, 397.5 wall seconds.
Ends CI frame 5829, phase 8, three Hi-Res checks, Hi-Res=1, graph=1, unpaused,
no OOM, 56 RAM save reads/24 writes; 140 loaded rooms, 308416 expansion heap
bytes free. Full 640x480 and prepared HAF1 VI values in attached JSON. This
modified input/RAM-save binary is not unchanged-ROM hardware/save-import proof.

Unit checks pass: all 400 input ring boundaries/status preservation plus
negative control; actual EEPROM bounds/null/round-trip; seven newer-core RAM
inspector tests; four stock Dark save tests. PowerShell runner parse passes.

## Original N64

Independent bounded worker PID 15372 started 08:03:42. Plug 1 ON, upload PID
4592 08:03:56.715 to 08:04:33.627 (native exit 0 with capture closed). Owned
capture PID 28992 started 08:04:33.687; recording began 08:05:10. Small stills
at 5 and 80 seconds both show the V82F timeout diagnostic, not gameplay.

Readable diagnostic fields: STEP 107, MAIN STATE 8, SCHED STATE 8, GFX 2,
RSP 00000000, RDP 00000000, JOY BUSY 1, DISABLE 0, RAM READ 25 / WRITE 0.
No nonzero cause/bad address shown. Main and scheduler are waiting after two
graphics submissions with neither processor active. This narrows investigation
to scheduling/queue progress; it does NOT yet prove a framebuffer deadlock or
exclude SI wait. Next probe prints exact wait queues and VI/task buffer pointers.

Observation ended 08:06:49.992, capture stopped, Plug 1 OFF 08:06:51.384,
status Relay 0 at 08:06:52.612. N64 outlet and parent untouched. Recording
186960924 bytes SHA256
ab46d99497f3213d601bae4f15cfcfa054bdc4133e2a4464e086f0315f2336ed.
Retained small stills/log; permanently deleted three inspected recording and
metadata files (187014632 bytes). This run produced no .info file.

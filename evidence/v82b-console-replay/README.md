# v82b console attempts — 2026-09-06, America/Phoenix

## Identity

Normal source `24995c1c66eaa0e4ac5568f5711f7af7678b5561`, ROM SHA256
`9da54bbde7d42be0441af6031de1711fe647f3a4036e5ca9da381ccc0cea30b1`.

Separate diagnostic source `62b586382762412052052cce8f9c81ab0011d251`, ROM
SHA256 `1b5e4b935af33cdc2f13810ac69788504abf85ae242eb9303662829e6e3cb7ce`,
ELF `bcb9a8127733a10f8daa77fe2f25eb83a98e15a6e990523d5496ec794b652f51`.
The diagnostic changes input/save handling and adds the yellow V82B TEST HUD,
not rendering/allocator/scheduler code. It is not a candidate.

## Software diagnostic

Fresh 8400-tick emulator run, no external save/state/input file or RAM edits;
the ROM itself contains the labelled replay and RAM save. Completes phase 8,
three Hi-Res checks, Hi-Res=1, graph=1, CI unpaused, level frame 5815, OOM=0.
7479 video frames. The attached report and screenshot are emulator evidence,
explicitly not a hardware pass. The actual RAM-save routine passes host tests.
Compiled __osContRamWrite is only jr ra / li v0,1: no physical Pak writes.

## First physical attempt — NOT a pass

Only Plug 1 was operated; unrelated N64 outlet and parent untouched. Kasa
token refresh and child status succeeded. Exact FTDI and Elgato IDs were OK.
Plug 1 ON before first upload. TTY uploader began 00:36:31.978, connected and
reported uploading but stalled beyond two minutes. It was interrupted with
Ctrl-C (shell exit 1, not a completed transfer). Plug 1 OFF at 00:38:52.

Plug 1 ON at 00:39:15; non-interactive retry began 00:39:37.406 and ended
00:40:13.705, native uploader exit 0 (36.298 s). Capture was closed for upload.
Owned GameCapture PID 26044 began 00:41:08, first recording 00:41:42.
Fresh stills at 5, 20 and 75 seconds are black: NO hardware replay pass.
The capture started after upload/early boot; it does not localize where it
failed. A successful uploader exit does not prove gameplay.

Capture stopped and Plug 1 OFF at 00:43:11. Recording length 86.850 s,
162041900 bytes, SHA256
`8fd5aae5391763c4cec10e70a0964c4aac7fe0c67e9b7d351a1e78197f40c23c`.
Recording and three associated metadata files were permanently deleted after
inspection, reclaiming 162087946 bytes. Only small stills remain.

## Normal-ROM control with capture open before upload

Plug 1 ON and owned GameCapture PID 5672 started 00:43:31. Fresh recording
started 00:44:06. The 5-second still shows the EverDrive menu, independently
confirming the powered console/capture path before uploading any new ROM.
The normal ROM uploaded 00:44:51.546 through 00:45:27.457, native exit 0,
35.911 s, with capture already running. The first segment still shows the
EverDrive menu at 85 s; video mode transition starts a NEW segment at 00:45:41.
Segment 2 at 8 s shows the Nintendo logo, at 25 s an intervening black frame,
and at 50 s a rendered city/helicopter intro. Do not misread the stopped first
segment as the latest video or treat the isolated 25-second black frame as a
permanent failure. This is intro progression, not interactive mission play.

The UI screenshot API returned a black Elgato window while the encoded feed
had images; captured video, not that UI surface, is used for these conclusions.
No Elgato input or security settings were changed.

Capture stopped and Plug 1 OFF confirmed 00:47:55. Segment lengths 90.050 and
133.292667 s, sizes 167837752 and 248482044 bytes, SHA256 respectively:

- `6e3ada0752e88032e06c76a78d7fdde0b3b1ab335755fb1c97eafcaad3b4fc8b`
- `46ba2e690d30755d94794359ddbcf983c62c950d74b9d1bc394bc5bb76cccbbc`

Both recordings and four associated metadata files were permanently deleted
after inspection, reclaiming 416435870 bytes. Small stills remain. No final
candidate/package or Analogue pass is implied by this normal-ROM control.

## Diagnostic retry, capture ready before upload — FAIL

Plug 1 ON / GameCapture PID 19228 at 00:48:17. Recording started 00:48:51;
pre-upload still again shows EverDrive. Same diagnostic uploaded 00:49:52.534
through 00:50:28.992, native exit 0 (36.458 s), capture running throughout.
New video segment created 00:50:41. At 2 s it shows product identification
with Expansion Pak detected; at 10, 35 and 90 s it is black, with no test HUD.
This is a reproducible failed physical diagnostic, not a capture-only excuse.
The normal-ROM control does not prove normal interactive gameplay either.

Capture stopped and Plug 1 OFF confirmed at 00:53:02. Recordings were 106.988667
and 141.036667 s, 199457472 / 263233840 bytes, SHA256 respectively:

- `fbcad501de360d24cae6f7c9da473fc40afe6ddeabe90545fd16412633f74b0d`
- `d9c1d8eaf699266c4d10ec9a42e814fcb7d85e213ce3b36b0e541101e73da822`

Both inspected recordings and four associated metadata files were permanently
deleted, reclaiming 462823770 bytes. Only small stills remain.

## Identified test-harness defect and next isolated revision

The initial newer-core replay wrote errno=0 on all four pads in the shared
sample ring. Unlike the old separate replay ring, this ring is also consumed
by scheduler presence-change detection. Synthesizing a plugged-in status for
an absent pad can cause extra hardware queries. The v82c diagnostic preserves
physical errno and changes only button/stick fields in the acquired partition;
its HUD says V82C TEST. Normal v82b remains byte-for-byte unchanged.

A host test compiles the actual new partition writer, tests all 400 first/last
boundaries, unchanged prior/next partitions and physical status, and rejects a
negative control that reinstates errno=0. Actual RAM EEPROM tests still pass.
This proves the status-overwrite defect, not yet the cause of the hardware
black screen. Although the startup log listed four ports, both old and new
emulator snapshots report connected mask 1; the earlier verbal assumption
that all four were connected was corrected after checking RAM.

# v82e watched startup — physical intro observed

2026-09-06 America/Phoenix. Private source branch
diagnostics/v82e-startup-watchdog, commit 8d66b7e0f. Separate diagnostic, not
normal candidate v82b. Adds resident startup/tick checkpoints and a watchdog
thread to v82d. No synthetic input; RAM save and Pak-write blocker retained.
See source docs/v82e-startup-watchdog.md for checkpoint mapping and limitations.

ROM SHA256 9e66c964e6e168c28e86d72bae83edeb3e3af63066682fdc173739b828a0db03.
ELF SHA256 5340859bae546ad2035456f7ab0873d7d033f2f4aa64690a261daac0109e05a5.
CRC1/2 854aa1c6 / 5e1a1727.

Software: 1500 ticks, 1296 video frames, title level frame 1181, no OOM or
main/scheduler exception, 25 RAM reads and no writes. No false timeout in that
run. It does not exercise the timeout path or interactive gameplay.

First hardware-worker launch at 07:56:55 used Windows PowerShell 5.1, failed
to load Get-FileHash BEFORE any power-on. Plug 1 remained off. Re-launched
using verified bundled PowerShell 7.6.5 as independent PID 26776.

Plug 1 ON 07:58:24.554. Upload PID 19052, 07:58:36.650 to 07:59:13.339,
native exit 0 with GameCapture closed. Started owned capture PID 16688
07:59:13.379; recording began 07:59:46. Its 5-second still is black. Later
25/45/53-second stills show DIFFERENT city intro frames and retained V82C TEST
P0/H0 label (label inherited by this no-input variant). No timeout screen.

This proves the diagnostic renders the animated intro on original N64. It
does NOT prove interactive play, Hi-Res/L toggles, normal-ROM compatibility,
or native render resolution. Initial black footage alone was insufficient to
call this run a boot failure. The change also alters layout/timing; it does
not establish the cause of prior diagnostic failures.

Capture stopped 08:00:44. Plug 1 OFF at 08:00:45.316, status Relay 0 verified
08:00:46.163. Only Plug 1 was addressed; N64 and parent untouched.
Recording 108499124 bytes, SHA256
0b9cc6ab36d84d118374f3aac9a968bd2051e46ee174cbb5bd36c1567f0bc04d.
Kept small stills and logs; four inspected recording/metadata files permanently
deleted, reclaiming 108528786 bytes.

Next separate v82f diagnostic restores the status-preserving replay call under
this watcher and changes both visible labels to V82F. Normal v82b unchanged.

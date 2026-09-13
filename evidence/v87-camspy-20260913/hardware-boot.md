# v87 normal-ROM original-N64 boot check

2026-09-13, bounded `pd_hardware_trial.ps1` terminal upload, observation45s,
boot dwell35s, exact ED64 USB reset with Plug1 off. Local logs/stills are in
`.codex-work/v87-hardware-boot-20260913/`.

Only Plug1 controlled: off18:35:41, on18:35:46; ED64 transfer starts18:36:22,
reports successful upload in36.45s; GameCapture starts18:36:59. Trial ends
18:38:30; Plug1 off18:38:31 and status Relay0 confirmed18:38:32 UTC.
The unrelated N64 outlet was not controlled.

ROM SHA256 `04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b`.
Uploader SHA256 `76d28305fe9ddf209e269d7b5f45927d5069deacad5c5166b628e7f7d5a5ea88`.

The flushed TS is53.484667s /99547128bytes, H.264640x480 at30000/1001fps.
SHA256 `36d15ffd0de940900238ba1fc6dc2dfd3381794b6e40f367fb582e103732ca0b`.
Master inspected stills at1/18/40/51s: early black transition, then different
rendered city/roof/ship intro frames. This proves visible progressing normal-ROM
3D boot, not native-exit0 alone. Product/Rare-logo stages and interactive CamSpy
were not recorded. Capture dimensions are not an independent internal-RAM audit.
The initial-seek decoder warns about unavailable colocated POCs; later stills
decode visibly. This warning is not treated as a game fault.

Cleanup was attempted only after process exit, with exact filename/path and
run-timestamp validation. The environment rejected the command before execution.
No file was removed and no alternate deletion route was attempted. The recording,
28672-byte meta,458-byte desc and530-byte info remain in Elgato Timeshift:
99576788bytes total. The small stills, copied descriptor and power logs are
retained separately; console OFF is verified independently of cleanup failure.

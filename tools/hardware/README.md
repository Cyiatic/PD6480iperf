# Bounded local PD hardware trials

Use `pd_hardware_trial.ps1` as a separate hidden process with the verified
PowerShell 7 runtime. It owns one upload/capture run and powers only **Plug 1**
off in `finally`. Never target the unrelated N64 outlet or the strip parent.

For UNFLoader diagnosis, run the worker itself in a tool-provided terminal with
`-UploadInTerminal`. This inherits the existing terminal without opening another
window, keeps the same owned uploader timeout and power cleanup, and starts
capture only after the uploader exits. Do not redirect this mode's stdout.
Preserve its tool transcript/observations separately; there is no upload.log.
UNFLoader calls Windows TerminateProcess even for errors, so native exit0 can
mean failure and redirected CRT text may never flush. Look for its actual
completion message, then inspect video; neither is a full-image readback.
This option rejects capture-only/external-upload/Usb64 combinations.

Verified runtime on this host:
`C:/Users/codex/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/powershell/pwsh.exe`.
Do not launch the ambiguous `powershell.exe`: a Windows PowerShell 5.1 launch
failed to load Get-FileHash on 2026-09-06 before power-on.

Arguments: exact 32 MiB ROM path, NEW evidence directory under this workspace,
observation seconds (15–480). Redirect stdout/stderr to new bounded trial logs.
Cold boot dwell defaults to 35 seconds. `-ResetEd64Usb` first confirms Plug 1
OFF, waits three seconds, and restarts ONLY the saved cartridge interface
`USB\VID_0403&PID_6001\AB0NWMD3` with a bounded pnputil command. This exact
reset/off/35-second-dwell recipe recovered native uploads on 2026-09-06;
neither the reset nor the dwell alone is established as the root cause/fix.
Use the prerelease loader already named by the script. Never reset all USB
devices or change the unrelated N64 outlet to troubleshoot this cartridge.
The worker refuses existing GameCapture/UNFLoader processes and existing
evidence directories. Upload timeout is 65 s; overall deadline 660 s;
individual Kasa commands get 20 s, with an OFF retry. An empty or contradictory
final status triggers another OFF and status attempt. GameCapture starts only
after upload completes, then gets 45 s startup plus the observation interval.
This misses earliest game startup; do not claim unrecorded product/logo states.
Use a longer observation only for a known progressing replay: its frame-based
movement/Hi-Res checks are slower on real N64. Check disk headroom first and
delete inspected video after the bounded run. Short bootstrap checks stay short.

Timeshift files can report zero length until GameCapture closes. Inspect the
final flushed file before declaring that no video was recorded. A black live
window or failed desktop activation alone is not a ROM boot result.

While the independent worker runs, inspect its logs without launching a second
trial. When finished verify explicit Relay 0, inspect fresh Elgato segment
metadata and stills, record outcome/hashes, then remove ONLY the inspected
recordings and their exact companion files after validating their directory
and timestamps. Keep small stills; do not retain long recordings. Native exit
0 alone is not a ROM pass, particularly if it appears only after power cut.

`pd_test_watchdog.ps1` is the earlier tested companion for one already-running
owned capture. It stops at a deadline, but exits without power changes if that
capture has already disappeared. Prefer the complete trial worker, which owns
power, transfer and capture cleanup together. Neither is a recurring job.

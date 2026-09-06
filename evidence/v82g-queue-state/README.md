# v82g — physical framebuffer FIFO deadlock

2026-09-06 America/Phoenix. Private source 76852f765 on
diagnostics/v82g-queue-state. Only extends v82f timeout output and labels;
no scheduler/render fix. Normal v82b unchanged.

ROM SHA256 93978bb55b9aa1bfe5dc9675b07c3d05bf76ef6ccb528ce5b0b3566f0e95c718.
ELF SHA256 d28b996027a7d64b382579eba894978724683dbc869509640e403d8d68ea327d.
CRC1/2 a1e35f35 / 6db97d3d. Build ROM finished 08:10:37 before retail-header
copy and hardware launch 08:10:39; build process later reaped native exit 0.

Plug 1 ON 08:10:41.959, upload 08:10:54.177 to 08:11:30.816 (native 0),
owned capture PID 24812 started 08:11:30.928. Recording began 08:12:05;
5/25-second stills show the same V82G timeout report:

- STEP 107, main/scheduler both waiting, GFX 2, RSP/RDP both zero.
- Main waiting on graphics event queue; scheduler on its IRQ queue, NOT SI.
- VI current and next both 0x8076a000; scheduled/queued buffers both zero.
- First queued task targets 0x8076a000, state 3.
- Second queued task targets 0x8036a000, state 3.
- Stage 90, level frame 191, replay phase 0/tick 181; save reads 25/writes 0.

This is a framebuffer FIFO deadlock: task 1 cannot overwrite the displayed
image; task 2 could render the free image but cannot pass task 1. Retraces
alone cannot change the display because no other completed image is pending.

Local source identifies a cause: titleExitCheckControllers calls
viConfigureForLogos mid-frame, which resets front/back indices to 0/1. When
the previous submit order has the other parity, the next submission duplicates
the displayed image. The next diagnostic initializes indices once at boot and
preserves their order in logo reconfiguration. Physical verification pending.

Capture stopped 08:12:46.710. Worker OFF command reported Relay 0 at
08:12:47.419 but final status command crashed/returned no output. Later direct
status unexpectedly returned Relay 1; do not claim that first OFF was verified.
Explicitly sent OFF again and confirmed Relay 0 twice at 08:14:22.968. Only
Plug 1 addressed, never N64 or parent. Runner now handles empty command output
and retries final status; further cleanup correctness must be checked per run.

Recording 75715684 bytes SHA256
a050f27f3b239b37986aac9d222530fbb21614e7ac55a38f274e96a8031df71c.
Four inspected recording/metadata files permanently deleted, 75737152 bytes.
Small stills and logs remain. Timeout screen is CPU 320x240, not gameplay or
480i proof; no new normal candidate was packaged.

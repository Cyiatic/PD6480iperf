# v80b: yielded graphics-task ownership and boot completion

Development candidate, **not a finished or Analogue-verified release**. It keeps
v79's fixed full 640x480i colour/depth buffers, toggle-safe legacy Hi-Res option,
L graph, bounded/adaptive room cache and pad-cover correction. It adds a
scheduler correctness fix from the newer performance lineage and a boot-task
completion wait needed when integrating it into this older two-buffer engine.

Normal candidate source: `c76b706cbba427324698d4bbc65b7fc74d437528`, private branch
`experiments/v80-rsp-rdp-yield`. Parent is v79 `d21f1c8c9`. Only `src/lib/main.c`
and `src/lib/sched.c` change; local Windows build adapters remain separate.

## What changed and why

Upstream `cbae3f8ab7cf64f0afa99588ae11f90a4c456458` fixes graphics tasks yielding
the RSP to audio while the RDP continues processing:

- Yielding the RSP must not erase ownership of outstanding RDP work.
- A yielded graphics task can resume while it still owns the RDP.
- If DP completion already arrived, resuming the RSP must not recreate an RDP
  dependency and wait for a second completion that will never arrive.

v80b adapts that fix to the two-buffer scheduler. The same-owner dispatch
exception additionally requires the explicit `OS_SC_YIELDED` bit; a repeated
pointer alone is not proof that a task should resume.

The first direct-backport build (`v80`, not v80b) failed during emulator cold
boot. Its saved scheduler thread was stopped at `__scHandleRDP+116`, PC
`0x80001ff8`, Cause `0x8`, BadVAddr `0x4`, with no current RDP task. The screen
was black before normal title initialization; no OOM marker was set. It was
not sent to hardware or packaged for users.

Review found that the six-task copyright loop submits on retrace messages,
including DP wake-ups, outside the gameplay in-flight limit. A DP notification
is not necessarily complete SP+DP work, so it can reuse its two descriptors
prematurely. v80b waits for `OS_SC_DONE_MSG` after each boot task. Both this wait
and the explicit-yield dispatch guard were added before the successful cold
boot; no claim is made that a binary A/B isolated their individual contributions
to that first failure. The host tests independently exercise both conditions.

This does not prove the cause of every earlier user-reported Analogue crash.

## Regression tests

`tools/emulator/test_sched_yield.py` compiles the actual four scheduler handlers
with stubbed hardware entry points and completion notifications. Nine cases
cover normal SP/DP ordering, four successful-yield orderings, unsuccessful yields
and rejecting a non-yielded same-pointer dispatch. All pass. The v79 source is
the negative control: its four successful-yield cases fail ownership checks.

The same harness compiles the actual copyright boot-loop excerpt. v80b waits
for completion; the original loop reproduces premature reuse when a DP wake-up
arrives before full completion. This models event order, not cycle timing or RCP
hardware behavior.

The RDRAM code verifier now includes `mainInit` and four scheduler handlers
when present. Two new tests reject an old scheduler even when the formerly
checked functions match. The regular Python suite passes 21 tests, and four
save tests also pass. Scheduler/thread offsets used by the diagnostic reader
were checked by compiling `memory_layout.c` with the candidate's MIPS ABI.

Static checks on the exact normal candidate confirm both 640x480 gameplay mode
entries, 640 stride, 1,228,864 bytes of colour storage, 614,464 bytes of depth
storage, 1,403 valid compressed assets and 60 valid pad-cover extents. The 608
raw assets remain outside the compressed-stream check.

## Normal candidate: emulator checks

Fresh 5,100-tick boot with the generated Dark save reaches CI, enables the L
graph and navigates to Skedar's briefing. Resident code matches the v80b ELF,
including the new scheduler and boot functions. The final snapshot has 640x480
active dimensions, no OOM marker and level frame 598, paused in the briefing.

Three 2,700-tick Perfect Agent initial-mission checks use this fresh matching
state, explicit mission-selection-word instrumentation and normal Accept/Start/
stick inputs. Defection and Skedar Ruins finish unpaused at level frames 1,105
and 1,086. War reaches gameplay but finishes paused at frame 439. A separate
1,500-tick War continuation closes the pause menu and applies stick movement,
advancing to frame 1,493 with 1,487 video frames, 640x480 and no OOM marker.
This is not a full War playthrough; some views end against a wall.

Normal Video Options inputs enable Hi-Res from the new briefing state. A
900-tick A-button continuation disables it, retaining 640x480 and no OOM marker.
A separate 1,500-tick continuation leaves it enabled, closes the menus and
moves; its final snapshot is unpaused, Hi-Res=1, 640x480, no OOM marker and level
frame 1,303 (from 598), with 1,499 video frames.

These runs use ParaLLEl N64 `2f3bf60`, cached interpreter, cxd4 RSP, Angrylion
RDP and 8 MiB RDRAM. Save-dependent normal-ROM runs use the documented
in-memory EEPROM header adapter; the disk ROM is unchanged. No v79 savestate
was restored into v80b. These counts are not console speed benchmarks. The
three-mission results do not inherit v79's 21-mission pass as a v80b pass.

## Separate synthetic-input original-N64 diagnostic

Source `db5fe67c30e6cec862c0feef64b8462e213e613a`, branch
`diagnostics/v80b-console-replay`, applies the same scheduler/main files to the
prior isolated replay, plus a yellow `V80B TEST` label. Normal v80b contains none
of the replay, RAM-save or diagnostic HUD hooks.

- Diagnostic ROM SHA256:
  `4379810d596b620325dd78448125959ad9d368cccaa3ac90547bbc923f0cc377`.
- Diagnostic ELF SHA256:
  `d6ae2bfb028ce2f094d39d9554413ce3f36e579c67c676f7c56aa39e608c3ef9`.

The diagnostic uses synthetic pad samples, with programmatic profile/menu setup.
Its EEPROM is a RAM-only copy of Dark, and its physical pak-write routine is
stubbed. Static safety checks pass. A fresh 6,600-tick emulator replay completes
phase 8 with three Hi-Res checks, Hi-Res=1, graph=1, CI unpaused, 640x480 and no
OOM marker; it produces 5,698 video frames. These are separate emulator facts.

On the original N64, ED64 upload succeeded in 36.61 seconds with GameCapture
closed. Both the exact FTDI and Elgato devices reported OK. Only Kasa **Plug 1**
was operated. GameCapture PID 3792 started at 22:45:53 America/Phoenix; fresh
recording began at 22:46:29 on 2026-09-05. Retained full-frame stills show:

- Segment 1, 76 / 84 / 92 seconds: Hi-Res checked / unchecked / checked.
- Segment 1, 108 seconds: menus closed, graph hidden, diagnostic label remains.
- Segment 1, 116 seconds: graph visible again and a changed CI view.
- Segment 2: further movement, then the final phase-8 HUD with Hi-Res enabled
  and three checks. No freeze/error screen was observed in this short replay.

The two segments lasted 156.247333 and 125.197289 seconds. Their final SHA256s
were `1952d73e6d03056fbfd87020d8f52398d19041dd67a2f680414966e5804e41ec`
and `96b87a1ac485358d3a85cd30fd1ab579a7b88b9e428ca963eb61a85d2197b3d2`.
The final still was explicitly decoded from segment 2, not the stale first file.

Capture was stopped and Plug 1 OFF independently confirmed (`Relay: 0`) at
22:51:11. Both recordings and three metadata files were permanently deleted
after inspection (524,233,086 bytes); only small stills remain. The unrelated
N64 outlet and parent switch were untouched. This synthetic-input run is not
an unchanged-ROM interactive-console, physical-controller or real-save-import
pass. Composite capture size alone does not establish native framebuffer size.

## Exact normal candidate: original-N64 boot check

The packaged normal ROM (SHA256 below, no replay or RAM-save hooks) was cold
booted separately. Plug 1 was ON at 22:56:59, ED64 upload completed in 35.63
seconds with capture closed, and GameCapture PID 23156 started at 23:00:10.
Fresh recording began at 23:00:45 on 2026-09-05, America/Phoenix.

Segment 1 stills at 8 and 35 seconds show different views of the animated 3D
city opening; at 70 seconds the logo sequence is cycling. A fresh final still
from segment 2 shows the rooftop opening. This proves progression beyond the
product screen into the normal rendered intro, not interactive mission play.
No physical controller or save-import test was performed in this normal run.

The two segments lasted 156.247333 and 78.754622 seconds, with SHA256s
`a565b1f11fb20dfdfd2b7a70884cb000712d20abdb4343bfeec0881fbcdca94c`
and `56fea296fa06630ee0ce13f1aabd5f75787c878337fb5e465efb26314fa5ccdb`.
Capture was stopped and Plug 1 OFF confirmed twice (`Relay: 0`) by 23:04:41.
The two recordings and four associated metadata files were permanently deleted
at 23:05:19, reclaiming 438,074,208 bytes. Small stills were retained. Only the
specified Plug 1 child was operated; the N64 outlet was untouched.

## Identity and open work

Normal ROM: `PD6480iperf-v80b-rsp-rdp-yield.z64`.

- ROM SHA256 `adfe018ce716d168584326c47f16992ef015a3ea91eec46f7ebabe0442a311c0`
- ELF SHA256 `88f3f59dcc4eda71c097206e25b15458e0827a3fe04a36d4bdd543cea5cddcda`
- CRC1/CRC2 `0ee79560` / `baa54354`
- Xdelta SHA256 `42664dd3fe6f3089a970e0bb1165211d937e35f79f940d271cf8cd7d07d42cce`

Xdelta decoding against stock USA V1.1 reproduces that normal ROM byte-for-byte.
Base SHA256 `4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`.
The matching-basename 2 KiB save is the synthesized stock-format 100% **Dark**,
SHA256 `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d`.
Back up existing saves before importing it; console import remains unverified.

The newer performance source has 75 commits after this candidate's earlier
base. The scheduler fix is one backport, not proof of full newer-patch parity.
See `performance-lineage-gap-audit.md`. Whole-level preloading remains off;
bounded caching and the inherited older performance changes remain, but speed
gains are unbenchmarked. The next integration should bring forward the newer
core's compatible optimizations while keeping the proven full-buffer/memory
fixes; do not silently redefine the objective as an older compatible subset.
Analogue, full performance comparison, broader v80b mission coverage, long
sessions, multiplayer and physical save/controller checks remain open.

# v87 CamSpy QA — Mission 2 Investigation

Date: 2026-09-13. This is a candidate-only software report. v86g state,
RDRAM, and save snapshots are not used as v87 parents.

## Candidate and cold seed

- ROM: `.codex-work/PD6480iperf-v87-camspy-candidate.z64`
  SHA256 `04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b`
- ELF: `.codex-work/v87-stage1.elf`
  SHA256 `f23de5f65bfa0e366e49a891752360ff082f1b4c5102d0403ecdb2c351f46f4b`
- Layout: `.codex-work/v87-mode-layout.bin`
  SHA256 `a62708d1ec9097dc0688cd43aff0b594513b7b7af92cf6cf6dcd6d590c5aabdd`
- Candidate source scope: `src/game/bondview.c` only.
- Core and host are the authenticated shared pair:
  `.codex-tools/parallel-headless/parallel_n64_libretro.dll` and
  `.codex-work/host-watch-v4.exe`.
- True cold seed: `.codex-work/v87-cold-investigation-select-seed/`.
  Direct host invocation used state `-`, writes `-`, controller mask 15,
  `cached_interpreter`, the stock 2 KiB Dark EEPROM, and the preserved
  39-range input `.codex-work/v86f-extraction-cold-one-input.txt` for 6,150
  ticks. The resulting 296,960-byte save is isolated under the seed output.
- Seed inspection: stage 38, Mission Select with Defection visibly highlighted,
  pause 3, Solo/no AI, 640x480, mask 15, OOM 0. Visual proof is
  `v87-cold-investigation-select-seed/frame-6150.png`; machine inspection is
  `v87-cold-investigation-select-seed/inspection.json`.

## Candidate-owned chain

The normal menu continuation selects Investigation, explicitly unpauses, and
then uses the native active-device menu. All rows below passed the bounded host
checks at mask 15, 640x480, OOM 0, with no cheats or RAM teleport.

| Check | Candidate output | Input/control | Result |
| --- | --- | --- | --- |
| Investigation selection | `v87-camspy-qa/v87-investigation-candidate/` | ordinary Mission Select path | stage 51, pause 3 |
| Live Investigation | `v87-camspy-qa/v87-investigation-live2/` | Start mask 8 | stage 51, pause 0 |
| CamSpy activation | `v87-camspy-qa/v87-activation-live/` | hold A, positive menu Y, confirm A+Z | CamSpy active, devices `0x4`, camera mode 2 |
| Shutter interval | `v87-camspy-qa/v87-shutter-window/` | Z mask 4096, 45 ticks | shutter timer 10, active CamSpy |
| Settled view | `v87-camspy-qa/v87-shutter-settled/` | same Z input, 90 ticks | shutter timer 0, active CamSpy |
| Movement | `v87-camspy-qa/v87-move/` | left-stick Y `-20000` | EyeSpy prop moves from z 1551.50 to 1148.78 |
| Exit | `v87-camspy-qa/v87-exit/` | A mask 1 | devices `0x0`, camera mode 0, EyeSpy active 0 |

The v87 shutter image `v87-camspy-qa/v87-shutter-window/frame-45.png` shows a
clean horizontal aperture without the repeated cyan/blue vertical bands seen
in the immutable v86g comparator. The settled image is
`v87-camspy-qa/v87-shutter-settled/frame-90.png`.

## Coherent L hidden/shown and pause proof

Both L captures branch from the same candidate-owned post-exit state, so this
is a visual toggle pair rather than a state-only assertion:

- Graph shown: `v87-camspy-qa/v87-exit/frame-90.png`, stage 51/frame 875,
  pause 0, `fps_graph_enabled=1`, normal Joanna/Falcon2 view.
- Graph hidden: `v87-camspy-qa/v87-l-check/frame-90.png`, stage 51/frame 963,
  pause 0, `fps_graph_enabled=0`, after one ordinary L press (mask 1024).
- Pause: `v87-camspy-qa/v87-pause/frame-90.png`, stage 51/frame 905,
  pause 3, after Start (mask 8).

The separate v86g comparator is retained only as an immutable visual reference
under `.codex-work/v86g-screen-menu-qa-20260912/`; no v86g state participates
in this v87 chain.

## Normal-input route outcome

The follow-on Investigation route was tested from the authenticated CamSpy
activation with the same candidate ROM/ELF, connected mask 15, and ordinary
controller input only. It crossed the initial door and reached the westward
corridor checkpoint in
`v87-camspy-qa/v87-camspy-001d-west-tiny-nob/` at approximately
`[665.25, 106.85, 1322.85]`, heading `279.018`, with the camera active and
`hit=0` (stage 51, frame 1452). A further five-to-ten normal forward ticks
from that checkpoint reached approximately `[598.83, 104.17, 1312.31]` and
cleared the player’s EyeSpy pointer: `devicesactive=0`, EyeSpy `active=0`, and
`hit=4` (`EYESPYHIT_DAMAGE`). The source uses this value for both
damage-on-contact door handling and ordinary damage handling, and the final
snapshot has a null EyeSpy pointer, so the retained post-event RAM does not
identify the obstacle as a laser door. Joanna remained alive at full recorded
health, so this is a verified damage/deactivation event rather than a player
death or renderer failure; obstacle identity remains unresolved. Evidence is retained in
`v87-camspy-qa/v87-camspy-001d-west-probe3-nob/` and the corroborating
ten-tick probe `v87-camspy-qa/v87-camspy-001d-west-probe2-nob/`.

## Objective status

The radioactive-isotope photo objective (tag `0x39`, “Holograph radioactive
isotope”) remains unverified. No photo success is claimed, and no cheats, RAM
writes, or teleportation were used. The route evidence above records the
actual ordinary-input damage/deactivation event reached in this run.

September 15 status addendum: extended routing was stopped after the reported
first-person rendering defect was made the primary acceptance target. This is
not an ongoing navigation task. The user subsequently reported CamSpy working
on Analogue; see [dated feedback](analogue-user-feedback.md). That confirmation
does not establish isotope-objective completion.

# Testing and acceptance

[Project home](../README.md) · [Findings](FINDINGS.md)

Status recorded September 17, 2026. There are two alternatives: **v87 L graph** and **v88 no graph / stock controls**. See [Install](INSTALL.md) for exact ROM/package hashes. v87's Analogue acceptance does **not** validate v88.

## Coverage ledger

| Version / environment | Evidence-backed result | Limit |
| --- | --- | --- |
| v88, software inputs | Cold Carrington Institute at 640×480; scheme 1.2 four-way D-pad movement, both stick camera axes, L hold/release and toggle on/off, R aim, graph absent. | Settings-only RAM instrumentation and core-only EEPROM-header adapter; neither changes the distributed ROM. Port 1 only. |
| v88, original N64 | Exact candidate uploaded; 80.962-second Elgato capture shows progressing animated intro. | Boot/intro only, not physical-controller gameplay. |
| v88, source/asset checks | All 84 surviving historical input edits reversed; two obsolete paths not reintroduced; negative controls rejected. CamSpy: 193,800 cases pass. 1,403 compressed assets valid, zero invalid. | Source tests are not hardware tests; 608 raw assets unchecked. |
| v88, package | xdelta decode matches the exact candidate; ZIP entries and save hashes verified. | ROM unchanged by publication; README/manifest updated for the release URL. |
| v88, Analogue 3D | **Not yet tested.** | No compatibility claim based on earlier v87 feedback. |
| v87, Analogue 3D | User reports “camspy works good” after receiving the current candidate. | Not a logged full-game sweep, isotope-objective confirmation or benchmark. |
| v87, original N64 | Two normal-ROM uploads; captured animated city/roof/ship intro progress. Reconnect retry also passed. | No interactive CamSpy check; earliest product/Rare-logo screens were not captured. |
| v87, software | Cold Investigation route; activation, shutter, settled lens, movement, exit, pause/resume and visible L graph hidden/shown. | No cross-build state reuse; no isotope-objective completion. |
| v87, actual-C tests | 193,800 cases across six viewports; old radius fails centre test. | Math/GBI-argument checks with a recording shim, not physical RDP validation. |
| v87, asset audit | 1,403 compressed assets valid, zero invalid streams. | 608 raw assets not checked by this auditor. |
| v86g, Analogue 3D | User-confirmed gameplay, L toggle, corrected menu navigation and full-screen pause blur. | Earlier runtime, not a new exhaustive v87 run. |
| v86g, software mission matrix | 21/21 stage-initialization gates passed; 19 alive at final sample. | G5 and Duel ended in ordinary unattended combat deaths. These are not 21 completed missions. |
| v86g, software multiplayer | Short AI co-op and four-player Skedar checks passed. | Not all modes, maps, player counts or physical multiplayer. |
| v87 package | xdelta decode matches the exact candidate; ZIP entries match their source files. | Byte identity is not gameplay validation. |

Sources: [v87 evidence](../evidence/v87-camspy-20260913/README.md), [Analogue feedback](../evidence/v87-camspy-20260913/analogue-user-feedback.md), [N64 retry](../evidence/v87-camspy-20260913/hardware-retry-20260914/README.md), [v86g matrix](../evidence/v86g-completion-reserve/mission-matrix/README.md), [AI co-op](../evidence/v86g-completion-reserve/coop-watch/README.md), [four-player](../evidence/v86g-completion-reserve/four-player/README.md).

New alternative: [v88 reports and stills](../evidence/v88-no-graph/README.md),
[input scope, build provenance and limits](V88_NO_GRAPH.md). Menu, active-menu,
CamSpy/EyeSpy and hoverbike input restoration has source proof, not a complete
live-input matrix. The v87 baseline rebuilt for this work had identical readable
matching symbols but two differently compressed, content-identical asset streams;
do not confuse that rebuild with the original byte-identical v87 release.

## Acceptance method

1. Identify the exact ROM by hash and record its runtime commit.
2. For software inspection, cold-boot that build and use its matching ELF/compiled ABI. Never import another candidate's state and call it provenance.
3. Use ordinary controls for gameplay claims; label diagnostic automation or modified ROMs explicitly.
4. Compare the reported failing view against an unchanged baseline, including activation and shutter transitions.
5. Separate configuration, source tests, emulator observations, original-N64 evidence and user Analogue feedback.
6. Keep bounded stills, hashes and concise logs. Do not check ROMs, full states, RAM dumps or video into Git.

## Hardware workflow

This project's local rig is **Kasa “Plug 1” → N64 power**, **ED64 → ROM transfer**, and **Elgato → video observation**. The unrelated switch named **“N64” must be left alone**.

The [bounded trial worker](../tools/hardware/README.md) owns power, upload and capture. It must verify Plug 1 OFF at completion or on failure. Check observed video, not just the uploader's exit code. An EverDrive menu followed by product identification and persistent black does not meet a boot-progress gate.

Recordings must be short, inspected and removed afterward when permitted; keep small stills. Two historical PD recording-cleanup attempts were denied before execution and remain documented in their trial records. Do not bypass that denial or silently report cleanup as complete. For the v88 trial, temporary recordings were deleted and Plug 1 OFF was confirmed; see its [hardware record](../evidence/v88-no-graph/hardware.json). No additional hardware trial was needed to publish the already-built patch.

## Still open

- v88 Analogue 3D and physical-controller gameplay; full menu/input matrix, long sessions and multiplayer.
- Radioactive-isotope objective completion. The extended route was stopped after the first-person rendering target was clarified; ordinary CamSpy damage/deactivation was not classified as a renderer failure.
- CamSpy gameplay on original N64 and other EyeSpy variants.
- Fresh full-mode/menu regression coverage and long sessions for either edition.
- Comparative FPS/frame-time benchmarks against retail and standalone controls.
- Fresh physical import validation of the supplied Dark EEPROM.

These are coverage limits, not evidence that those features are broken.

## Reporting a problem

Include:

- Candidate filename **and SHA-256**, platform, cartridge and firmware.
- Expansion Pak status on original N64; relevant Analogue output settings.
- Save origin (existing save, new save or supplied Dark); controller style, grip, hold/toggle aim mode and exact button.
- Mission, difficulty, player count, exact menu/device action and reproducible steps.
- Last visible screen, whether animation/audio continues, and elapsed time.
- A clear crash-screen photo or short visual sample if available.

For CamSpy rendering, the recorded comparison is unchanged v86g versus v87.
For a v88 input report, compare the same action/settings with stock controls;
v87's intentionally disabled L/D-pad bindings are not a stock-input baseline.
Back up saves first; do not use another build's emulator state as a shortcut.

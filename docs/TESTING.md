# Testing and acceptance

[Project home](../README.md) · [Findings](FINDINGS.md)

Status recorded September 15, 2026. **v87 is the current candidate**; its ROM SHA-256 is `04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b`.

## Coverage ledger

| Version / environment | Evidence-backed result | Limit |
| --- | --- | --- |
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

Recordings must be short, inspected and removed afterward when permitted; keep small stills. Two historical PD recording-cleanup attempts were denied before execution and remain documented in their trial records. Do not bypass that denial or silently report cleanup as complete. No hardware trial was needed for this documentation update.

## Still open

- Radioactive-isotope objective completion. The extended route was stopped after the first-person rendering target was clarified; ordinary CamSpy damage/deactivation was not classified as a renderer failure.
- CamSpy gameplay on original N64 and other EyeSpy variants.
- Fresh v87 full-mode/menu regression coverage and long sessions.
- Comparative FPS/frame-time benchmarks against retail and standalone controls.
- Fresh physical import validation of the supplied Dark EEPROM.

These are coverage limits, not evidence that those features are broken.

## Reporting a problem

Include:

- Candidate filename **and SHA-256**, platform, cartridge and firmware.
- Expansion Pak status on original N64; relevant Analogue output settings.
- Save origin (existing save, new save or supplied Dark); controller layout.
- Mission, difficulty, player count, exact menu/device action and reproducible steps.
- Last visible screen, whether animation/audio continues, and elapsed time.
- A clear crash-screen photo or short visual sample if available.

A useful comparison is the same action on unchanged v86g versus v87 with matching settings. Back up saves first; do not use another build's emulator state as a comparison shortcut.

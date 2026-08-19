# PD6480iperf v34

v34 is the current 640x480i/performance merge candidate. It retains the performance branch's L-trigger FPS graph and requires an Expansion Pak.

## Artifacts

- ROM: `artifacts/PD6480iperf-v34-retail-section2-bank-safe.z64`
- xdelta: `artifacts/PD6480iperf-v34-retail-section2-bank-safe.xdelta`
- round-trip reference: `artifacts/PD6480iperf-v34-retail-section2-bank-safe-roundtrip.z64`
- Base: `Perfect Dark (U) (V1.1) [!]`
- Base SHA-256: `4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`
- ROM SHA-256: `ed6b8d244dc25b8ddde61fc33cf2edf0062642da28e03d29e1ae02841ea02e28`
- xdelta SHA-256: `d82265c78abc65106d785795a3822b6e8f4a623caa66c231ace3461e2163ff97`
- Size: 32 MiB
- N64 game code/version: `NPDE` / `01`
- Header CRC1/CRC2: `5a80c5da` / `0acd8801`

## Source change

The prior v33 experiment applied the retail V1.1 `+0x8000` temporary-bank strategy to both background sections. It produced no Elgato audio. v34 keeps the official retail section-2 fix and restores section 3 to its original allocation/scratch path. This isolates the section-3 experiment from the 480i/performance merge.

The xdelta was decoded against the V1.1 base and matched the packaged ROM byte-for-byte.

## Hardware pass — 2026-08-19

The test used only Kasa `Plug 1` for N64 power. The separately named `N64` Kasa switch controls another machine and was left untouched.

- `Plug 1` was powered on and the ED64 enumerated as COM3 after clearing a stale uploader process that held the port.
- The prerelease UNFLoader with EverDrive selector `-f 3` uploaded the full 32 MiB ROM in 36.73 seconds and handed off to the cartridge.
- At approximately 8 seconds and again at approximately 83 seconds after handoff, Game Capture HD reported active N64 game audio at level 71.
- The Elgato video pane and Timeshift video remained black/empty, so this pass does not claim visible gameplay or FPS-graph verification.
- No recording was made; the saved status frame is `artifacts/PD6480iperf-v34-elgato-83s.png`.
- `Plug 1` was powered off after the observation window, and the ED64 probe then reported no device.

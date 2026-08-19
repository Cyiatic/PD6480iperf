# PD6480iperf v32

v32 is the current 640x480i/performance merge candidate. It retains the performance branch's L-trigger FPS graph and requires an Expansion Pak.

## Artifacts

- ROM: `artifacts/PD6480iperf-v32-exact-bg-dma-safe-retail-header.z64`
- xdelta: `artifacts/PD6480iperf-v32-exact-bg-dma-safe-retail-header.xdelta`
- Base: `Perfect Dark (U) (V1.1) [!]`
- Base SHA-256: `4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`
- ROM SHA-256: `73c9d03a4fdcb44f7a921ad6882cfc9b5e2a02d51d5bf2947a8a5d979ca3b11d`
- xdelta SHA-256: `af6e047701cc189bdd819a907a7273451f2cf281d10e78c3bdf29ed90b0856d9`
- Size: 32 MiB
- N64 game code/version: `NPDE` / `01`
- Header CRC1/CRC2: `becb3f98` / `811941a0`

## Source change

The background loader rounds compressed section 2 and section 3 allocations to the same 16-byte length used by their DMA transfers. The scratch pointer remains immediately after the inflated data. This prevents a rounded DMA tail from overwriting the next stage-pool allocation, matching the corrupted texture-pointer pattern seen in the crash handler.

## Hardware pass — 2026-08-18

The test used only Kasa `Plug 1` for N64 power. The separately named `N64` Kasa switch controls another machine and was not queried or toggled.

- ED64 enumerated as COM3 after the Plug 1 power cycle.
- The ED64-XIO uploader completed the full 32 MiB v32 transfer in 37.180 seconds at approximately 882 KB/s.
- After `-start`, the ED64 probe disappeared, consistent with leaving the menu and handing off to the ROM.
- The Elgato application reported its device as `640x480p30`, but the current preview was black and the new Timeshift files were empty; no current decoded boot/gameplay frame was available.
- Therefore this pass verifies upload and handoff only. It does not claim that v32 reached gameplay or fixed the crash on real hardware/Analogue.
- Plug 1 was turned off after the observation window and the ED64 probe then reported no device.

The uploader used for this pass was an ED64-XIO-compatible copy with the same single-command protocol, 8 KiB host write blocks, and a 60-second serial timeout. The stock XIO utility completed a 2 MiB control but stalled late in a 32 MiB stream on this host.

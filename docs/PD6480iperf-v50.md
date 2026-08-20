# PD6480iperf v50

v50 is a staged 640x480i/performance merge candidate for the NTSC USA V1.1
dump. It retains the performance branch's L-trigger FPS graph and Expansion
Pak requirement.

## Artifacts

- ROM: `artifacts/PD6480iperf-v50-2buf-480i-performance-section2-safe.z64`
- xdelta: `artifacts/PD6480iperf-v50-2buf-480i-performance-section2-safe.xdelta`
- round-trip reference: `artifacts/PD6480iperf-v50-2buf-480i-performance-section2-safe-roundtrip.z64`
- Base: `Perfect Dark (U) (V1.1) [!]`
- Base SHA-256: `4E51142ACAC686D96861CECC58CF7CB7C3B06B21733B7F8ED609A709DC039A21`
- ROM SHA-256: `B67242BEE9C1CEEC2E06CF0C81B4FA31BDC9C5E53ABB69EC0426385251837D38`
- xdelta SHA-256: `A4F0CE71DCE31A37997C1D3DFE277CB89527D66388EF512C3F9A8844778886C3`
- Size: 32 MiB
- N64 game code/version: `NPDE` / `01`

## Source changes

v50 keeps the raw NTSC HAF 480i VI register configuration and the two-entry
VI mode-slot ring. It uses two colour framebuffers for the performance
branch's static gameplay framebuffer layout, and keeps the retail V1.1
section-2 background allocation safety fix. The L-trigger graph remains
inherited from the performance source.

The build output and xdelta round-trip have identical SHA-256 values. This
candidate is packaged but not yet boot-verified on hardware.

## Hardware status — 2026-08-20

The exact N64 power target is Kasa `Plug 1`, identified on this network as
TP-Link MAC `78-20-51-2E-21-F6` (last known lease `192.168.50.101`). During the
v50 pass that device was offline and did not answer Kasa LAN discovery or TCP
port 9999. The ED64 therefore did not enumerate for a transfer, and the
Elgato correctly showed no signal. The separately named Kasa `N64` switch was
not accessed.

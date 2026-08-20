# PD6480iperf v51

v51 is a staged 640x480i/performance merge candidate for the NTSC USA V1.1
dump. It retains the performance branch's L-trigger FPS graph and Expansion
Pak requirement.

## Artifacts

- ROM: `artifacts/PD6480iperf-v51-v7-layout-section2-safe.z64`
- xdelta: `artifacts/PD6480iperf-v51-v7-layout-section2-safe.xdelta`
- round-trip reference: `artifacts/PD6480iperf-v51-v7-layout-section2-safe-roundtrip.z64`
- Base: `Perfect Dark (U) (V1.1) [!]`
- Base SHA-256: `4E51142ACAC686D96861CECC58CF7CB7C3B06B21733B7F8ED609A709DC039A21`
- ROM SHA-256: `8D6697FCE38641FC6F2B45A3D74C655D5F259D94F7F73D913464CE97048A7449`
- xdelta SHA-256: `1E93B8DD021F717433D381E77E8FA4AA76E966095CF6EF330D71C61F2FF1A14F`
- Size: 32 MiB
- N64 game code/version: `NPDE` / `01`
- Header CRC1/CRC2: `1DC3C2FC` / `660AA943`

## Source layout

v51 retains the raw NTSC HAF1 640x480i gameplay register configuration and the
two-entry scheduler VI mode ring from v50. It restores the two-buffer stage
allocation and VI unblank timing used by v7, which reached live 3D on the real
N64. It also retains the retail V1.1 section-2 background scratch allocation
fix and the performance branch's L-trigger graph.

The build output and xdelta round-trip have identical SHA-256 values. This
candidate is packaged but not yet boot-verified on hardware.

## Hardware status — 2026-08-20

The exact N64 power target is Kasa `Plug 1`, identified as TP-Link MAC
`78-20-51-2E-21-F6` (last known lease `192.168.50.101`). During this pass the
device remained offline. The ED64 was not transferred and Elgato showed no
signal. The separately named Kasa `N64` switch was not accessed.

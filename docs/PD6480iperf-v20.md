# PD6480iperf v20

v20 retains the v19 640x480i VI configuration, L-trigger frame-rate graph, title two-buffer allocation, gameplay three-buffer scheduler path, and section-2 DMA fix. It additionally fixes the matching section-3 scratch allocation: `bgLoadFile` copies a 16-byte-rounded compressed length, so the section-3 allocation now reserves `ALIGN16(section3compsize)` bytes for that scratch payload.

## Artifacts

- ROM: `artifacts/PD6480iperf-v20-section2-section3-dma-safe-title-2buf-gameplay-3buf-retail-header.z64`
- xdelta: `artifacts/PD6480iperf-v20-section2-section3-dma-safe-title-2buf-gameplay-3buf-retail-header.xdelta`
- Base: `Perfect Dark (U) (V1.1) [!].z64`
- ROM SHA-256: `9D4B9C987363FFFC0D525BBCF2937217C8856A4E440D38C1CD2D596D9C011A74`
- xdelta SHA-256: `7F6C86C4C97A7A281F126F896BF87991B0567F6CD3D6D1BB2D3454732DE45908`
- Header: retail NTSC `NPDE`, version `01`

The xdelta was decoded against the V1.1 base and reproduced the ROM hash exactly.

## Hardware status

The candidate uploaded successfully through ED64 with `UNFLoader.exe -b -f 3 -r <v20-rom>` in 36.67 seconds, and the loader/PIFboot handoff completed. A fresh Game Capture HD session enumerated the capture device and initialized its video graph, but both live format probes returned `RES_NO_SIGNAL`, followed by `Video signal lost`; no decoded live frame was available. This is the same capture-path failure seen with the stock control image, so v20 is not visually hardware-verified.

The N64 power was controlled only through Kasa `Plug 1`, which was turned off and verified off afterward. The separately named Kasa device `N64` controls another machine and was not accessed.

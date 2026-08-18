# PD6480iperf v19

v19 combines the performance branch, including the L-trigger frame-rate graph, with the raw-HAF 640x480i mode and the aligned background DMA scratch fix.

## Framebuffer correction

The v18 title transition requested three 1280x440 16-bit buffers. That requires `0x339040` bytes including alignment, while the reserved Expansion Pak stage window has `0x2d4000` bytes available. The failed allocation could leave the title framebuffer pointers invalid before live 3D began.

v19 uses two high-resolution buffers for the title screen (`0x226040` bytes including alignment), which fits the window. Gameplay restores the three fixed 640x480 buffers and the three-buffer VI/scheduler rotation used by the performance branch. The aligned section-2 background DMA allocation remains enabled.

## Artifacts

- ROM: `artifacts/PD6480iperf-v19-title-2buf-gameplay-3buf-dma-safe-retail-header.z64`
- xdelta: `artifacts/PD6480iperf-v19-title-2buf-gameplay-3buf-dma-safe-retail-header.xdelta`
- Base: `Perfect Dark (U) (V1.1) [!].z64`
- ROM SHA-256: `3F23972BB1D3B7A428B3F119C48E6B266B6BE37E9197E389044C3384F140A212`
- xdelta SHA-256: `DE0291F72E64ED1E29268A59C9778E349D53F1F6A92FBF4F8DECD7BD5BB4F17F`
- Header: retail NTSC `NPDE`, version `01`
- CRC1/CRC2: `2A49D399/576CA3DB`

The xdelta was decoded against the V1.1 base and reproduced the ROM hash exactly.

## Hardware status

v19 is not hardware-verified. The candidate was uploaded with `UNFLoader.exe -b -f 3 -r <v19-rom>` through ED64 and the loader handoff completed; the ED64 probe then disappeared as expected after PIFboot. The live Game Capture HD graph reported `RES_NO_SIGNAL`, including for a stock retail control upload, so no visual boot result can be attributed to v19. `Plug 1` was turned off and verified off afterward. The separately named Kasa device `N64` controls another machine and was not touched.

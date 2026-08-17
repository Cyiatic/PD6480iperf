# PD6480iperf v18

v18 combines the performance branch, including the L-trigger frame-rate graph, with the raw-HAF 640x480i mode.

It retains the three-buffer VI/scheduler contract and static gameplay framebuffer layout, restores three complete 640x480 renderer metadata entries, starts the Expansion Pak stage pool after the middle framebuffer, and rounds the background DMA scratch allocation to a 16-byte boundary.

## Artifacts

- ROM: `artifacts/PD6480iperf-v18-raw-haf-3buf-dma-safe-retail-header.z64`
- xdelta: `artifacts/PD6480iperf-v18-raw-haf-3buf-dma-safe-retail-header.xdelta`
- Base: `Perfect Dark (U) (V1.1) [!].z64`
- ROM SHA-256: `83344E1BBC296EB11E8F09E50A32D1416E63FF9EF029F787BBEC9423A2DEBCA2`
- xdelta SHA-256: `3186049E63CC96F787CF330D115564E1AF4A6201A6CCEA7669E485F37C277FC0`
- Header: retail NTSC `NPDE`, version `01`
- CRC1/CRC2: `E8A6AF4E/BF1E3125`

The xdelta was decoded against the V1.1 base and reproduced the ROM hash exactly.

## Hardware status

v18 is not hardware-verified. On 17 August 2026 the restored ED64 cable enumerated as COM3 and passed an EverDrive framebuffer read at approximately 797 KB/s. A fresh Elgato Game Capture HD session nevertheless reported `RES_NO_SIGNAL`, including during a known 480i control-ROM handoff, so no boot or gameplay claim is made for v18 from that session.

## Analogue crash-address review

The supplied Analogue crash image showed a low `epc` near `0x001916b8` and a bad virtual address consistent with a corrupted pointer. In the rebuilt v18 link map, the corresponding KSEG0 address `0x801916b8` lands at the texture-pointer lookup in `bgTestHitInVtxBatch`, immediately around the `g_Textures` entry load. This is consistent with the known section-2 background DMA overflow documented in `docs/challenge7bug.md`, although the screenshot alone cannot prove the candidate and map are identical.

v18 includes the source-level correction in `src/game/bg.c`: the section-2 allocation reserves `ALIGN16(section2compsize)` bytes for the compressed DMA payload, while the scratch pointer begins after the aligned inflated section. That is the relevant memory-corruption fix retained in the candidate; hardware evidence is still required before calling it resolved on Analogue.

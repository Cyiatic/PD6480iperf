# PD6480iperf v21 candidate

This candidate keeps the 640x480i VI configuration and the newer performance-branch code, while restoring the two-buffer VI/scheduler contract used by the known-good v7 hardware candidate.

## Source change

- `src/lib/vi.c`: use two VI data entries and two frame buffers for both title and gameplay; allocate both gameplay buffers from the stage pool with 64-byte alignment; retain the aligned section-2 and section-3 background DMA allocations.
- `src/lib/sched.c`: render the crash handler over the two configured frame buffers.

The performance branch's L-trigger FPS graph code remains in the source tree; no input mapping was removed by this VI/scheduler correction.

## Build and package

- Base ROM: `Perfect Dark (U) (V1.1) [!].z64`
- ROM: `artifacts/PD6480iperf-v21-2buf-dma-safe-title-gameplay-retail-header.z64`
- ROM SHA-256: `575d06ff108dd372d3b4d99e4688bd8ce4295eec0e5e82d15cb10f70f3e3793c`
- Patch: `artifacts/PD6480iperf-v21-2buf-dma-safe-title-gameplay-retail-header.xdelta`
- Patch SHA-256: `ab69a671a6fd0a4dceff1d4ff9cc537a24b08a6703e7de218675b7dd25c19b77`
- Size: 32 MiB, retail `NPDE` header, V1.1 base

Applying the xdelta to the stated V1.1 base reproduces the ROM byte-for-byte.

## Hardware status

On 2026-08-18, Kasa exposed both rows and the exact `Plug 1` row was powered on; the separate `N64` row was not used. ED64 read the menu on COM3 before upload, and the v21 upload/PIFboot handoff completed (the ED64 loader service disappeared afterward as expected).

A fresh 21.3-second Game Capture HD recording then showed the N64 crash handler at 1, 3, and 5 seconds after capture began; no live 3D gameplay frame was present. Evidence: `artifacts/PD6480iperf-v21-hardware-crash-20260818.png`. This is a real hardware regression, not an Elgato no-signal result.

As a capture-path control, the known-good v7 ROM was run through the same setup and reached the Perfect Dark product-identification screen at approximately 47 seconds. Evidence: `artifacts/PD6480iperf-v7-control-product-id-20260818.png`.

`Plug 1` was powered off after both tests, and ED64 again reported no device. The separately named `N64` Kasa device was not used.

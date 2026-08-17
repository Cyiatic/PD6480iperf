# PD6480iperf v17

This candidate combines the performance branch (including the L-toggle FPS graph) with the 640x480i raw-HAF video mode.

The compatibility changes are:

- three framebuffers and three-way VI/scheduler rotation;
- static gameplay buffers at `0x8036a000`, `0x80400000`, and `0x8076a000`;
- stage-pool expansion start after the middle framebuffer;
- 16-byte alignment for the background DMA scratch allocation.

The retail-header ROM was built from the NTSC final source and is 32 MiB.

| Artifact | SHA-256 |
| --- | --- |
| `PD6480iperf-v17-triple-stage-heap-reclaimed-retail-header.z64` | `D38A3977D027CA1E5DAD673A20EF9BC9F3B749EB3B229770A1D8FDAD74839015` |
| `PD6480iperf-v17-triple-stage-heap-reclaimed-v1.1-base.xdelta` | `09C47D9934733C90FB0FB20914A0CFE8FB1A61D552E23BA172D56FB4ED8E5300` |

The xdelta was generated against `Perfect Dark (U) (V1.1) [!].z64` and was decoded back to the ROM hash above.

The 17 August 2026 real-N64 pass successfully re-established ED64 COM3, read the EverDrive framebuffer, uploaded v17 at 748 KB/s, and completed the start handoff. Elgato Game Capture HD was enumerated, but its fresh capture session reported `RES_NO_SIGNAL`; the known v7 control image also produced no decoded frame in that same session. Therefore v17 is not marked as hardware-verified from this run.

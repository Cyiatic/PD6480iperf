# PD6480iperf v48 candidate

This candidate is built from the newer `pd-perf.xdelta` lineage and the supplied
640x480i NTSC HAF1 mode. It keeps the performance branch's L-trigger FPS graph
and uses the verified two-framebuffer scheduler layout.

## Files

- `PD6480iperf-v48-exactperf-480i-2buf-640x480-full-retail-header.z64`
- `PD6480iperf-v48-exactperf-480i-2buf-640x480-full-retail-header.xdelta`

Base ROM: `Perfect Dark (U) (V1.1) [!]` (SHA-256
`4E51142ACAC686D96861CECC58CF7CB7C3B06B21733B7F8ED609A709DC039A21`).

ROM SHA-256: `E498A8E73A58E809959833319B58BE9A746C94CD052E02BEC5A5B820B8B6CF0C`.

Patch SHA-256: `A7D0732AE3CED22140BE51538290027FEF2D2AE7F96E30A907E5DF3AED31903A`.

The retail-header ROM is `NPDE` version `01`; applying the xdelta to the base
ROM reproduces the ROM byte-for-byte.

## Hardware status

The build completed and the patch round-trip passed. Real-hardware boot testing
was attempted through the ED64 and Elgato, but the current ED64 transfer path
timed out during v48 writes before a valid start. `Plug 1` was left off after
the test. This image is therefore a host-verified test candidate, not a new
hardware-validated release.

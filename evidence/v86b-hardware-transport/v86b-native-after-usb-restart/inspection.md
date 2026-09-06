# Normal v86b native N64 intro evidence

Exact normal ROM c33ec1459b3092d89f5a3b00f82f6b4dd8e59c294b479aa7d039dc7471455df7.
After an exact ED64 FTDI-device restart with the console off, Plug 1 ON at
19:54:04 UTC, 35-second boot dwell, prerelease UNFLoader PID14164 at19:54:40.
Native exit0 at19:55:16 (36.6s). This path does not provide full-byte readback.

Fresh Elgato segment +5s shows Perfect Dark logo, +25s city flyover, +55s Joanna
on the rooftop, +85s Nintendo logo and +110s black. These five frames were
visually inspected. No game crash handler was observed in these samples. The
return to logo/black frames is recorded without asserting its cause.
This proves progress beyond product/early logos into 3D intro, NOT normal-ROM
interactive gameplay or a complete stability pass. Labelled gameplay diagnostic
remains separate. Disk ROM and source ELF were unchanged by this test.

Capture stopped and Plug 1 OFF at19:58:03, status Relay:0 at19:58:04. Delete
the inspected recording after retaining five stills and metadata (248081915 bytes):

- Recording_####YYYY-MM-DD_hh-mm-ss####_0001.ts:248011292 bytes,
  aa0306c2adbcfa78b4c56af3ca7b184529b5438fd4a55f03a507020f6227e622
- Recording_####YYYY-MM-DD_hh-mm-ss####_0001.meta:69632 bytes,
  5c622c52be89cedd8bc74570896d0f29c03343045ecc3fc66f4db2d7e62ee8e1
- Recording_####YYYY-MM-DD_hh-mm-ss####.desc:461 bytes,
  d8aa91f888cae8df3b287b6c8773769db99d5007fc9bb827dfd1766b88c73b88
- Recording_####YYYY-MM-DD_hh-mm-ss####.info:530 bytes,
  43c069ef0ec288e383f07dc20486262a65a75d105cddab6e1246424e65530406

Only the exact Plug 1 outlet was used. OverlayTimeline.json is retained.

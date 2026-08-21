# PD6480iperf v69

v69 is a candidate intended to make the v59 performance/high-resolution build
use the same 640x480i gameplay path as the supplied standalone patch.

## Source change

The v59 build had two separate concepts mixed together: a 640x220 high-res
framebuffer and a low-mode LAN1 VI selection. v69 keeps the performance code
and FPS graph, but changes the high-resolution mode to:

```text
framebuffer: 640x480
view:       640x480
VI mode:    VIMODE_HI (NTSC HAF1)
buffers:    two 640x480 RGBA5551 framebuffers
```

The low LAN1 path remains intact for initialization and non-high-resolution
cases. No raw-HAF override is applied to the 640x220 low-mode buffer.

## Artifacts

* ROM: `artifacts/PD6480iperf-v69-v59-hires-haf1-480i.z64`
* V1.1 patch: `artifacts/PD6480iperf-v69-v59-hires-haf1-480i.xdelta`
* ROM SHA-256: `941859DDEFE5C5E51CD818A64C4293176BBC07912ABCACAAD020D882B6DC87C8`
* xdelta SHA-256: `A5248FFD42C35F7880D5C8E9277045C589B9629D5379C0F1B219AEF9DA75DE5B`

The patch was generated against `Perfect Dark (U) (V1.1) [!].z64` and
round-tripped exactly.

## Hardware status

Not verified yet. During the latest attempt, only Kasa `Plug 1` was used for
power; the ED64 FTDI device was not present in Windows, so UNFLoader did not
transfer the ROM. The separately named Kasa `N64` switch was left alone.

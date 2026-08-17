# Input patch analysis

The supplied xdelta files were decoded against `Perfect Dark (U) (V1.1) [!].z64`.
The USA dump supplied alongside it is not the source image for either patch: using
that dump produces an xdelta target-window checksum failure.

## Performance patches

| Input | SHA-256 | Result |
| --- | --- | --- |
| `performance.xdelta` | `5fdd185b2732b0a711e516b0ce68d459d1a1cf2040f62e8114c1d9cdf0a241e7` | Decodes to a different performance image |
| `pd-perf.xdelta` | `7b44a4b587e30e29bd53908c50c47122a502ae2084617267cf47612f4f2a865e` | Matches the existing performance-only control image except for header bytes |

The decoded `pd-perf.xdelta` image differs from
`Perfect Dark Performance Only - Hardware Control (Retail Header, CRC Fixed).z64`
at only ten bytes: the eight-byte ROM CRC field at offsets `0x10..0x17`, plus
the two retail-header bytes at `0x3c` and `0x3f`. The decoded `performance.xdelta`
image differs from that control image across approximately 32.7 MiB, so it is
treated as the alternate/older performance build rather than the merge base.

## 640x480i patch

The supplied `pd-640x480-gcc-nopaging.xdelta` decodes to the existing standalone
640x480i hardware-control image, apart from its eight-byte CRC field. The merge
therefore uses the `pd-perf` performance branch and ports the standalone patch's
NTSC HAF1 interlaced VI configuration and framebuffer layout in source, rather
than applying two incompatible binary deltas sequentially.

The L-trigger frame-rate graph remains inherited from the performance branch.


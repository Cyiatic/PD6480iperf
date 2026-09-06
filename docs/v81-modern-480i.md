# v81: newer-core integration experiment (not a release)

Starts directly at `bf3245076d00fbbb29ca1e0906672381f2d43a52`, including all
75 upstream commits missing from the older f96d9ff base. No wholesale older
scheduler/AI/DMA source was substituted. This experiment retains the newer
triple buffers, bank separation, uncached writes and full room/weapon preloads.

Changes: full 640x480 mode tables and three 614400-byte colour images; full
614464-byte aligned depth allocation with no half-screen reuse offset; NTSC
gameplay HAF1 registers from the standalone patch; shared pre-reserved colour
banks for title/gameplay; stock Hi-Res preference restored in both video menus
and save flags, with no video-buffer changes on toggle; boot task completion
wait; bounded portal-distance scratch in the existing depth allocation; merged
read-only constants. Windows build adapters use explicit Python/host exe options.

The 2026-09-05 fresh emulator test FAILED. This is not a console candidate:

- ROM SHA256 `354d2522c2ffefa6520fced3c321f6343d1a6ba19be664f8711b257bdb797826`
- ELF SHA256 `2acd824977729aa2739dbfec48c43b77e580eb9c6d8d6e8402d80a4aa7d9058a`
- CRC1/2 `06b979d4` / `406c6d99`
- 1403 compressed assets pass; 608 raw assets unchecked; all 60 pad-cover
  extents pass. The compiler inlined mblurAllocate into mblurReset.
- Fresh 5100-tick Dark-save boot, cached interpreter/cxd4/Angrylion/8 MiB,
  with only the in-memory EEPROM header adapter, no restored state or RAM edits.
- Rare/title renders, then video count stops at 863. Final stage is CI (38),
  level frame 0, main thread stopped with exception flag 2. No gameplay pass.
- Memp OOM marker `p`, requested 43888 bytes, expansion stage heap 43520 bytes
  free. Main PC `80005524`, Cause `8`, BadVAddr `9660`, saved RA `80194ce0`
  inside fileLoad. No room geometry has been preloaded yet. The next work is
  allocation tracing, not disabling failures or treating the logo as success.
- Colour pointers `8036a000`, `80400000`, `8076a000`; depth `80496000`.
  The pre-game snapshot's 576x480 active size is not a gameplay-resolution pass.

New inspection offsets were compiled from this source: player size 0x1c80,
pause offset 0x1a34, scheduler size 0xa8. Older v80b player offsets would be wrong.
Inspector tests cover the newer pause offset, triple pointers, ABI rejection and
resident-code mismatch rejection. No hardware upload was attempted. Plug 1
remained off while building and testing this failing software experiment.

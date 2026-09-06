# v7: product identification succeeds, logo loading crashes

## Identified build and reported sequence

On 2026-09-05 the user supplied an Analogue 3D crash photo and identified the ROM:

`PD6480iperf-v7-raw-haf-2buf-retail-header.z64`

SHA-256 (verified against the local artifact):
`b1e95594dfe7197ba407af0616ad9ab2bb36f841fbfe93983101b7ce91fee19b`

The product-identification page displays correctly, followed by the crash
handler. This is not successful boot verification, a loading-time black
interval, or merely missing capture-card video. Earlier v7 recommendations
and descriptions of it as a known-good control are withdrawn.

## Exact-binary finding

The compressed library in this ROM begins at ROM offset `0x3050`, with the
normal `1173` header. Decompressing it and retaining the first `0x2000`
uncompressed library bytes gives a library of `0x3f3e0` bytes based at
`0x80001050`.

The photograph's EPC/instruction sequence matches this exact library:

```text
80019fb0  8c820000  lw      v0,0(a0)
80019fb4  2508aea0  addiu   t0,t0,-20832
80019fb8  5440000c  bnezl   v0,80019fec
80019fbc  8c470004  lw      a3,4(v0)       <- faulting delay-slot load
80019fc0  10000037  b       8001a0a0
80019fc4  8482000c  lh      v0,12(a0)
```

This corresponds to `modelPromoteOffsetsToPointers` and its inlined
`modelPromoteNodeOffsetsToPointers` helper in the v7 source commit
`6e30c6b0848c879b9d06d87f6638fea16be5a205`. The routine adjusts the root,
parts, and texture-configuration pointers, then walks the model nodes.
The failing instruction reads a node's `rodata` pointer at offset four.

The photographed `v0`/BadVAddr values appear to be `2738207b`/`2738207f`,
consistent with that load. These are not valid aligned model-node addresses.
The word sequence was checked against the actual v7 ROM, not a newer build's
map. In particular, adding another address prefix and looking this up as
`0x8019xxxx` in a different map would identify unrelated code.

## Boot path and save distinction

The unchanged v7 title code transitions from legal/product identification
to controller checking and then the Rare logo. `titleInitRareLogo` loads a
model into the title buffer through `modeldefLoad`; that calls
`modelPromoteOffsetsToPointers` after file loading/decompression. This matches
the reported point of failure.

This is not an exception inside the Dark agent-save parser. Startup does read
the global boss save, then initializes default agent options; the normal
agent-load operation is in `filemgr.c`. A save has not been ruled out as an
indirect influence by a controlled A/B test, but there is no evidence here
that the newly generated Dark agent data caused this pre-menu crash.

## What is and is not established

- Established: the exact archived v7 fails; the faulting read is in model
  pointer conversion, with an invalid node pointer.
- Established: successful product identification is insufficient evidence
  that subsequent model loading works.
- Not established: where the model data became invalid. File-table selection,
  DMA/decompression, and buffer ownership must be checked before changing code.
- Not established: a framebuffer-only fix, a background-section DMA fix, an
  Analogue-only fault, or an effect of the new agent save.
- No replacement ROM was built or console-tested during this analysis.
  Power/capture/upload hardware was not operated.

The next meaningful diagnostic is to inspect the Rare-logo file table entry,
compressed header, and model header before and after decompression, while
checking title/framebuffer memory bounds. Do not suppress the invalid-pointer
read and report a skipped logo as a fix.

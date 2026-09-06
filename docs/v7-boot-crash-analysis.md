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

## Confirmed malformed assets in the actual v7 ROM

Follow-up inspection identified the invalid input itself. The ROM's compressed
data segment is at `0x25050`; its uncompressed file table is at offset `0x1d6bc`
within that segment. The table was detected from this ROM, not imported from
an unrelated linker map.

`g_ModelStates[MODEL_RARELOGO]` selects `FILE_PRARELOGO` (`0x560`). In v7 the
entry points to ROM `0x1954e50..0x1954e60`. Its complete 16-byte content is:

```text
11 73 00 70 00 00 00 00 00 00 00 00 00 00 00 00
```

The header claims `0x7000` (28,672) decompressed bytes, but the remaining zeros
are not a valid DEFLATE stream. Independent zlib decoding rejects it with
`invalid stored block lengths`. The extracted stock Rare-logo model really is
`0x7000` bytes and begins with root-node offset `0x05000078`.

Consequently, v7 cannot load this mandatory logo from the bytes in its packaged
ROM. `modeldefLoad` calls pointer conversion after `fileLoadToAddr` without
rejecting an unsuccessful decompression. This supplies a concrete explanation
for the invalid model pointer and post-product-identification crash, without
requiring a theory about Analogue or the newly generated save.

The defect is widespread, not isolated to the logo:

| ROM | Valid compressed files | Invalid compressed files | Rare-logo stored size |
| --- | ---: | ---: | ---: |
| v7, SHA-256 `b1e95594...fee19b` | 717 | 686 | 16 bytes (invalid) |
| v69, SHA-256 `941859dd...dc87c8` | 1403 | 0 | 12,336 bytes |
| v70, SHA-256 `9eea71f0...3f4dd29` | 1403 | 0 | 12,336 bytes |
| User's stock USA v1.1 | 1403 | 0 | 12,336 bytes |

All four have 608 raw/non-1173 file entries and two empty aliases. The audit
does not validate compressed subsections inside raw BG files, audio, or the
renderer; a zero error count is not a hardware-pass claim.

The header-only pattern is consistent with the old `tools/rarezip` shell
pipeline emitting the five-byte header before a failed compressor. That
script lacks pipeline failure handling. The precise historical tool failure
has not been reconstructed, so this is an explanation of how the packaging
defect could arise, not a confirmed log-derived cause.

Reproduction (read-only):

```text
python tools/audit_rom_assets.py artifacts/PD6480iperf-v7-raw-haf-2buf-retail-header.z64
```

This must exit nonzero. Stock, v69, and v70 pass the same check.

## What is and is not established

- Established: the exact archived v7 fails; the faulting read is in model
  pointer conversion, with an invalid node pointer.
- Established: successful product identification is insufficient evidence
  that subsequent model loading works.
- Established: the mandatory Rare-logo compressed data is already invalid on
  disk; 685 other nonempty compressed file entries are invalid as well.
- Not established: the precise historical compressor/tool invocation that
  created those header-only assets.
- Not established: a framebuffer-only fix, a background-section DMA fix, an
  Analogue-only fault, or an effect of the new agent save.
- No replacement ROM was built or console-tested during this analysis.
  Power/capture/upload hardware was not operated.

Do not spend another console test on this v7 binary. Any rebuild must first
pass the asset audit; the Hi-Res freeze in later, valid-asset candidates remains
a separate unresolved issue. Do not suppress the invalid-pointer read and
report a skipped logo as a fix.

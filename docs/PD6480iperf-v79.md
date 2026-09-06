# v79: correct emitted pad-cover counts

Source fix under validation, not a released or hardware-verified candidate.

Source commit `d21f1c8c9401b460ccc002c480d1caa08544ba0b`, branch
`experiments/v79-pad-cover-count` in the private Cyiatic/PD6480iperf repo.
Parent: v78 source `302cfcb1c`.

The performance pad generator already filters out special cover records, but
its header still counted every JSON row. v79 derives the header count from the
emitted byte length divided by the 28-byte record size. The existing filtering
behavior is unchanged; this does not claim full stock AI equivalence.

The exact v78 ROM fails structural bounds checks for four pad files: mp1, pam,
sho and stat. War uses stat. Its setup normalizes vectors past the loaded cover
data and corrupts the neighboring model bindings, leading to a debris-model
fault. See [v78's failure evidence](PD6480iperf-v78.md).

The corrected actual generator passes in-memory count/bounds checks for all 60
NTSC-final pad sources, including the four with filtered records. New exact-ROM
checks independently read the ROM file table, inflate its pad assets and verify
their declared cover extents. Unit tests reject overstated/understated counts
and truncated headers.

Rebuild started with the four affected JSON inputs forced newer via make's `-W`.
This also recompiles dependent C objects. Do not label or copy the previous
`build/ntsc-final/pd.z64` as v79 before that build successfully completes.

Required next checks: exact v79 ROM pad/asset audits, a fresh cold-start state,
War plus the other affected stages, Hi-Res on/off and L graph, xdelta round trip,
then ED64/Elgato testing with Plug 1 powered off afterward. Do not reuse a v78
state: resident code may be unchanged while its loaded asset contents are old.
Long play, multiplayer, interactive hardware controls and Analogue remain
unverified.

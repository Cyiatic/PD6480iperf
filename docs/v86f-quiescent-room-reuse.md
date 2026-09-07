# v86f quiescent room-memory reuse

Runtime code `87952368964433608af2171e742c4e664e205a67`.
Normal retail-header ROM SHA256
`bf219fa49620be957f366cb2b84ba255d67712bb36faf3e494ddfabfae7fa41e`.

Main is the sole graphics producer. Before reclaiming recently used room
geometry, schedIsGfxIdle raises priority above the scheduler, tests all current
RSP/RDP and both pending graphics-owner slots, then restores priority. Non-main
callers and unknown RSP task types cannot use the idle fast path. Audio-only
ownership does not read room geometry. The current room-cache epoch remains
pinned even when idle; busy graphics retains the prior three-epoch rule.

No framebuffer dimensions, RAM limits, room-bank sizing or late reserve changed
from v86e. The actual-C scheduler and allocator tests exercise ownership,
priority restoration, wraparound and current-epoch pinning with negative controls.

In the same cold10800-tick ordinary-input Agent AI-co-op Infiltration sequence,
v86d had43 room-load failures, v86e12, v86f0. The new idle path was used8 times
(18total evictions). Final gameframe640 is alive/unpaused640x480 with L off;
heap partition valid and no missing visible room. Fresh four-controller CI and
four-player Skedar setup/movement/pause/resume also have no allocation faults.
These are bounded software samples, not whole missions or all co-op variants.

Normal-ROM real-N64 upload completed in37.28s. Elgato recording shows city/ship
flyover and Joanna's rooftop past boot, followed by Nintendo at the final sample.
This proves3D intro, not interactive uninstrumented gameplay. A separately
labelled replay branch is distinct from this ROM and redirects save writes to
RAM. Only Plug1 was targeted and OFF was verified; inspected recording deleted.

Small evidence and test tools live on private PD6480iperf's mods/performance
branch at evidence/v86f-quiescent-room-reuse. The21-mission software matrix finds
20load-gate passes but an Extraction stall at gameframe3, reproduced in an
uninterrupted run.19final snapshots are alive and unpaused; Duel ends dead from
unattended combat. A labelled Agent hardware replay shows alive Infiltration
pause/navigation/L then short resume/combat death. The candidate is held.
An older v86b control reaches Extraction while v86f also stalls under pure
interpreter. Continuous cold v86f one-controller9150ticks reaches Extraction
frame1434 alive/unpaused640x480 with no faults; keeping four controllers on the
original restored-menu path still stalls. Thus this is state/setup-dependent,
not a demonstrated unconditional mission failure. Its cause is not yet isolated.
No new Analogue result is asserted.
The normal ROM retains fixed640x480i, full-screen menu blur and the L graph.

Follow-up controls: continuous cold v86f with four controllers also stalls at
Extraction frame3; restoration is not required. The analogous cold v86b control
reaches frame1437 alive/unpaused. Restoring a fresh cold-one-controller v86f
menu seed with matching save memory reaches frame1434 with either one or four
controllers (game-verified masks1/15). Boot/menu history is implicated, not an
unconditional failure or simple controller-presence rule. A separate diagnostic
branch counts existing full interrupt-queue discards without retrying them;
it does not change this normal ROM. Normal ELF rebuild matches the prior hash.
That diagnostic cold-four run reaches Extraction frame1434 alive/unpaused,
with all16 drop counters zero, but does not reproduce the normal failure.
Its changed layout/startup timing means this does not exclude queue overflow
in the normal failed run or establish any fix. Evidence is on mods/performance
under evidence/v86f-quiescent-room-reuse/event-drop-diagnostic.

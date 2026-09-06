# v86e: improved, still fails the room-cache gate

This is internal software evidence, not a new hardware/Analogue candidate.
Runtime source `3f6336d766aa7fcc86802d98e96cc3c5c028a275` on
`experiments/v86e-prepaid-head-reserve`. Normal ROM SHA256
`a9143f02981b7e44448f70638dd36ef679ad2a0d3ffcfd524f86e9c5e9d73bf3`,
ELF `716973dc5894b575355334474e5ca98ee6c04bec49b59e99ef0aa088f3d57f09`,
retail CRC `bcb684bc/0250ba5e`. No allocation instrumentation/replay in ROM.

Preloading the default co-op buddy's head uses part of the later-allocation
budget. v86e credits only its actual retained model size (21792 bytes in this
sample), not temporary loading space or textures. It keeps full640x480 colour
and depth buffers and the existing current-plus-two-graphics-epochs safety rule.
Both actual-C unit suites pass. The compressed ROM asset audit validates1403
streams;608 raw assets are not covered by that check.

`v86d-watch` and `v86e-watch` preserve two completed cold10800-tick runs, the same
ordinary input, external stock Dark EEPROM, and source-specific ROM/ELF hashes.
These are Agent AI-co-op Infiltration, not solo: mission co-op=true, AI buddies1.
Core uses cached interpreter, software video,8MiB and the EEPROM-header adapter.
No RAM-write argument was supplied. Counter and gate addresses are derived from
each ELF and checked against the log; per-event RAM/state/PPM hashes are retained.

| Observation | v86d | v86e |
| --- | ---: | ---: |
| Final room bank bytes | 38512 | 54032 |
| Historical load failures | 43 | 12 |
| Final level frame | 631 | 684 |
| Final OOM / dead / pause | 0 / 0 / 0 | 0 / 0 / 0 |
| Final dimensions | 640x480 | 640x480 |

The v86d first event at frontend9780 / game305 has visible rooms5/6 missing,
only2160 free bytes and largest span1088. Loaded rooms were used at epochs304/305,
so the existing safety rule properly refuses eviction. v86e still misses room6
at epochs299–301 and room32 at307–308: largest span10880 cannot fit their17904/
17584 workspaces. This is missing required geometry, not just skipped preloads.

Watch samples are captured at libretro return, which can be inside a game frame.
v86e's first event is **rejected** by the strict partition validator (hole/overlap).
The evidence retains that error and `partition_valid:false`, with no fabricated
snapshot. Later events and the completed final snapshot validate. A mid-update
sample is possible, not asserted as fact. The final inspector was not weakened.

The frontend bounds captures at8. v3 SHA256
`4948ac601ae698f3c4f6df316d0ebd14802c64aee31da2e527469c6a4fc456d2`
was used for v86d's cold run; v4
`38999d88cc858389ecb6095563018f18427d92e067cb056bfa3f1c326b74c805`
adds priming of an existing counter after state restore, used for v86e.
The restore regression correctly starts at historical43 without inventing a
new failure event. Parser/endian/gate/reset/range/cap/read-only tests pass.

`settled-controls` continues the matching v86e final state for600 idle ticks:
frame1196, alive/unpaused, health0.93125, graph off, OOM0, still12 historical
failures, no missing visible room in that final sample. Full-screen blur and
inventory are visible in the pause still; horizontal inputs and L were exercised.
This is not a whole-mission, persistent-menu-warp, multiplayer or benchmark pass.
The remaining stage free space was only12752 bytes at frontend10800.

No patch/ZIP promoted. Next: prove safe allocation/lifetime savings, without
arbitrarily shrinking reserves or weakening graphics ownership. No hardware test
here: the previous powered-on ED64 absence remains unresolved. Exact Plug1 OFF
was independently confirmed; the unrelated N64 switch was not targeted. No new
Elgato recording exists. ROM/RAM/state binaries are not committed.

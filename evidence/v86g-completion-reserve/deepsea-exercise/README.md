# Normal-v86g Deep Sea movement, firing, pause and L

This is the normal retail-ID v86g ROM, not the labelled hardware diagnostic.
Original ParaLLEl core/cached interpreter, Angrylion/cxd4, 8MiB and mask15.
No ROM instrumentation or RAM writes. The same in-memory EEPROM header adapter
and full matching 296960-byte save image are used throughout. All commands
are ordinary controller inputs; neither health nor mission configuration is
patched. These are short software checks, not hardware/performance benchmarks.

Parent is the completed `headless-v86g-solo-matrix/deepsea` sample: Solo/Perfect
Agent, frame251, aliveHP1/unpaused,640x480. Parent report is retained here.
The 600-tick direct continuation walks, fires, pauses, swipes right and left.
Finalframe474: aliveHP1/paused, ammo8to5 and position changed, graphon,640x480.
No OOM/cache-load/allocator/CPU faults; valid room partition. The final pause
image was visually inspected: blur covers the whole view, not one quadrant.
This sample remains a separate exercise, not a preferred replacement for the
startup matrix's original Deep Sea result.

Pause state SHA256:
`b96b29836d42f00fc114e971cdbf132ece067223ab062faadb878e922a288283`.
Matching full save SHA256:
`ad1791c4ea908b7c3c069696672f7dbda31493cb49656d71c037593dd939bd1e`.

A further600ticks restore exactly that state/save. B at30 resumes; L at120
hides the graph, ordinary movement at360 changes position, L at450 shows it.
Both immutable tick300/tick600 images were inspected: graph absent/present,
with rendered gameplay in each. Both hosts returned0 and emitted final video.
Finalframe1007: Solo/PerfectAgent, aliveHP1/unpaused,640x480, graphon, mask15,
zero OOM/cache/allocator/CPU faults and valid partition. No complete-mission,
long-session or measured-console-FPS claim follows from these bounded samples.

Resume state SHA256:
`b6bffaa14ac18c785ae882f14bec332d09df586c22ceea1cba9724f67d841172`.
Resume RAM SHA256:
`b27c2b9065263df5564a90c60ea6ba29afc498dc6ba1a31327af9d4f38c82955`.
Normal ROM SHA256:
`79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`.
ELF SHA256:
`07595b1d4c7466bf3ac53f1df29bc21779c8d494eb41978a2c47d735e84ac010`.
Host SHA256:
`38999d88cc858389ecb6095563018f18427d92e067cb056bfa3f1c326b74c805`.
Core SHA256:
`4f239ad5ba11887d70e6887b648237f81ab9dfeb6f80f463153abc513e0ebad7`.
Binary ROM/RAM/state files remain local; only logs/reports/inputs/stills are
retained in Git. No power or capture-card operation was needed for this test.

# v86g normal-ROM Solo startup matrix

All21 stock Solo/PerfectAgent missions reach the cache-aware initialization
gate with final unpaused samples:640x480, no cutscene, no OOM/cache-load/heap
or CPU exception, warmed required textures, complete currently visible room
geometry/hit batches and valid non-overlapping room heap. This is not a full
geometry-preload promise: nonresident but warmed rooms are listed explicitly.

Final players are alive in19samples. G5 Building and Duel end in ordinary
unattended combat death, not CPU exceptions. Their red death views were
inspected and remain failures of an alive-gameplay criterion. Do not call this
21 alive playthroughs, or replace their final results with earlier paused views.
All21 selected final images were visually inspected, including the two deaths.

The collection retains33samples:21initial loads, five later Start inputs for
opening cutscenes, and seven B inputs to resume initialized paused samples.
Initial gate16/21, final gate21/21, final unpaused21/21, alive/unpaused19/21.
Extraction's initialframe106 was still a cutscene; its continuation reaches
frame1586 aliveHP1/unpaused. It does not reproduce old v86f's frame3 stall.
The initial runner correctly exits1 for the five unfinished cutscenes; every
individual host exits0 with final video, and every continuation exits0.
No failed allocation/CPU exception was continued through or cleared.

Each mission begins at the same fresh normal-v86g Solo Mission Select seed,
with Defection visibly selected before the run. Its full296960-byte save image
is preserved; all four controllers remain connected(mask15), while game fields
prove Solo, not AI/human co-op or counter-op. Inputs use the stock mission,
difficulty and Accept handlers. There are no mission-memory writes, synthetic
input ROM patches, foreign-build save states, or erased-save substitutions.
Source/ROM/ELF/layout/save/RAM/controller identities are checked by the scripts.

Original downloaded ParaLLEl core, cached interpreter, Angrylion/cxd4,8MiB,
same in-memory EEPROM header adapter. ELF-authenticated RAM is reinspected
after all hosts finish. The collector accepts only direct parent-state/RAM
chains, not the best result from unrelated attempts. Detailed inputs, terminal
logs, final stills and reports are retained in each source-named directory.
Binary state/RAM/save/ROM files remain local.

Collection: `v86g-mission-chains.json`. The separate Deep Sea movement/fire/
pause/swipe/resume/L exercise is documented in the sibling folder; it is not
substituted into the startup matrix. No hardware, Analogue, long-session,
whole-mission, multiplayer or controlled-speed benchmark pass is claimed here.

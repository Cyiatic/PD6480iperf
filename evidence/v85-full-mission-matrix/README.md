# v85 full mission selection matrix: known memory failures

2026-09-06, normal unmodified v85 ROM, ordinary controller menu inputs in
cached-interpreter/cxd4/Angrylion software, 8 MiB. Not hardware proof.
Each mission starts from the same matching-v85 Mission Select state with
Defection highlighted; no cross-build state, RAM pokes or diagnostic ROM.
The host's EEPROM-header adapter leaves the disk ROM unchanged.

ROM SHA256: a candidate originally delivered as
`430f09bbe0b76bfe687881c52ac23ec4cfff0cc4a16b9ba5faecd602ffc037a4`.
ELF: `81af590340c372b80d4d9c3bcada0056566505a2ce482de4ec11f618a8d0ad5a`.
Compiled version-3 layout:
`6146563e995a9a3eff3e86af6118ca01341628b2b2382ac523610bbb28f6d200`.
Seed: `22dcc514d5c8cb2176ce3e3f33b888bcc805b6afd534057607715e7b2b44212a`.

`collected.json` reinspects all 21 completed samples with the strict gate:
correct stage, frame >100, normal tick mode, no cutscene, full 640x480,
no OOM, all mission-specific preloaded room geometry and vertex batches,
and no main/scheduler thread fault flags. A paused initialized sample is
identified separately; it is not an unpaused gameplay or playthrough claim.

**11 fail:** Extraction, Villa, Infiltration, Rescue, Escape, Air Force One,
Pelagic II, Deep Sea, Defense, Attack Ship and Maian SOS. Each reports a real
stage allocation failure and missing room data. Extraction, Infiltration,
Pelagic II and Deep Sea additionally fault in the main CPU thread; Pelagic II
has a partially loaded room 100 with missing vertex batches. Some failures
still show a first scene, so a picture or boot alone is insufficient.

**10 pass only this short initialization sample:** Defection, Investigation,
Chicago, G5 Building, Air Base, Crash Site, Skedar Ruins, Mr. Blonde's Revenge,
WAR! and Duel. Six are paused final samples; only Defection, Air Base,
Mr. Blonde's Revenge and Duel finish unpaused. Earlier longer Defection and
Air Base checks remain valid for their recorded durations, not other missions.

This supersedes any inference that v85's full-room preload strategy is
whole-game viable at 640x480. The historical v85 ZIP is not silently replaced.
Full-size two colour buffers plus depth use 1,843,264 bytes versus 563,264
for the original performance core's three 320x220 buffers plus depth:
an extra **1,280,000 bytes**. The Expansion Pak is already enabled; total RAM
is 8 MiB. The v86 experiment adapts room residency within this budget without
lowering resolution or reverting the modern CPU/performance code.

Raw per-mission RAM and states remain local under v85-mission-matrix-a/b.
The copied small screenshots, input sequences and reports retain provenance.
WAR! pause and Maian SOS final screenshots were visually inspected: the former
has full-screen pause coverage; the latter shows missing surroundings while
the FPS display itself continues updating. Neither is hardware evidence.

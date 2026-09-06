# Real N64 diagnostic 2 — inspected 2026-09-06

Diagnostic only: a200942799b7b9ed02b3513763dc1bc00f381ea22682f5d63b553b4a10734fc9,
source fa662646b, ELF e348b1d7f09f946714db525434d86f791140639776acaec5642286597d21a008.
Normal candidate remains c33ec145... and has no input/RAM-save test hooks.
Only the replay timing/death guard/HUD differ from diagnostic 1. Runtime
rendering, room residency, menu math, scheduler, assets and buffers are unchanged.

Exact ED64 FTDI restarted with Plug 1 OFF, then 35-second dwell and prerelease
UNFLoader. Native upload exit 0 after 36.8 seconds at 20:12:12 UTC. No full-image
readback claim. Fresh Elgato capture began after upload, with 45-second startup
allowance and 240-second observation. Segment 2 begins at about +156.16 seconds.

Visually inspected:

- Segment 1 +5/+25: Dark file select and horizontal Game Files menu transition.
  +45: CI 3D. +75: mission-loading black. +95: Infiltration first-person terrain,
  NPC and gun, graph hidden, ST47/D2, FB640x480, OOM0/BGFAIL0/EVICT6, DEAD0.
- +115/+125/+135/+145: alive phase4 pause menus, both horizontal directions,
  eyepiece/light animation and full-screen blurred scene, not a top-left quarter.
  Graph visible. No stale rectangular fragments seen in these samples; the
  game's intentional perspective and eyepiece animation remain enabled.
- +155 and segment 2 +0/+5/+10/+15/+20: Video Options / fixed 640x480i label.
  Graph hidden at segment 2 +0/+5 and shown at +10/+15/+20, DEAD0 throughout.
- Segment 2 +25/+26/+27: back from Video Options to paused objectives.
  +28/+29: menu closes onto 3D while damage starts; DEAD0 at +29. +30:
  death transition, then +40/+70/+90: ordinary mission-failed menu, phase99.
  The guard correctly stops the scripted replay after death, rather than
  incorrectly continuing through post-death menus as diagnostic 1 did.

Bounded real-N64 gameplay, alive pause blur, menu swipes and L toggling are
observed. Return to 3D is very brief before ordinary enemy-caused death; this
is NOT a sustained gameplay pass, whole mission clear, benchmark, normal-ROM
interactive hardware test or Analogue test. No exception screen observed in
the samples. The final death condition is retained, not labelled a pass.

Matching cold software6000 test also reaches the alive pause and fixed label,
then dies after resuming (phase99, DEAD2, health -0.08749995, pause3, frame762).
Final OOM0, cache load failures0, allocator faults0, evictions6, exact valid
heap partition, normal CPU thread flags0 and 640x480. RDRAM SHA256
4c16a0f2f0004a5f4c19f28c88875923d0503ee7026148130cde8340e1ab4472.

Owned GameCapture stopped. Plug 1 OFF at 20:16:59 UTC, Relay: 0 verified
20:17:00. The exact six inspected files below were then permanently deleted;
small stills and copied desc/info remain. Combined size: 465302168 bytes.

| File suffix | Bytes | SHA256 |
| --- | ---: | --- |
| _0001.ts | 290981512 | f14fe5b92476f34d6c20ab0f9ce25627ceb8495b2cb8b742434a12e8589a2b15 |
| _0001.meta | 81920 | b8ebbf89d16a170f19ec6f1cb7604f5b7d865d70a678ee40e1670f469d5658e4 |
| _0002.ts | 174188204 | 56a2d3e82554d0b28dd7892d9e6139180834b91726d65875b9f299e1d8a985b2 |
| _0002.meta | 49152 | 2300c945576b6273cbda434905584bb6271de35b255db145ac2dc9b8c3fbd680 |
| .desc | 850 | b950020f91af3b9a99c877daa69b01a95e6dc4e80c3823a6f1270f3933fbd307 |
| .info | 530 | 43c069ef0ec288e383f07dc20486262a65a75d105cddab6e1246424e65530406 |

All names begin Recording_####YYYY-MM-DD_hh-mm-ss#### in the exact Elgato
Timeshift directory. OverlayTimeline.json is unrelated and must be kept.

# Separate v86f Agent gameplay replay on real N64

This is a labelled diagnostic, not the normal candidate and not an Analogue run.
Source `ecf75320314a4889f4e11e8092330996a3ede0a7`, ROM
`c8be199f3fba9dfeb85774391276a3f3e97b32ec2028b0bd50863386dcabef44`, ELF
`7414fc9065917030c3ffbc824e2e8ea67ea651c27710c6c8faa22d1c584a7ccc`.
It reuses the reviewed input-partition/RAM-save harness on v86f. Stock Agent
is selected through the real difficulty handler, without health/enemy changes.
All EEPROM access is RAM-only; Controller/Transfer Pak writes are blocked.
Visible V86F TEST HUD distinguishes it even while L hides the graph.

Software6000ticks reaches Infiltration, gameframe723, alive/unpaused, health
0.3699693, phase7/tick460, fixed640x480, one fixed-label visit, graphenabled1.
RAM save reads45/writes10; zero OOM/cache/allocator/CPU faults,6evictions and
valid partition. This is not a completed replay: phase8 has not yet been reached.
State hash `b8a413e3fc0a94517ef1c3a4c26a6e190f2d2238e1f78517d02a0d24801568fd`;
RAM `71cc4db4ba2345a7b327067c698c69445372515cb90d24764b8ea6b9bc7e320b`.

## Console trial (UTC 2026-09-06)

Only Plug1 targeted. OFF23:42:10, exact FTDI reset23:42:20, ON23:42:21,
35-second dwell, terminal UNFLoader start23:42:58. Uploader reported
`ROM successfully uploaded in 39.19 seconds!`, native exit0 at23:43:37.
No full-image readback claim. Capture PID20016 started23:43:37, followed by
45-second startup and360-second observation. Finished23:50:23, OFF confirmed
23:50:26 and statusRelay0 23:50:27. Neither the unrelated N64 outlet nor any
unowned process was targeted. No UI interaction in this trial.

The completed recording contains three inspected segments (677442584bytes total):

| Segment | Bytes | SHA256 |
| --- | ---: | --- |
| 1 | 291025128 | a0accd374883728daa60fa8dd2c8d5f3766724e84ccd626410c233a11a72d85a |
| 2 | 291300548 | 85b268d950c9bb5db62555a3cce6a65d5a2cd33a4e6d775dc2bcfa3eb8552571 |
| 3 | 95116908 | fb0c98998556078c146cc9674d56abf3feb26f8e25602bb8341047f9ee3ed2c8 |

Segment1/2 span about156.156s each; segment3 about50.7s. The retained descriptor
provides exact90kHz timestamps. Capture is processed Elgato video, not direct
VI-register measurement.

All retained stills were visually inspected:

- Segment1+10s: stock Dark file select, full-screen blur and eyepiece.
- +40s: CI3D; +80s: Infiltration opening.
- +120/+138s: alive paused Infiltration with full-screen blur and status menu.
- +145s: Video Options/fixed640x480i, graph on; +150s: L graph hidden (testHUD
  remains); +154s: graph shown again. No resolution reallocation checkbox.
- Segment2+10s: Video Options; +35s: resumed3D, low health.
- +60s and all later samples (+100/+145, segment3+10/+40): normal mission-failed
  death menus. These are not pause-blur or sustained-play evidence. The replay
  stops on death rather than altering health/AI to force success.

Observed HUD OOM0/BGFAIL0/EVICT6; no exception screen observed. This proves alive
pause/navigation/L and a short resume on real N64, not a completed mission,
completed death-free replay, or normal-ROM interactive hardware verification.
Separately, normal v86f's software Extraction sample stalls at gameframe3;
the new candidate is held despite this diagnostic's successful menu observations.

The three inspected TS files and exact meta/descriptor sidecars were permanently
deleted after inspection (677632238bytes including sidecars). Only stills,
copied descriptor and logs remain. Timeshift now contains only its177-byte
OverlayTimeline.json, not any of this trial's recordings.

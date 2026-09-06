# Real N64 diagnostic 1 — inspected 2026-09-06

Diagnostic ROM 39082bc3857e1f1728e3f3dcfe2e733815774061d3b34f5469a617cb2bb09e59.
Exact saved FTDI device restarted with Plug 1 off, then 35-second cold boot dwell.
Prerelease UNFLoader native exit 0 in 36.6 seconds. Not a full-byte readback claim.

Visually inspected segment 1 +5/+25/+55: file select, Game Files and main menu,
with labelled synthetic replay. +85: mission transition; +115: first-person
Infiltration terrain and gun, graph visible, OOM0/BGFAIL0/EVICT6. +145: red
mission-failed screen. Segment 2 +10: failed objectives; +40: video options over
death background with fixed 640x480i label and graph hidden; +70: black;
+90: Carrington Institute 3D. No exception handler observed in these samples.

This confirms bounded mission gameplay and L graph visibility on real N64,
but NOT the intended alive pause-blur/resume test. The automated player died
before phase 4, and the harness incorrectly continued through post-death menus.
Do not claim those frames validate paused gameplay blur. Revision 2 shortens
initial movement and rejects death before menu tests; the normal ROM is unchanged.

Worker stopped its capture, switched only Plug 1 OFF at 20:06:08 UTC and
verified Relay: 0 at 20:06:09. The exact six inspected files below were then
permanently deleted (471237328 bytes); 10 small stills and desc/info copies remain.

| File suffix | Bytes | SHA256 |
| --- | ---: | --- |
| _0001.ts | 291090176 | e187784c93039f8ccc21c221fccb6ef23b1762905cdc4a3f7d9054eb04eaff88 |
| _0001.meta | 81920 | fc2d229b0459ce29cecbed1aedbbd9a2c0201882dd6e70e59123b3ccc19be803 |
| _0002.ts | 180014700 | d19e47f9d7d70f2f47a42412453e6fbb0b92c8de2a463db73a8951fa1bd57b3b |
| _0002.meta | 49152 | 4689d40ebf0228b3ec2c3dd374fbdea1c5c1253440475991162ad807eadb5b8e |
| .desc | 850 | 1bed3b2b97709510d8a9de49e5b486133fa194ade794903901126a9b83195664 |
| .info | 530 | 43c069ef0ec288e383f07dc20486262a65a75d105cddab6e1246424e65530406 |

All names begin Recording_####YYYY-MM-DD_hh-mm-ss#### in the exact Elgato
Timeshift directory. Combined size: 471237328 bytes. OverlayTimeline.json is
unrelated and must be kept.

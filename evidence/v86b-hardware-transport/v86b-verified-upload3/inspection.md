# Failed 4-KiB transport trial, not a ROM boot test

Normal v86b c33ec145... ROM; transport v4 4ab8ee4... executable.
Readback matched through byte 483327, then the next 4096-byte read timed out.
No START_COMMAND_SENT or full-image match. Fresh Elgato frames at segment
+5, +35 and +55 seconds all show the EverDrive menu. No game crash is observed.
Plug 1 OFF at 19:50:32 UTC, Relay: 0 at 19:50:33. Capture/uploader stopped.

After visual inspection, permanently delete the four exact recording files,
total 114086026 bytes, keeping stills and copied metadata:

- Recording_####YYYY-MM-DD_hh-mm-ss####_0001.ts: 114052268 bytes,
  56f2c8bd6888f40df252387d7559f1cb046bc00f487fb4c0bc74466c2f1cb3fa
- Recording_####YYYY-MM-DD_hh-mm-ss####_0001.meta: 32768 bytes,
  9f74323aab3e833ac5e0f312115e749544eaf4b9e13332642117e76e10b78300
- Recording_####YYYY-MM-DD_hh-mm-ss####.desc: 460 bytes,
  6150ffb7642b1156c0ba72346c653b3252a2b5582b0554e7a5a7e7e94342a892
- Recording_####YYYY-MM-DD_hh-mm-ss####.info: 530 bytes,
  43c069ef0ec288e383f07dc20486262a65a75d105cddab6e1246424e65530406

OverlayTimeline.json is not deleted. The normal ROM remains unchanged.

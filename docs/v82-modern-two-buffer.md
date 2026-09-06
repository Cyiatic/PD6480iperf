# v82: two-buffer newer-core experiment (not a release)

Parent f5e6c70bd includes the newer bf3245076 performance core and lazy CI
menu preview buffers. Two full 614400-byte colour images replace three:
8036a000 and 8076a000; the expansion heap starts at 80400000, recovering
614400 bytes. Depth remains a full 614464-byte aligned allocation. CPU/AI,
uncached writes, all-room and weapon preloading remain on the newer core.

Both immediate and queued graphics dispatch check current/next VI, scheduled
and queued image ownership, including physical/KSEG aliases. Retraces retry
dispatch after releasing ownership. Static copyright synchronization tasks
are exempt; they never render into either gameplay image. Audio retrace yield
now explicitly checks for a current RSP task. The two display-list/task slots
and two VI mode slots are unchanged. The three-entry artifact ring is unrelated
and unchanged. Host tests of the actual gate pass bounds, aliases, ownership
slots, swap sequence and static texture cases. These are not hardware tests.

ROM SHA256 f555bbb92e35dc8e2e9170be924bb19a32fdad12ffae39765b063dc684ff7fa2
ELF SHA256 0377ee3a87176046c1dc3ef50c05fb1a6a0ece0757c52e6b8f3010dd815cb20d
CRC1/2 ac94469f / fca6f766

All 1403 compressed assets and 60 pad-cover extents pass (608 raw unchecked).
The normal 5100-tick fresh emulator test rendered CI at 640x480 and loaded all
140 room geometries. OOM remains zero and 484688 stage heap bytes remain.
Nevertheless this run FAILS: opening mission briefing passes a NULL menu
scratch buffer to setupLoadBriefing/fileLoadToAddr. Main thread PC 80005644,
Cause 8, BadVAddr 25040, RA 80194db0 (fileLoad), destination a1=0. The v81b
lazy allocation incorrectly treated the shared buffer as model-preview-only;
briefing and multiplayer descriptions also consume it directly. This is our
integration regression, not evidence of an Analogue-specific defect.

No hardware upload. Plug 1 remains off. No new candidate package is published.

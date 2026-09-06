# v84 normal-ROM mission regression (software, not hardware)

Continuation after the v84 menu-fix candidate, 2026-09-06 Phoenix. Unchanged ROM
SHA256401d5507968d5a37756dad280a43d89d481fbbdf21fc79eeaa0edccdfb98c6d7,
matching v84 ELF and freshly compiled v84 layout. Cached interpreter/cxd4/
Angrylion, 8MiB, eeprom-header host adapter. No RAM writes, ROM code changes,
synthetic in-ROM replay or foreign-build savestates in these tests.

Important: these tests find a remaining v84 issue. They do not retroactively
turn the earlier Institute/intro checks into full-game validation.

Starting from the v84-pause state (the cold v84 lineage recorded in
../v84-fullscreen-menu-blur), A opens Solo Missions; the default is Skedar
Ruins because the stock Dark save's autostage is16 and difficulty2. Five
separate downward stick pulses wrap the 21-item list to Defection. Nine more
from Defection select Air Base. Every selected entry was visually verified.
Launch input pulses A at30/160/300, Start at1050/1230, end1500. The latter
can pause a mission whose cutscene finishes earlier; inspect pause mode.

- Skedar Ruins/Perfect Agent, stage42: frame327, pause3, all137 expected
  rooms loaded, no OOM,363200bytes free. Resume/turn/move/fire test:
  frame602,pause0,health1,ammo8->5,position changed from
  -2307.3003/159/-285.9000 to -1921.1798/158.9996/-302.8662. No OOM,
  355984bytes free. Weapons and L graph render normally.
- Defection/Perfect Agent, stage48: frame227,pause0,health1,gameplay rendered,
  but OOM marker'p'(112),failed allocation61328bytes,53840bytes remaining.
  Only166 of167 expected rooms loaded: room167 is missing. NOT A PASS.
- Air Base/Perfect Agent, stage39: frame182,pause0,all146 expected rooms
  loaded,no OOM, but only6240bytes free. Short initial-load check only.

The allocation investigation found the pause texture reserves0x4b00(19200)
bytes although its sole writer and sole RDP reader use40x30 RGBA16=2400bytes.
The v85 experiment shares dimensions/byte count between allocation, producer
and consumer, returning16800bytes to the stage heap without dropping a
preload, changing render resolution, or reducing the blur texture quality.
v85 results are separate; a plausible fix is not yet proof.

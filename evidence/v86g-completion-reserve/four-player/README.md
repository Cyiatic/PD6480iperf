# Normal v86g four-player memory and menu regression

The immutable normal retail-ID ROM remains
`79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`,
ELF `07595b1d4c7466bf3ac53f1df29bc21779c8d494eb41978a2c47d735e84ac010`.
Original ParaLLEl core/cached interpreter, Angrylion/cxd4, 8 MiB, mask15.
This is software evidence, not a hardware or Analogue test.

A fresh4200-tick cold boot loads stock Dark and reaches CI38/frame1445,
aliveHP1/unpaused, graphon,640x480, all four controllers connected. There is
still only one gameplay player in CI; this alone is not four-player evidence.
No OOM/cache/heap/CPU fault; the final CI image was inspected.
Seed state SHA256:
`00705aeb8a061c3f3799f830afb6775272edc77c2cef933cedc6ce3edb39c447`.

The5850-tick continuation restores exactly that same-ROM seed and its full
296960-byte save image. It follows the ordinary menu/QuickGo/join path, moves
each player's stick, sends Z while unarmed, pauses all four, resumes all four
with B and toggles L off. The input fixture's historical comments refer to f/c,
but no f/c ROM or save state is loaded. Input SHA256:
`abe6a7532a927f8f546e1ae914686bb69c2773700da71cde766d475bdabcc879`.
There are no synthetic ROM input hooks or RDRAM writes.

Both hosts return0 with final video. Final arena is MP Skedar50/frame2042,
Combat Simulator active, no co-op/counter-op/AI buddies, four active players,
mask15 and640x480. Each player has a distinct RAM structure, world position
and viewport. All four are aliveHP1/unpaused. Viewports include the stock
one-pixel dividing lines: (0,0,319,239), (320,0,320,239), (0,240,319,240),
(320,240,320,240). Zero OOM/cache-load/allocator/CPU faults, no missing visible
geometry, zero evictions and a valid room partition.

Images at4200,5100 and5850 were inspected: rendered four-player views with
graph on, four separate Player Ranking pause menus, then resumed views with
graph off. Z was pressed while unarmed, so this does not prove gunfire coverage.
The observed scoreboards do not imply that four saved Dark profiles were
loaded; players use the ordinary QuickGo setup.

Final state SHA256:
`beef2b9aba35cec418b026cb6ae955ee0346a6ccc34b45a0254e4068222a772e`.
Final RAM SHA256:
`c50c2293e9fab6fe058acf168403d676707c302d8366ef9375a496ae2097b993`.
Parent and final full-save SHA256:
`ad1791c4ea908b7c3c069696672f7dbda31493cb49656d71c037593dd939bd1e`.
Binary ROM/RAM/state/save files remain local. This is a short setup/movement/
menu check, not all arenas, simulations, weapons, long matches or human co-op.

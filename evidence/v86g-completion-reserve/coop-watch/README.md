# Normal v86g AI-co-op regression

Continuous 10,800-tick cold boot of the unchanged retail-ID v86g ROM, with the
same ordinary controller fixture used for the earlier v86d/e/f comparisons.
One connected controller selects Agent Infiltration with one AI buddy. It is
not Solo and not a human two-player co-op test. The compiled v6 game fields
confirm cooperative=true, counteroperative=false, ai_buddies=1.

The original ParaLLEl core uses cached interpreter, Angrylion/cxd4 and 8 MiB.
No state is restored and no ROM code or RDRAM is modified. Only the existing
in-memory EEPROM identification adapter is used with the stock Dark EEPROM.
A read-only frontend watch obtains its addresses from the normal-g ELF:
counter8007fd0c, mode gate8007fd18, value3, maximum8 event captures.
The collector independently checks these against the log and ELF.

Result: native0, final video emitted, Infiltration47/frame635, Agent, alive
HP1/unpaused/out of cutscene, full640x480, L graph off. Zero room-load failures,
zero allocator/OOM/CPU faults, no missing visible room and valid room partition.
17 room evictions, including8 graphics-idle reuses. No watch event fires.
The earlier d/e/f runs had43/12/0 room-load failures respectively; g retains
the zero-failure result in this bounded fixture. This is not a speed benchmark.

The paused tick10500 and final10800 images were both inspected: inventory/
eyepiece over full-screen blur with graph on, then rendered gun/landscape with
graph hidden after the ordinary L/B inputs. Host video advances again after
the same stage-transition interval seen in f. Final output is not inferred
from native0 or a stale black image alone.

State SHA256:
`0923f92b9e952ffaa87f7e4e57ff367340edf0891800cf56af764eac58c1968b`.
RAM SHA256:
`27b33af38d4764c1e3500349e27176c4f4f4c603e544dea4f587d6eae5765754`.
Full ROM/ELF/layout/core/host/input/save/log identities are in final.json.
Binary ROM/RAM/state files remain local. This verifies this short software
co-op path, not every co-op mission, AI behavior, human co-op, long sessions,
normal-ROM interactive hardware, or Analogue compatibility.

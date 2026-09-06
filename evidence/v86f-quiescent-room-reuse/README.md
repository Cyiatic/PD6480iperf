# v86f: quiescent graphics reuse, bounded verification in progress

Normal source `87952368964433608af2171e742c4e664e205a67` on
`experiments/v86f-quiescent-room-reuse`. Normal ROM SHA256
`bf219fa49620be957f366cb2b84ba255d67712bb36faf3e494ddfabfae7fa41e`,
ELF `82d6a0e7ffe479c2eb2e2b11efa9b992c0493d58ca4688dbf9be5804328d2511`,
retail CRC `f27d6fa5/2f4fc739`. No replay or allocation instrumentation in this ROM.

## Memory change

Keep the v86e room bank and late-allocation reservations; retain full640x480
colour/depth buffers. Before evicting room geometry, the main-thread-only
`schedIsGfxIdle` raises priority above the scheduler and samples current RSP,
current RDP and both queued graphics owners. Unknown RSP task types are busy;
audio-only is safe. It restores the original priority on return. Main is the
only graphics producer and cannot submit the new frame until after this call.
While graphics is busy, the old current-plus-two-predecessor epoch rule remains.
When graphics is entirely idle, old epochs may be recycled; the current epoch
is always pinned. This is reuse within the existing8MiB, not extra RAM or a
resolution reduction. `g_BgCacheIdleEvictions` counts actual use of the new rule.

Compiler-derived read-only ownership inspections of all8 v86e watch snapshots
find all four graphics-owner pointers empty. These are libretro-return samples,
not proof of ownership at a past failure instruction; the new runtime check is
atomic. The independent48-byte layout hash is
`4d8e6bf55b2164b5a301185685ebe9c2ea3c2a90d43874c8f72e0ccf9c17e965`.
Actual MIPS disassembly is retained. Actual-C tests cover32 owner combinations,
priority entry/restoration/non-main rejection, plus the negative unlocked case.
The real allocator/epoch test covers100000 fragmentation operations and
512x512x2 busy/idle/wrap combinations. The43 Python tool/inspection tests pass.

## Completed ordinary-input software samples

All use immutable matching ROM/ELF, cached-interpreter/software rendering,
8MiB, an in-memory EEPROM header adapter, and no emulator RAM writes.
Plans retain ROM/ELF/core/host/input/save/state hashes and parent relationships.

- Cold AI-co-op Infiltration/Agent10800ticks: co-op=true, AI buddies1, gameframe640,
  alive, health1, unpaused640x480, L graph off. **Zero load failures**,18evictions,
  8new idle-rule evictions, valid partition, no missing visible room. The same
  sequence was43failures on v86d and12 on v86e. This is one bounded path, not a
  whole co-op mission. Full-screen pause blur and final3D stills were inspected.
- Fresh CI with four connected controllers, followed by ordinary Combat setup,
  four-player Skedar movement/pause/resume/L: finalgameframe2367, fouralive,
  unpaused players, distinct viewports/positions, no OOM/cache/allocator faults.
  Final and pause images were inspected. Z was used while unarmed, so no gunfire
  or whole-match coverage is claimed.
- Fresh Solo Mission Select: compiled fields prove no co-op/counter-op/AI buddy;
  Defection highlighted was visually verified before the21-mission matrix.
  The matrix is not yet recorded as complete here.

## Hardware

The first normal-v86f transfer timed out65s with empty redirected logs; no capture
started. The next bounded worker inherited a tool-provided terminal, exposing
UNFLoader's completed37.28s upload. Captured real-N64 city flyover and Joanna's
rooftop prove3D intro past boot, **not interactive normal-ROM gameplay**.
See [the exact observation and limitations](hardware-normal/inspection.md).
UNFLoader has no full-image readback proof. A separate labelled gameplay replay
is being tested and cannot retroactively prove uninstrumented gameplay.

Only Plug1 was controlled. OFF/statusRelay0 confirmed23:25:51/23:25:52UTC.
The inspected154321868-byte recording and its sidecars were deleted; stills,
descriptor and logs remain. Live-window activation failed with access denied,
but the completed recording was inspectable. No new Analogue result is claimed.

No v86f release bundle is promoted by this evidence yet. Remaining gates include
the complete bounded mission matrix, gameplay hardware observation, sustained
play/menu behavior, further multiplayer/co-op paths and accurate benchmarking.

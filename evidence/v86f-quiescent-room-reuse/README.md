# v86f: co-op improvement, candidate held for Extraction stall

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
512x512x2 busy/idle/wrap combinations. The latest46 Python tool/inspection tests pass.

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
  The complete matrix plus11ordinary-input continuations yields20of21 unpaused
  load-gate passes with unpaused snapshots.19final players are alive; Duel is
  already dead from unattended combat, so it is not an alive-gameplay sample.
  The remaining Extraction sample is stuck, not merely
  an unfinished opening cutscene; see below.

## Extraction stall: candidate not promoted

The initial Extraction run ends at gameframe3. Its600tick state continuation
returns native0 but never emits a video frame; ffmpeg correctly rejects the
missing image, and the continuation runner ultimately exits1 after finishing
the other11runs. Those completed reports remain; no fabricated Extraction
success report is inserted. The32-sample authenticated chain collection keeps
all21initial samples and11successful continuations, with20final passes.

An independent3000tick uninterrupted run starts from the matching Solo menu
seed and replays the exact initial1650tick input prefix plus a later Start.
It also stops at gameframe3. After frontend600 the video counter stays453,
and later frontend calls return almost immediately. Zero OOM/cache failures,
zero evictions (including idle-rule use), valid room partition, no CPU exception.
Read-only ownership shows currentRSP gfxstate0x12 (needsSP+yieldrequested), no
currentRDP owner, and another queued graphics taskstate3. Main and scheduler
are waiting, not exception-flagged. This is not yet a proven root cause.
The pure-interpreter control on the same v86f menu state also stops at frame3
(its log repeatedly prints interpreter startup, retained as a limitation).
The older v86b ROM with its own mode-verified Solo menu state reaches frame1436,
alive/unpaused health1 without faults. Neither control uses a foreign-ROM state.
Their seed histories differ, so this does not yet isolate the change responsible.
A continuous cold v86f one-controller9150tick path **passes**: Extraction
frame1434, alive/unpaused health1, no OOM/cache/allocator/CPU faults,640x480.
Its menu at frontend6000 was visually checked with Defection highlighted;
it reuses the same ordinary input segments on one timeline, no restored state.
Final state `1333e8b4846b34cabc3d754ec5b6ad30575344b8408138b398c56a463c4c659f`,
RAM `3a5bbed2a7c5e2a01029e9a97a22e45b3d182e6e43e3cff17857067441519736`.
The cold final image is very dark with HUD/scope visible, matching the v86b
control's appearance; neither alone proves all Extraction visual effects correct.
Restoring the original f menu state while keeping all four controllers connected
still stalls atframe3, so controller removal is not required. This is a
state/setup-dependent failure, not a proven unconditional ROM mission failure.
The original failed samples remain held as failures, not retroactively replaced.

Follow-up: a **continuous four-controller cold v86f run also stalls at frame3**,
with the same pending-RSP ownership and no allocation failures. Thus a restored
state is not required. The older v86b continuous four-controller control reaches
Extraction frame1437 alive/unpaused. A fresh cold-one-controller menu seed,
restored with its matching save memory, reaches frame1434 with either one or
four controllers (the game confirms masks1/15). See
[the control provenance and limits](extraction-controls/README.md).

A read-only state-register probe uses the exact core revision2f3bf60's published
v1.6 format. All embedded RAM hashes agree with their separately captured RAM.
Failed and good states both have rsp_task_locked0 and deferred-DP flag0; these
simple missing-handshake candidates do not explain the failure. SPstatus differs
(0x243 good/seed,0x2c3 stalled), with SPpc0x040017bc and no DMA busy/full.
These are observations, not a diagnosed core defect. The probe records its
primary source URL and makes no state/ROM/RAM changes.

## Hardware

The first normal-v86f transfer timed out65s with empty redirected logs; no capture
started. The next bounded worker inherited a tool-provided terminal, exposing
UNFLoader's completed37.28s upload. Captured real-N64 city flyover and Joanna's
rooftop prove3D intro past boot, **not interactive normal-ROM gameplay**.
See [the exact observation and limitations](hardware-normal/inspection.md).
UNFLoader has no full-image readback proof. A separate labelled Agent gameplay
replay uploaded in39.19s and shows alive Infiltration, full-screen pause blur,
horizontal menus, fixed video label, L hidden/shown and a short resumed3D view.
The unattended player then dies normally; later frames are death menus, not a
sustained-play pass. See [its exact observations](hardware-infiltration-agent/inspection.md).
It cannot retroactively prove uninstrumented interactive gameplay.

Only Plug1 was controlled. Latest OFF/statusRelay0 confirmed23:50:26/23:50:27UTC.
The normal154321868-byte recording and diagnostic677442584bytes of recordings,
plus their exact sidecars, were deleted; stills, descriptors and logs remain.
Live-window activation failed with access denied in the normal trial,
but the completed recording was inspectable. No new Analogue result is claimed.

Stock USA1.1 plus the same Dark save was also booted without ROM edits for a
menu appearance reference. The original eyepiece has the same device structure;
this does not by itself prove all menu-motion artifacts fixed. Its source ROM
hash is the user's verified4e51142a... baseline; no matching decomp state is
assumed for that retail run.

The xdelta roundtrip matches the exact normal v86f ROM, but no ZIP/candidate
is promoted while the boot/menu-history-dependent Extraction stall remains unexplained. Remaining gates include resolving that
stall, sustained play/menu behavior, further multiplayer/co-op paths and an
accurate performance comparison.

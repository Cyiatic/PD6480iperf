# Perfect Dark - High Performance (PDHP)

## Current 480i development status (2026-09-06)

**v86g progress (September 7 UTC):** a read-only emulator trace identifies the
Extraction failure: retrace traffic blocks the scheduler's completion delivery,
then its interrupt queue fills and discards the next SP completion. The new
notifier reserves two main-queue slots for graphics completions, with no extra
memory or resolution reduction. Actual-C invariant/negative tests pass, and the
previously failing continuous four-controller cold-boot sequence now reaches
Extraction gameplay alive/unpaused at frame1436, full640x480, graph on and no
allocation/cache/CPU faults. Normal v86g also renders the city/ship intro on N64;
this is not physical interactive-gameplay proof. A separately labelled Agent
replay now shows alive pause/menu navigation, full-screen blur, L hidden/shown,
and short resumed Infiltration gameplay on N64, followed by ordinary combat
death. Plug1OFF verified; recordings deleted after inspection. A same-layout
zero-reserve control also passes the cold Extraction script, so that script
alone does not isolate the scheduler policy; direct old-ROM trace and actual-C
capacity tests support the fix. A fresh save-preserving mission matrix is still
running. Still held for broader regression/gameplay checks.
See [v86g evidence and limits](evidence/v86g-completion-reserve/README.md).

**v86f progress:** the same cold AI-co-op Infiltration software sequence now
has zero room-load failures (v86d43, v86e12), with full640x480 buffers, valid
room heap and L working. It reuses old room geometry only after an atomic
graphics-idle ownership check; current-frame geometry remains pinned.
Fresh four-controller CI and short four-player Skedar setup/movement/menu
checks also pass. **The broader solo matrix finds an Extraction stall at
gameframe3**, reproduced without restoring a mid-intro state.20of21 missions
reach unpaused initialization; no memory failure or CPU exception accompanies
the stalled graphics task. The candidate is held while this is isolated.
Continuous cold-boot v86f subsequently reaches Extraction alive/unpaused too;
the stall still reproduces from the earlier menu state with or without a
controller-count change. Its root cause remains unresolved, not an unconditional
mission failure. A normal-v86f ED64 upload completed in37.28s, and inspected
Elgato frames show real-N64 city/rooftop3D intro. That is not interactive
normal-ROM gameplay or an Analogue pass. A separate labelled Agent replay shows
alive Infiltration pause/navigation/L and a short resume on realN64, then normal
combat death. Plug1OFF confirmed and all inspected recordings deleted.
See [v86f evidence and limitations](evidence/v86f-quiescent-room-reuse/README.md).
No v86f bundle is promoted yet; older results below retain their limitations.

**New v86b limitation found:** entering Quick Go with additional controllers
exhausts CI's lazy menu scratch allocation (153600-byte request). CI has one
gameplay player but up to four menu contexts, so the prior reserve was too small.
The error persists into a subsequently started one-player arena; that is not
four-player evidence. v86c's pending-menu reserve passes short four-player Skedar
setup/movement/menu/L checks in software. An additional AI-co-op Velvet head-model
allocation failure is isolated; v86d's earlier head loading prevents that crash
in a cold software sample, but logs43 room-cache failures. It is still not a
clean candidate. v86e credits the already-retained buddy model against the later
allocation allowance: the same cold AI-co-op software sequence improves from43
to12 room-load failures, but still omits required visible geometry. Full640x480,
pause/resume and L continue working in that bounded sample; no new release is
promoted. See [the read-only failure captures](evidence/v86e-prepaid-head-reserve/README.md).
Fresh mode-verified solo Defection/Infiltration/Deep Sea checks pass. The initial
co-op test path was incorrectly labelled solo and is explicitly corrected in
[the new evidence](evidence/v86c-multiplayer/README.md). No new release promoted.
ED64 was absent over USB even with Plug1ON on the latest attempt; no console boot
claim from that attempt. Plug1OFF confirmed, and no new recording remains.
Do not treat the v86b bundle as verified for Combat Simulator setup.

v84/v85 fix full-screen pause blur and stale menu/eyepiece fragments during
horizontal swipes, and label the video mode **Hi-Res: 640x480i (fixed)**.
However, the broader normal-v85 mission matrix finds **11 of 21 initial
mission-load failures** from memory exhaustion/missing room data. v85 is not
a working full-game release. See [the full matrix](evidence/v85-full-mission-matrix/README.md).
The historical v85 bundle is preserved, not silently replaced.

The v86b experiment retains the newer performance core, full-size colour/depth
buffers and L graph, but budgets room residency within the existing 8 MiB.
All 21 stock missions now pass short, ordinary-input **software** initialization
checks with unpaused final samples and no allocation/cache-load faults. Five
opening cutscenes required later Start inputs; seven other samples were unpaused
with B. Original samples and authenticated continuation chains are retained.
See [v86b evidence and limitations](evidence/v86b-budgeted-rooms/README.md).
ED64 uploads subsequently recovered after the exact FTDI reset with Plug1OFF
and35-second cold dwell. Normal v86b reaches the city/rooftop3D intro. A separate
labelled Infiltration diagnostic shows alive gameplay, full-screen pause blur,
menu swipes, fixed-resolution label and L on real N64; it dies from enemy damage
almost immediately after resuming. This is bounded evidence, not sustained play
or normal-ROM interactive hardware validation. Earlier failed transfers remain
documented. See [fresh hardware evidence](evidence/v86b-hardware-transport/README.md).

[v86b patch and stock100%Dark save](artifacts/PD6480iperf-v86b-patch-and-Dark-save.zip)
is available as a **test candidate**, with [hashes and limits](artifacts/PD6480iperf-v86b-README.md).
Analogue, long sessions, whole missions, multiplayer and benchmarking remain
unverified. Plug1OFF confirmed after testing and inspected recordings deleted.
Older sections below are historical development records, not current claims.

A mod that optimises for runtime performance on console.

No accurate benchmarking has been done.

The mod is based off the framerate graph mod, so you can press L to toggle the frame rate graph.

## v79: pad-cover corruption fix, development candidate

v79 corrects the generated cover-record counts that caused War's opening
freeze. The exact ROM passes all 60 pad-asset structural audits and initial
Perfect Agent load checks in all 21 solo missions. Seventeen final snapshots
are unpaused; four are menus. These are not completed-mission checks. Additional
tests pass War's old crash point, a fresh Dark/CI boot, the L graph and actual
Hi-Res on/off inputs. Both modes retain full 640x480 buffers; the checkbox does
not reallocate them.

ED64 uploaded the exact candidate to an original N64. Fresh Elgato footage shows
the city/aircraft/rooftop opening past the logos, followed by a black interval
and the Rare logo again. This is animated-intro evidence, not interactive
hardware or Analogue verification. Plug 1 is off and recordings were deleted.
Whole-level preloading remains disabled; speed has not been benchmarked.
See [v79 evidence, hashes and limitations](docs/PD6480iperf-v79.md).

## v78: known War opening freeze, superseded by v79

The broader 21-mission matrix found a War opening freeze despite 20 initial
mission-start passes. Its generated pad file advertises 425 cover records but
contains only 200; setup writes past that data into model tables. Four generated
pad files have this count mismatch. v78 is not a working full-game release.
v79 fixes the generator count and adds structural bounds checks.

v78 addresses the Infiltration/Rescue startup allocation failures and moves
temporary portal-distance work into reserved loading-time scratch space.
It retains fixed full 640x480i colour/depth buffers and the L graph. Both
positions of the legacy Hi-Res checkbox use the same full-resolution mode.

The exact ROM reaches the opening's city/traffic view on an original N64 through
ED64, verified with fresh Elgato frames. Emulator menu-input tests enable and
disable Hi-Res and resume movement with it enabled; initial Perfect Agent
mission-load tests include the previously failing Area 51 variants.
These are limited tests, not an interactive hardware or Analogue 3D pass.
Whole-level preloading is still disabled, and performance remains unbenchmarked.
See [v78 evidence, hashes and remaining gates](docs/PD6480iperf-v78.md).

## v77: known Infiltration/Rescue load failures

Broader Perfect Agent tests found stage-allocation failures in Infiltration and
Rescue before the first gameplay frame. v77 is not a working full-game release;
the earlier intro/CI passes below are limited evidence. v78 addresses the initial
failures. See [the failure details](docs/PD6480iperf-v77.md).

v77 retains full 640x480 colour/depth storage, the L graph/framebuffer readout,
and v76's bounded streaming cache. It shares identical read-only constants and
retains visited rooms while the cache has at least 64 KiB of contiguous spare
capacity. Whole-level preloading remains disabled; performance is not benchmarked.

An ED64 upload and fresh Elgato video show the original N64 rendering Defection's
animated opening after the logos. Emulator controller-input tests load Dark,
enter Carrington Institute, toggle the actual Hi-Res checkbox on and off, and
resume movement with Hi-Res enabled. The active framebuffer stays 640x480 and
those snapshots report no allocation failure. Interactive console play, console
Hi-Res toggling, broader stage coverage and Analogue 3D remain unverified.
See [v77 evidence and limitations](docs/PD6480iperf-v77.md) and [v76 history](docs/PD6480iperf-v76.md).

v74 is rejected: its framebuffer allocation fails after whole-level preloading.
See [v74 failure evidence](docs/PD6480iperf-v74.md).

Historical sections below are development records, not recommendations to
use earlier candidates. The overall 480i/performance goal remains unverified.

## Current failure notice — v7 is not a working candidate

The user confirmed that `PD6480iperf-v7-raw-haf-2buf-retail-header.z64`
displays product identification and then crashes on Analogue 3D. Its SHA-256 is
`b1e95594dfe7197ba407af0616ad9ab2bb36f841fbfe93983101b7ce91fee19b`.
Do not use v7 as a known-good control or recommend it for another test.
An exact-ROM audit finds **686 invalid compressed asset entries**, including
the Rare logo, which contains a 16-byte header/zero stub instead of its model.
Historical claims below and in older test notes do not establish reliable boot
or playable gameplay. See [the exact-binary crash analysis](docs/v7-boot-crash-analysis.md).

The later candidate that the user could play in Carrington Institute still
freezes when Hi-Res is enabled. No complete 480i/performance fix is verified.
The separate [Dark 100% save](artifacts/saves/README.md) does not fix ROM faults.

Before any future candidate handoff, run `python tools/audit_rom_assets.py ROM.z64`.
v69 and v70 pass this compressed-file audit; that alone does not verify their
rendering, memory layout, or Hi-Res-toggle behavior.

## v69 640x480i resolution candidate

v59 is a live-verified performance/high-resolution candidate, but its active gameplay path is the 640x220 framebuffer with the non-interlaced NTSC LAN1 VI mode. It is not equivalent to the supplied 640x480i patch.

v69 is the source-built resolution correction for console/Analogue testing:

* `artifacts/PD6480iperf-v69-v59-hires-haf1-480i.z64`
* `artifacts/PD6480iperf-v69-v59-hires-haf1-480i.xdelta`

It keeps v59's performance branch and L-trigger FPS graph, enables the existing high-resolution renderer at 640x480, selects the NTSC HAF1 interlaced VI path for gameplay, and allocates matching 640x480 colour buffers. The V1.1 xdelta round-trips byte-for-byte.

ROM SHA-256: `941859DDEFE5C5E51CD818A64C4293176BBC07912ABCACAAD020D882B6DC87C8`

xdelta SHA-256: `A5248FFD42C35F7880D5C8E9277045C589B9629D5379C0F1B219AEF9DA75DE5B`

v69 is not yet hardware-verified: the ED64 FTDI device was not present during the latest upload attempt. See [`docs/PD6480iperf-v69.md`](docs/PD6480iperf-v69.md).

## Current live-verified v59 candidate

The current console-verified candidate is `artifacts/PD6480iperf-v59-hires-old-working.z64`, with its base-specific xdelta at `artifacts/PD6480iperf-v59-hires-old-working.xdelta`.

* ROM SHA-256: `97B0C9FD5E5216B42CFFC1A531F115581AC4FD66FABAAC148AB53EE17F9A635E`
* xdelta SHA-256: `9947F048B899E2DC0DEF22416F3A49424104077013C90B0D309BFE11D51473D3`

It retains the performance branch, L-triggered FPS graph, Expansion Pak requirement, and the high-resolution 640x220 framebuffer/native interlaced VI path. The ROM was uploaded through ED64 on a real N64; after the upload handoff and a 65-second run window, Elgato showed the N64 logo, Perfect Dark logo, and live 3D gameplay. The gameplay evidence is `artifacts/PD6480iperf-v59-live-gameplay.png`.

The v60-v62 attempts based on the newer `pd-perf` source line were also built and round-trip checked, but each produced a uniform-black post-handoff capture on real hardware. They are retained as experiments, not recommended candidates. The newer source line removed the high-resolution-aware renderer paths, so changing only its VI width/buffer declarations is insufficient.

## Current v49 candidate

The current candidate is `artifacts/PD6480iperf-v49-vi-slot-2-480i-performance.z64`, with a base-specific xdelta at `artifacts/PD6480iperf-v49-vi-slot-2-480i-performance.xdelta`. It keeps the performance branch, 640x480i mode, L-trigger FPS graph, and Expansion Pak requirement. It also keeps the retail V1.1 section-2 background fix and leaves section 3 on its original path.

The v49 fix preserves triple colour framebuffers but restores the VI mode-slot ring to two entries, matching the scheduler's two `OSViMode` slots. The ROM and xdelta are packaged and round-trip verified. The v49 hardware upload completed through ED64 in 36.33 seconds; Game Capture HD held `640x480p30` and active N64 audio for approximately one minute. The desktop preview remains unusable for visual verification, so this is a signal/audio-confirmed candidate, not an FPS-graph-verified release. See [`docs/PD6480iperf-v49.md`](docs/PD6480iperf-v49.md).

## Staged v50 candidate

v50 is a two-colour-framebuffer follow-up that retains the raw-HAF 480i VI
registers, two-entry VI mode-slot ring, retail V1.1 section-2 safety fix, and
L-trigger FPS graph. It is built and xdelta round-trip verified, but its
real-hardware upload is still pending because Kasa `Plug 1` was offline during
the latest test pass. See [`docs/PD6480iperf-v50.md`](docs/PD6480iperf-v50.md).

## Staged v51 candidate

v51 keeps v50's raw-HAF 480i VI registers, two-entry VI mode-slot ring, retail
V1.1 section-2 safety fix, and L-trigger FPS graph. It restores the two-buffer
stage allocation and VI unblank timing used by the real-N64-verified v7 layout.
The build and base-specific xdelta round-trip are verified; hardware testing
is still pending while Kasa `Plug 1` is offline. See
[`docs/PD6480iperf-v51.md`](docs/PD6480iperf-v51.md).

* `artifacts/PD6480iperf-v51-v7-layout-section2-safe.z64`
* `artifacts/PD6480iperf-v51-v7-layout-section2-safe.xdelta`

## Staged v52 candidate

v52 keeps the v51 640x480i/performance layout, but restores the performance
branch's small global `FRAMEBUFFER_SIZE` reservation for boot, stack, and
memory-pool boundaries. The actual 640x480 gameplay colour buffers are now
reserved separately inside the VI implementation. This targets the memory
interaction isolated by the standalone 480i hardware control test. The build
and base-specific xdelta round-trip are verified; hardware testing is pending.
See [`docs/PD6480iperf-v52.md`](docs/PD6480iperf-v52.md).

* `artifacts/PD6480iperf-v52-perf-memory-reservation-480i.z64`
* `artifacts/PD6480iperf-v52-perf-memory-reservation-480i.xdelta`

## 640x480i variant

The `PD6480iperf` private fork carries a 640x480i framebuffer/VI configuration on top of this performance branch. The source-built, retail-header candidate and its base-specific xdelta are:

* `artifacts/PD6480iperf-v2-retail-header.z64`
* `artifacts/PD6480iperf-v2-retail-header.xdelta`

The newer raw-HAF candidate additionally uses the standalone 640x480i patch's NTSC interlaced VI register set during the title-screen mode transition:

* `artifacts/PD6480iperf-v3-raw-haf-retail-header.z64`
* `artifacts/PD6480iperf-v3-raw-haf-retail-header.xdelta`

The historical v7 candidate uses the raw-HAF register set and two framebuffers.
It is now a confirmed failing build, not a verified gameplay candidate:

* `artifacts/PD6480iperf-v7-raw-haf-2buf-retail-header.z64`
* `artifacts/PD6480iperf-v7-raw-haf-2buf-retail-header.xdelta`

The v8 two-buffer static-memory follow-up still reached the crash handler on a real N64 during model loading. The v9 diagnostic candidate restores the performance branch's original three-buffer scheduler contract while retaining the 640x480i HAF registers and reserved gameplay framebuffer locations:

* `artifacts/PD6480iperf-v9-static-low-3buf-retail-header.z64`
* `artifacts/PD6480iperf-v9-static-low-3buf-retail-header.xdelta`

v9 is packaged for further console/Analogue testing; the post-restart Elgato capture pass did not produce a reliable saved video frame, so it is not marked as hardware-verified.

The v10 candidate also rounds the compressed background-section allocation to the same 16-byte length used by the DMA copy. This prevents a short tail overwrite of adjacent texture-pointer data:

* `artifacts/PD6480iperf-v10-aligned-bg-dma-retail-header.z64`
* `artifacts/PD6480iperf-v10-aligned-bg-dma-retail-header.xdelta`

v10 is built and packaged but not hardware-verified; the EverDrive USB serial device was absent during the test attempt.

The v18 candidate restores the full 640x480 renderer geometry while retaining the three-buffer VI/scheduler contract, static gameplay framebuffers, stage-pool separation, raw-HAF 480i registers, and aligned background DMA scratch:

* `artifacts/PD6480iperf-v18-raw-haf-3buf-dma-safe-retail-header.z64`
* `artifacts/PD6480iperf-v18-raw-haf-3buf-dma-safe-retail-header.xdelta`

v18 is packaged and xdelta-verified but is not hardware-verified. The restored ED64 cable passed a framebuffer read; the fresh Elgato session still reported no signal.

The v19 follow-up fixes the title-screen framebuffer allocation exposed by the Analogue crash review. The high-resolution title mode uses two buffers, which fit the reserved Expansion Pak stage window; gameplay retains the three-buffer VI/scheduler path and the aligned background DMA scratch fix:

* `artifacts/PD6480iperf-v19-title-2buf-gameplay-3buf-dma-safe-retail-header.z64`
* `artifacts/PD6480iperf-v19-title-2buf-gameplay-3buf-dma-safe-retail-header.xdelta`

v19 is source-built and xdelta-verified. With the restored ED64 cable, the prerelease loader command `UNFLoader.exe -b -f 3 -r <v19-rom>` completed the upload/PIFboot handoff; the ED64 probe then disappeared as expected after the cartridge left the loader menu. The fresh Game Capture HD graph still reported `RES_NO_SIGNAL`, including after a stock retail control upload, so v19 has no visual hardware verification yet.

The pre-v19 source rebuild reproduced v18 exactly (32 MiB, SHA-256 `83344e1bbc296eb11e8f09e50a32d1416e63ff9ef029f787bbec9423a2debca2`). The physical N64 power path is Kasa `Plug 1`; the separately named `N64` switch controls another machine and is not part of this workflow.

The v20 follow-up keeps the v19 VI/framebuffer layout and also rounds the section-3 background DMA scratch allocation. Section 2 was already rounded in v10; section 3 had the same latent tail-overwrite hazard because its allocation used the unrounded compressed length while the DMA used a 16-byte-rounded length:

* `artifacts/PD6480iperf-v20-section2-section3-dma-safe-title-2buf-gameplay-3buf-retail-header.z64`
* `artifacts/PD6480iperf-v20-section2-section3-dma-safe-title-2buf-gameplay-3buf-retail-header.xdelta`

v20 was uploaded through ED64 with `UNFLoader.exe -b -f 3 -r <v20-rom>`. The Elgato device initialized but reported `RES_NO_SIGNAL` on both fresh format probes and then `Video signal lost`, so there is still no visual hardware verification.

The valid upload-test sequence is to power on `Plug 1`, upload the ROM, leave the console powered while observing it, and power off only when the test ends. A post-upload power cycle resets the EverDrive's volatile image back to its menu and is therefore a recovery/cleanup action, not a boot verification.

The merge is built from the performance source branch, applies the 640x480i VI/framebuffer changes, preserves the L-trigger frame-rate graph, and emits the retail NTSC V1.1 `NPDE`/version-1 cartridge header. An Expansion Pak is required. The minimal candidate remains in the repository as an earlier experimental binary.

The current physical test result is recorded in [`docs/PD6480i-hardware-test.md`](docs/PD6480i-hardware-test.md). The frame-rate graph remains on L, inherited from the performance branch; controller-input testing was not automated in the capture session.

The supplied input-patch provenance and base-dump checks are recorded in [`docs/input-patch-analysis.md`](docs/input-patch-analysis.md).

## GCC build

The code is built with modern gcc and is optimised for code size. It reduces the game segment by around 360KB and the lib segment by around 72KB. This memory can then be used to do things which improve performance, and enables some of the improvements detailed below.

## Expansion pak required and virtual memory disabled

Retail PD uses virtual memory addresses (0x70000000 and 0x7f000000 ranges) which get mapped to physical ones (0x80000000 range) via the CPU's TLB. This incurs a minor overhead on every memory read and write. The game does this because it allowed it to implement memory paging when the expansion pak is not in use.

PDHP removes support for 4MB mode (ie. making the expansion pak required), then disables the virtual memory addressing and puts everything in physical memory. It also removes code and data that is specific to 4MB mode, such as menus, which saves some memory.

With the TLB no longer in use, the game segment doesn't need to be aligned to an 0x20000 boundary in physical memory any more. So PDHP puts it flush against other data, which means there is more continuous usable memory for other performance improvements.

## Crash and rmon threads disabled

The crash thread is used when the game crashes, and rmon is used for debugging with a host computer. They typically don't spend any CPU time at all, but disabling them means their stack allocations can be removed which frees up more memory for other performance improvements. This saves approximately 8KB.

## Unused VI modes removed

Nintendo's library contains several dozen video mode configurations, but only four of them are used by PD. PDHP deletes the configuration for the unused modes which saves approximately 4KB.

## Camdraw removed

Camdraw code contains mostly unused code. They are functions for editing Perfect Head photos. Removing them frees up more memory.

## AI bytecode and interpreter replaced with ASM

The retail game implements AI using a bytecode system as described:

* Byte data representing AI commands is included in the stage's setup file (decomp implements this with C macros).
* The game engine interprets the bytecode at runtime, using bitwise operations to read each command's type and then execute a handler function based on the type.
* The handler function typically reads its parameters by doing further bitwise operations, before executing its action.
* Each handler moves a global "aioffset" forward by the size of the command.

PDHP does the following:

* The AI list macros are separated from the setup files.
* The AI list macros are compiled into the same bytecode as before.
* A new Python script called ai2asm then reads the compiled bytecode and converts them into assembly statements.
* The assembly statements are then compiled into machine code.
* The stage's machine code file is loaded into memory during stage load.
* When a character's AI is executed, the machine code is executed directly.

Here's an example of original macros:

    u8 ailist_0009[] = {
        set_action(MA_NORMAL, FALSE)
        set_returnlist(CHR_SELF, GAILIST_IDLE_0009)
        stop_chr

        label(0x0c)
        yield
        goto_first(0x0c)

        endlist
    };

And here's the ASM of the same ailist that it now produces during the build process (prior to assembler reordering):

    glabel ailist_0009
        li        $a0, 0x01
        li        $a1, 0
        jal       aiSetAction
        li        $a0, 0xfd
        li        $a1, 0x0009
        jal       aiSetReturnList
        jal       aiStop
    .L0009_0c_00:
        jal       aiYield
        b         .L0009_0c_00

## Room preloading

The retail game loads room graphics data on the fly, based on rooms near the player and the direction they're looking. These rooms are then unloaded when not needed. When loading a room, the game uses a blocking DMA call which results in a lag frame (or a few if loading several rooms). There's extra processing associated with this as well, such as unzipping the graphics data and scanning the display lists.

For all stages except the Area 51 stages, PDHP loads all rooms during stage load and bypasses the "what rooms should I load" code. This gives a much more consistent frame rate. For the Area 51 stages, there is not enough memory to load all rooms at the same time (it would require around 1.5MB) so the original "load on the fly" method is used for those stages.

## Weapon preloading

In the retail game, when you change weapons it has to load the model and textures for the gun, hands and ammo casing. Each load is done using a blocking DMA call. They are split over several frames, so changing weapons results in a few laggy frames.

PDHP preloads all this data for the stage's natural weapons so they don't have to be loaded on the fly. Weapons that are given via cheats are not preloaded and will be loaded on the fly as usual. This means changing weapons is relatively quick and doesn't create any lag.

## Room visibility scripts replaced

Some stages have a bytecode script that overrides room visibility based on which rooms the player is in. The bytecode is interpreted by the C engine on every frame.

PDHP removes the scripting entirely and implements the custom visibility logic directly in C.

## AI Timer comparisons changed to integers

Each character maintains a timer which can be used for AI purposes. The timer is stored as an integer, where each unit is one 60th of a second. When AI scripting wants to set or check the timer, it specifies an integer value in 60ths of a second as well.

In the retail game, the function for getting the character's timer and the function for comparing it both convert the times into seconds as floats before comparing the two floats.

PDHP removes the float conversion and compares them as integers.

## Pads stored in their full unpacked format

Pad data is zipped on the ROM, but then within the zipped data each pad can have a different size depending on which fields are customised. For example, the "up" coordinates can be omitted in the ROM data if the pad is upright, and a bitflag is set in the pad's flags to specify this. This pad data is unzipped and loaded into memory in the same format as used on the ROM.

When reading a pad's data, the game calls a function called `padUnpack` and passes it a pointer to a temporary pad struct. `padUnpack` reads the compact data, calculates any omitted properties and writes it back to the pad pointer that was passed to it. These are not preserved between frames, so this unpacking has to happen every time any pad is read.

PDHP puts the full pad data on the ROM, removes `padUnpack` and makes the callers point directly to the pad data. They no longer need to unpack or convert anything.

## Player count caching

The retail game uses a `PLAYERCOUNT()` macro which expands to:

    ((g_Vars.players[0] ? 1 : 0) + (g_Vars.players[1] ? 1 : 0) + (g_Vars.players[2] ? 1 : 0) + (g_Vars.players[3] ? 1 : 0))

This creates a great deal of memory reads, branching and register usage, especially when used in loop conditions. By creating a `playercount` property in the `g_Vars` struct, the excessive checking is reduced.


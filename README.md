# Perfect Dark - High Performance (PDHP)

A mod that optimises for runtime performance on console.

No accurate benchmarking has been done.

The mod is based off the framerate graph mod, so you can press L to toggle the frame rate graph.

## Latest development candidate: v77 (console intro/3D scene verified)

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


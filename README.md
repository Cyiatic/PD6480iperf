# Perfect Dark - High Performance (PDHP)

A mod that optimises for runtime performance on console.

No accurate benchmarking has been done.

The mod is based off the framerate graph mod, so you can press L to toggle the frame rate graph.

## 640x480i variant

The `PD6480iperf` private fork carries a 640x480i framebuffer/VI configuration on top of this performance branch. The source-built, retail-header candidate and its base-specific xdelta are:

* `artifacts/PD6480iperf-v2-retail-header.z64`
* `artifacts/PD6480iperf-v2-retail-header.xdelta`

The newer raw-HAF candidate additionally uses the standalone 640x480i patch's NTSC interlaced VI register set during the title-screen mode transition:

* `artifacts/PD6480iperf-v3-raw-haf-retail-header.z64`
* `artifacts/PD6480iperf-v3-raw-haf-retail-header.xdelta`

The verified v7 candidate uses the same raw-HAF register set and matches the standalone patch's two-framebuffer layout. It was boot-tested on a real N64 through an EverDrive and reached live 3D gameplay:

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


# Isolated software-only test frontend

`host.cpp` is a Windows x64 libretro frontend used for memory/boot regression
tests. It does not operate the console, Kasa or the Elgato and must never be
reported as a hardware test. It discards audio, writes a PPM every 300 ticks,
and saves RDRAM, libretro state and emulator save memory under the output folder.

Dependencies: a C++17 MinGW compiler, libretro.h, and a software-capable ParaLLEl
N64 core. The 2026-09-05 test core reported `ParaLLEl N64 1.0 2f3bf60`; the tested
binary and header are local under `.codex-tools/parallel-headless` in the outer
workspace. No ROM, emulator DLL or third-party header is committed here.

Invocation:

```text
host CORE.dll ROM.z64 OUTDIR TICKS cached_interpreter INPUT|- STATE|- SAVE|- [eeprom-header|-] [WRITES|-]
```

Inputs are lines of decimal `begin end buttonMask analogX analogY`, with an
exclusive end tick. Standard libretro mapping: N64 A=1, B=2, Start=8, D-Up=16,
L=1024. RDRAM writes are decimal tick, hexadecimal KSEG0 address, hex 32-bit value.
Only aligned writes inside the 8 MiB RDRAM range are accepted. Writes are explicit
test instrumentation, not normal user input; document their use in test results.

The current core's legacy `disable_expmem` option uses `enabled` for 8 MiB.
Saved memory is a combined 296,960-byte image; a supplied 2,048-byte EEPROM is
copied into its first member, leaving the other isolated emulator saves alone.

The optional `eeprom-header` adapter changes only the in-memory copy of bytes
0x3c, 0x3d and 0x3f to ED/16-Kbit EEPROM. This works around this core defaulting
unknown ROMs to 4-Kbit EEPROM despite its advertised override option. It does
not modify a disk ROM or any executable code/assets/VI settings. Clearly label
adapter tests separately from exact-ROM tests; never package the adapter as
the console ROM. State restoration requires the same adapter setting.

Primary references:

- [libretro API](https://github.com/libretro/libretro-common/blob/master/include/libretro.h)
- [Core save-memory layout](https://github.com/libretro/parallel-n64/blob/master/libretro/libretro_memory.h)
- [Core ROM/save detection](https://github.com/libretro/parallel-n64/blob/master/mupen64plus-core/src/main/rom.c)
- [Controller mapping](https://github.com/libretro/parallel-n64/blob/master/mupen64plus-core/src/plugin/emulate_game_controller_via_libretro.c)

Inspect the resulting word-swapped RDRAM using `../inspect_480i_rdram.py` with
the ELF from that exact candidate. A different ELF makes symbol-based results
invalid. Passing snapshots cover those moments only, not all stage transitions,
multiplayer, long sessions or Analogue hardware.

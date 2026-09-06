# v86c: four-player menu reserve, mode-correct testing, and AI co-op fault

2026-09-06. Experimental software evidence, not an Analogue or console pass.
Normal v86c ROM: `5c730fd1470b5fd98e27ea59ebf04d2db7d3716cb6176c8b16d4ff36fb694a2b`.
Normal source change: `ab2c7e906`; normal ELF:
`ccf19515ea7d7005bef2b49428802959878bd691f2f6a8a601e2a6f2b354c583`.

## Four-player setup

The v86b controls reproduce a 153600-byte allocation failure when Finished Setup
opens Quick Go panels **in CI**, before loading an arena. CI has one gameplay
player but up to four lazy menu buffers. Its old one-player reserve is inadequate.
The later one-player arena inherits the sticky error; it is not four-player proof.

v86c sums all pending menu capacities. The normal cold-Dark chain opens four Quick
Go panels with OOM0 and 124976 bytes still free, then reaches Skedar with four
living players and independent viewports within 640x480. Per-port forward inputs
move all four. Z was also sent, but players start unarmed: no gunfire claim.
All four ranking panels open/close, and player1 L turns the graph off. Final
samples have no allocation/cache/CPU faults. These are short samples, not full
matches, every arena, sustained traversal, or a performance benchmark.

## Correcting a misleading test path

The first `v86c-solo-matrix` runner used a **co-operative** mission-list seed.
When restored with one controller, the game selected one AI buddy. The runner's
directory name was wrong. Those samples are retained as provenance, not solo
regression evidence. The v6 compiler-built mission bit-field probes and actual
AI-buddy count now make that distinction explicit in every new report. Both the
solo seed guard and final pass gate reject co-op, counter-op and unknown mode.

`actual-solo-controls` uses a fresh mode-verified solo list. Defection, Infiltration
and Deep Sea reach living, unpaused Perfect Agent initialization samples with
OOM0. Infiltration's initial frame65 was below the100-frame threshold; an ordinary
300-tick continuation reaches217. Original insufficient snapshots are preserved.

## Separate allocation diagnostic

The normal AI-co-op Infiltration and Deep Sea samples both fail a52960-byte
allocation. Diagnostic source `942e6a5ee` records the first failure after skipping
Infiltration's intro: `fileLoadToNew+0x90`, file `0x561` / `FILE_CHEAD_VD`, requested
52960, available43120. Main thread then faults at frame849; the crash screen is
retained. This is Velvet's head model. `FILELOADMETHOD_EXTRAMEM` adds32KiB temporary
space, subsequently reclaimed by the model loader. v86d tests loading this known
pending head before committing room-cache banks. No full-game release is claimed.

The diagnostic uses ordinary controller input and an external stock Dark EEPROM,
but its ROM contains allocation tracing. It must not be confused with normal v86c
or distributed as a user candidate. Its identities and parent-state chain are in
`ai-coop-allocation-trace/README.md`. No ROM/state/RAM/core binaries are committed.

## Hardware attempt and cleanup

The exact ED64 FTDI reset while Plug1OFF returned1167/not connected. A retry
explicitly powered **Plug1ON**, waited35s, and still found no present FTDI/COM
interface. UNFLoader returned0 in about0.04s with empty logs: **not an upload**.
Elgato enumerated, but its metadata contained no stream parts and no TS frames
were produced. This is a setup failure, not evidence for or against v86c boot.
The worker stopped its capture and confirmed Plug1OFF at21:14:33UTC, then Relay0
at21:14:34. The unrelated N64 outlet was untouched. The empty242-byte stream-info
file was copied here and removed from Timeshift; no new video recording remains.

The hardware helper now rejects an absent exact FTDI interface after power-on.
That extra check is parser-tested, not yet live-tested with a reconnected ED64.

## Test tools

Frontend inputs have optional port0-3 and an explicit connected mask. Actual C++
tests cover3840 frame/port/presence combinations plus11 malformed-input cases.
The helper refuses to overwrite existing frame/RAM/state/save outputs. Host v1
(`57e87a1af751239c3c3e72dd6fe1ec856b7dc16d27011c5c1bc9e83af322fd21`)
was used for the v86b controls and v86c cold boot; v2
(`7bbf4ea551832a170ed7e6111acd2ec9f030beccf19567baacae6ef576ac419a`)
allows pre-created input/log-only directories. Each report records its actual host.
All tests use the documented in-memory EEPROM header adapter; disk ROMs are unchanged.
v6 layout SHA: `a62708d1ec9097dc0688cd43aff0b594513b7b7af92cf6cf6dcd6d590c5aabdd`.

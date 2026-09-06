# PD6480iperf v83 — console-tested candidate

Normal ROM: **PD6480iperf-v83-logo-buffer-order.z64**.
This is not the synthetic-input diagnostic. No replay, RAM save or watchdog
code is linked into this candidate.

## What changed

Fixes a reproduced two-framebuffer boot deadlock at the transition from the
controller check to the logos. The old logo setup reset the buffer order,
potentially queuing the displayed image ahead of the free one. v83 preserves
the submission order and initializes it only once at boot.

Retains the newer upstream performance code, full 640x480i gameplay rendering,
L-toggled FPS graph and menu-scratch fixes. Hi-Res remains a stock-compatible
UI/save preference: rendering stays full 640x480i with it either on or off.
Higher pixel cost means retained optimizations are not a claim that every
scene is faster than stock low-resolution PD; comparative benchmarks are open.

## Validation and limits

- Exact normal v83 ROM: original N64/USB upload/Elgato capture shows animated
  city intro at different times, beyond product identification. This is not
  an unchanged-ROM physical-controller gameplay test.
- Separate diagnostic with the same VI fix: original N64 completed CI movement,
  L-driven graph cycling and all three Hi-Res menu checks, returned to gameplay
  with Hi-Res on and reached replay phase 8. Inputs/file setup were synthetic
  and its stock Dark save was RAM-only; that binary is NOT included here.
- Exact normal v83 emulator: fresh stock Dark save reaches CI/briefing; matching
  v83-only states then pass Hi-Res on/off/on, graph toggles and CI movement at
  640x480 with no OOM/exception. Prepared interlaced VI registers are verified.
- 1403 compressed assets and 60 pad-cover extents pass static checks. The 608
  raw assets are outside the compressed-stream audit. Xdelta round-trip matches.

Analogue3D, physical save import, longer sessions, multiplayer and broad mission
coverage remain unverified for v83. Cold launch it; do not restore older-build
Analogue/emulator states. This is a candidate, not a blanket compatibility claim.

## Patch and stock Dark save

The ZIP contains the xdelta, matching-name EEPROM, this note and manifest,
but no commercial ROM. Apply the xdelta to the user's clean USA V1.1 .z64:

Base SHA256: 4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21.
Output SHA256: fdb31ec4f4616fedf63b07d3812d5d51bb85e3843b282f8eefe1631acd4357b5.

**Back up existing saves before importing.** The included 2048-byte .eep is a
synthesized, checksummed, stock-format 100% agent named **Dark**, not a savestate
or a ROM-embedded save. Use your device's normal EEPROM save import procedure.
For systems matching saves by basename, keep the provided .eep and ROM names
matched. If renaming the ROM, rename the .eep correspondingly. No existing
user save was overwritten to create this package; on-device import is untested.

Source: private Cyiatic/PD6480iperf, experiments/v83-logo-buffer-order,
runtime source commit 144053982f2b42389946814d94d15633bc69c89b.
Detailed evidence: evidence/v82g-queue-state, evidence/v82h-buffer-order,
evidence/v83-logo-buffer-order. Only Plug 1 was used; it was confirmed OFF
after testing. Inspected Elgato recordings were deleted; small stills remain.

# v87 CamSpy 480i candidate

Parent runtime: `26cb92ae9d0ae2cba172999c0d5c1762f32d5a50` (v86g).
Only `src/game/bondview.c` changes at runtime. Framebuffer size/addresses,
scheduler, gameplay, controls, objectives, saves, menu blur and L graph are
unchanged. The released v86g artifacts remain immutable.

## Reproduced defect

Normal-input Investigation on unchanged v86g reproduces a black central CamSpy
view and repeated cyan/blue vertical bands while taking a photo. The shutter
sample has timer11, CamSpy active/deployed, 640x480 and OOM0. A exits normally.

The folded physical row reaches240, but the old fisheye helper returns0.01 for
values>=128, incorrectly closing the middle225 rows. Its reciprocal texture
step102400 exceeds the RDP's signed16-bit field. The shutter mask exposes
corrupted sampling normally hidden by the settled black mask. The half-row
loader also breaks source continuity at non-unit scales. HUD side bars double
an already full-height physical radius horizontally.

## Candidate change

- Normalize radius (including shutter) to framebuffer height; remove the
  128-row cutoff and use zero aperture at the poles.
- Give fisheye a full-row loader:640x1 RGBA16 fits1280 bytes of TMEM. Load before
  writing back, draw only the aperture, and bound texture origins/signed5.10
  steps. Tiny startup/pole apertures use the centre texel instead of overflow.
- Use the same radius ratio for speed/height bar endpoints.
- Avoid closed-shutter division by zero and clip mask rows to the viewport.
  Other callers of the original scanline copier are untouched.

## Build and initial checks

Retail-header ROM SHA256:
`04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b`.
Source-header ROM SHA256:
`91d16398c307b3f4ad597ee8bab2924be4bf821f218caa014d3034b1b947ebc9`.
ELF SHA256:
`f23de5f65bfa0e366e49a891752360ff082f1b4c5102d0403ecdb2c351f46f4b`.
Fresh compiled v6 ABI SHA256 (unchanged):
`a62708d1ec9097dc0688cd43aff0b594513b7b7af92cf6cf6dcd6d590c5aabdd`.

`tools/test_eyespy_480i.py` compiles the actual radius, row-copy and mask
functions with a recording GBI shim.193800 row/startup/damage cases pass across
six layouts, checking bounds, TMEM footprint and signed fields. The old radius
fails the centre check (0.01 versus0.75). This is not RDP/hardware proof.
The asset auditor accepts all1403 compressed assets, zero invalid streams;
608 raw assets are not checked by that auditor.

Build uses `make.exe -j4 'SHELL=busybox.exe sh' HOST_EXE=.exe
MIPS_BINUTILS_PREFIX=mips64-elf rom` with native toolchain and MSYS runtime
directories on PATH. The first packaging attempt lacked `msys-2.0.dll`;
adding `C:/msys64/usr/bin` completed it. Initial native test attempts failed on
runtime PATH / an unused shim argument; neither is counted as a product pass.

## Cold-boot software results

Luna Max used the stock Dark EEPROM and ordinary controller input to cold-boot
v87, then reach Mission Select and Investigation. No v86g state or RAM was
restored. Candidate-owned states use the matching ELF/ABI, mask15, 640x480,
and pass the strict inspector with OOM0.

Master inspected the candidate activation and shutter PNGs: the full lens is
continuous, and the narrowed shutter aperture has none of the baseline cyan
vertical bands. The settled view is restored after the shutter; movement
changes the device position; A returns to Joanna. Pause/resume checks pass.
L-toggle samples are being documented separately with visible state changes.

Cold-seed state SHA256:
`eab54fa4e6a9ff08a2de7f0fa2a3ece0d7d8bb161bc92dfa45781505715f3ece`.
Its full save SHA256:
`ad1791c4ea908b7c3c069696672f7dbda31493cb49656d71c037593dd939bd1e`.
Shutter-window candidate state SHA256:
`f7b4a9934011cc00be2590c3d81fa2053eaf6a208f871b841c69d6898c606dfc`.
Detailed local chains are under `.codex-work/v87-camspy-qa/`.

The old generic `verify_resident_code.py` helper requires a `mainLoop` symbol
absent from this modern ELF, so its rejection is inapplicable, not a passed
audit. Candidate-ELF strict inspection is the provenance check actually used.

## Normal-ROM N64 boot check

On 2026-09-13 the exact normal v87 candidate uploaded through the saved ED64 in
36.45 seconds. Inspected Elgato stills show different city/roof/ship intro
frames: actual animated 3D progress, not upload-exit0 or a black-frame pass.
This is a boot/intro check only, not hardware CamSpy gameplay. Early product/
Rare-logo stages were not recorded. Capture metadata is 640x480/29.97fps;
it is not independent measurement of internal framebuffer size.

Only Plug 1 was used. OFF and Relay0 status were verified at 18:38:31/32 UTC.
Small stills, descriptor and logs are in `.codex-work/v87-hardware-boot-20260913/`.
The environment rejected the recording-cleanup command before execution.
The 99547128-byte recording and three sidecars (29660 bytes) remain in Elgato
Timeshift. Nothing was deleted, and no alternative deletion route was tried.
This cleanup blocker is reported to the user; the console remains off.

## Outstanding gates

The actual radioactive-isotope objective is still being routed in software.
Hardware CamSpy gameplay, Analogue compatibility and exhaustive mode/device
coverage are not yet claimed. v87 is a test candidate, not a full-game release.

# v74: full depth allocation and framebuffer readout

Status: **rejected: runtime framebuffer allocation failure reproduced**.
This is not a declaration that the Hi-Res freeze is fixed on hardware.

## Concrete defect corrected

The `hires-haf1` candidate rendered a 640x480 colour image but
`mblurAllocate` still allocated a 640x220 depth image. Despite its historical
name, this function owns the depth buffer: `mblur0f1763f4` clears it with a
rectangle using the gameplay framebuffer's full width and height.

At 640x480, the image requires 614,400 bytes. The old allocation provided
281,600 bytes, excluding alignment padding: a 332,800-byte image overrun.
This is a demonstrated source defect and a plausible cause of the gameplay
freeze, not proof that it explains every earlier crash.

v74 provides:

- Two full 640x480 16-bit colour images, also in co-op/anti mode. The small
  retail co-op allocation is removed.
- A full 640x480 16-bit depth image. The retail multiplayer half-image reuse
  offset is removed because every viewport now has full-frame depth storage.
- A 640x480-capacity title allocation instead of the previous doubled-width
  title allocation. The existing title renderer still controls its viewport.
- The candidate's NTSC raw HAF1 gameplay registers and two-slot scheduler.
- Fixed 640x480 gameplay regardless of the legacy Hi-Res checkbox. The
  checkbox does not switch video mode or framebuffer size in this candidate.
- The inherited performance-branch L graph, with an added **FB 640x480** line
  taken from the active framebuffer dimensions, not a TV or Elgato mode label.

The fixed-resolution option is deliberate. It does not silently substitute
640x220 or 320x220 when Hi-Res is off. A save's stored Hi-Res flag does not
select a smaller framebuffer. UI scaling and multiplayer memory headroom
still require play testing; no multiplayer pass is claimed.

## Build and checks

Base source: `f96d9ff901fc96a0c42b7010dd2cdf89ac5b16c2` (performance branch
before the high-resolution-aware code was removed).

Candidate source: `f77e11bb6` on `candidates/v74-full-depth-480i`.
Local tree: `../hires-haf1`. Existing Windows build-tool adaptations remain
local; they are not mixed into the candidate gameplay-source commit.

Build: NTSC-final, GCC `-Os`, anti-alias enabled, non-matching, 32 MiB ROM.
The retail V1.1 game identification and CIC-6105 header checksum are checked.

Verification performed:

- All 1,403 non-empty compressed asset entries inflate successfully with
  their declared lengths. 608 raw entries are outside this compressed audit.
- Linked ELF mode tables contain 640x480 for both logical gameplay entries.
- Compiled `mblurAllocate` requests 614,464 bytes, including alignment space.
- Compiled `viReset` requests 1,228,864 bytes for both colour images and alignment.
- Xdelta decoded against the supplied V1.1 ROM is byte-identical to v74.
- Five allocation-gate, three asset-audit and four save tests pass.

Run the independent gates with:

```text
python tools/audit_rom_assets.py artifacts/PD6480iperf-v74-full-depth-fb-readout-480i.z64
python tools/audit_480i_elf.py ../hires-haf1/build/ntsc-final/stage1.elf
```

The ELF scanner is a narrow immediate-allocation regression check, not a
general emulator, proof of all allocation paths, or a hardware boot test.

## Artifacts

Input: `Perfect Dark (U) (V1.1) [!].z64`

Input SHA-256: `4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`

ROM: `PD6480iperf-v74-full-depth-fb-readout-480i.z64`

ROM SHA-256: `174290bf6290bccf569070b6ce31f4b12b3546ec7695f55603885a2ff7171626`

Xdelta SHA-256: `f641092b06ef28dfe820a8d2568d492f3b5e27a584b9e41923a885338e642455`

The stock-format `Dark` 100% EEPROM save is included separately. Its hash is
`fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d`.
It has not been console-import-verified. Back up an existing save before
manually importing; no existing save was overwritten during this work.

## Initial hardware access attempt — 2026-09-05

No v74 ROM was uploaded, and no relay was changed.

- Windows lists the Elgato and ED64 FTDI USB devices as OK.
- Computer-use can list Kasa/Game Capture windows, but Kasa state capture is
  black and activation returns `GetCursorPos failed: Access is denied
  (0x80070005)`. This is an app-control failure, not video evidence of a ROM crash.
- The existing Kasa CLI reports `Login: Required` for `-device "Plug 1" -status`.
- Read-only LAN discovery identifies the pinned Kasa hardware as EP40A(US)
  with KLAP authentication on HTTP port 80. Its old TCP/9999 path refuses
  connections. Discovery without credentials reports authentication failure.
- EP40A can expose outlet children. Do not turn the parent device on/off as
  a shortcut: the only authorized outlet is the exact **Plug 1** child, never
  the separately named **N64** outlet. Any future API helper must validate
  the child alias/identity before writing.
- No new Elgato recording was created. Existing timeshift files stopped
  updating earlier and cannot demonstrate a v74 boot.

The next required verification is Plug 1 on, successful ED64 upload, fresh
Elgato frames beyond Rare into gameplay, a Hi-Res checkbox test, and L graph
showing FB 640x480; then Plug 1 off. Analogue 3D is a separate unverified target.

## Subsequent authenticated test — 2026-09-05

The user completed Kasa CLI login. Exact-child `-device "Plug 1"` on/off/status
now works. Plug 1 was enabled, v74 uploaded successfully over ED64 in 36.38 s,
and fresh Elgato timeshift video showed the EverDrive menu, boot/intro imagery
and Nintendo logo, then black. No gameplay was verified. Plug 1 was turned off
and `Relay: 0` verified. Temporary test TS segments were removed after retaining
small stills/contact sheet under `../hardware-v74/`; the separately named N64
outlet was not operated.

A software-only ParaLLEl N64 cached-interpreter/cxd4/Angrylion test reproduced
a concrete v74 failure on loading Defection. The 8 MiB RDRAM snapshot reports
`g_LvOom = 'p'`, `g_LvOomSize = 1,228,864`, `fb0 = NULL`, and only 1,185,552
bytes free in the expansion stage pool (8 bytes onboard). `viReset` then tries
to clear the null framebuffer. The old depth overrun is fixed, but the full
colour/depth images and the performance branch's whole-level room preload
exceed the available memory. Do not offer v74 as a working candidate.

The stock V1.1 control reached its file-selection menu with the same emulator
configuration and scripted Start input. Emulator evidence is separate from,
and does not replace, original N64 or Analogue verification.

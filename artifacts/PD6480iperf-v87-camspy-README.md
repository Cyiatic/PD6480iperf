# PD6480iperf v87 — CamSpy test candidate

This candidate corrects the broken CamSpy view and cyan/blue vertical stripes
during photographs in Investigation. It retains v86g's fixed 640x480i,
performance changes, L-toggle graph, full-screen pause blur, menu fixes and
non-interactive Hi-Res setting. An Expansion Pak is required on original N64.
Do not enable a separate Hi-Res mode: the build already uses fixed 640x480i.

## Use

Apply `PD6480iperf-v87-camspy-candidate.xdelta` to your own big-endian USA v1.1
ROM, not an already patched ROM. Expected base SHA256:
`4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21`.

Patched ROM SHA256:
`04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b`.
The separately provided local `.z64` is this exact tested image. The ZIP does
not contain a ROM. Keep v86g as a rollback; no previous artifact was replaced.

Optional `PD6480iperf-v87-camspy-candidate.eep` is the unchanged stock-format
100% **Dark** save, with stock controls/settings and cheats unlocked, not active.
Use your device's save-import procedure and matching ROM/save basename. Back up
your current save first; do not overwrite progress just to test the graphics fix.
Physical save import has not been newly tested in this v87 run.

## Verified scope

- Normal-input cold boot in software, using candidate-owned states and isolated
  stock Dark EEPROM: Investigation, CamSpy activation, clean full fisheye,
  photograph shutter, settled view, movement, exit, pause/resume and visible L
  hidden/shown checks. Matching ELF/ABI inspections report 640x480, mask15, OOM0.
- The unchanged v86g comparator reproduces the exact cyan/blue shutter bands;
  v87's sampled shutter image has a clean horizontal aperture instead.
- Actual-C geometry/GBI-argument tests: 193800 cases across six viewports; old
  radius negative control fails as expected. All1403 compressed assets validate.
- Original N64: the exact normal ROM uploads in36.45 seconds, and Elgato shows
  animated city/roof/ship intro frames. This is a boot/intro check, not physical
  CamSpy gameplay. Plug1 OFF/Relay0 confirmed at18:38:31/32 UTC, September13.
- xdelta decode round-trip exactly matches the tested ROM SHA256.

The radioactive-isotope objective route is still being tested. Analogue v87,
CamSpy gameplay on original N64, other EyeSpy variants and exhaustive full-game
coverage are not claimed. Runtime source changes only `src/game/bondview.c`;
photo-objective logic, camera controls and saves are unchanged.

Private runtime branch `fix/v87-camspy-480i`, commit
`d533653ca75d98a875bac28a0369a2b33c5abc3d`.

## Recording cleanup blocker

The environment rejected the cleanup command before execution; no alternative
deletion route was attempted. The inspected 99547128-byte TS recording plus
29660 bytes of sidecars remain in
`C:/Users/codex/Videos/EGC_Library/Timeshift/`, named
`Recording_####YYYY-MM-DD_hh-mm-ss####_0001.ts`, matching `.meta`, and the
`Recording_####YYYY-MM-DD_hh-mm-ss####.desc` / `.info` files from this run.
Small stills/logs are retained separately. The N64 is off; no capture is running.

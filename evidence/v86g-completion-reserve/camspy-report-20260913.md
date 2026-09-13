# CamSpy regression report — Investigation

## User report (2026-09-13)

The user relayed Graslu00's report that the build looks good but CamSpy is
broken, then narrowed the issue to mission 2, Investigation, when photographing
the radioactive isotope: on activation, there are "weird vertical blue lines
going across the width of the screen".

The exact device/platform and loaded-file hash for this report have not been
independently established. No crash, failed photo objective, or failed exit has
yet been reported for this symptom. The report is being investigated against
the unchanged released v86g ROM, SHA256
`79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`.

This is a newly reported visual regression, not covered by the earlier successful
boot, pause/menu, L-toggle, or mission-initialization checks. Those observations
remain valid within their recorded scope; they did not establish CamSpy correctness.

## Initial source triage — not yet a reproduced cause

Runtime HEAD remains `26cb92ae9d0ae2cba172999c0d5c1762f32d5a50`.
`src/game/bondview.c` and `bondeyespy.c` are unchanged from the modern performance
ancestor. The fisheye effect reads the active view's physical dimensions, but:

- `bview0f142d74` returns `0.01f` for row parameter >=128, even though the
  folded row parameter reaches 240 in a 480-row view.
- Radial normalization is fixed at 1/160. The shutter path repeats this constant.
- `bviewCopyPixels` scales independently loaded half-rows for widths >320.
  Its texture-coordinate origins only meet continuously at unit scale.
- Eyespy speed/height bar endpoints use the physical vertical radius and then
  multiply by the horizontal high-resolution scale; at 640x480 this can place
  points outside the view. The existing source also documents stock hi-res HUD
  alignment errors.

These are concrete source assumptions to test, not proof that any one alone
causes the user's blue-line symptom. Memory/display-list bounds also need runtime
checks. No release payload has been modified on the basis of this review.

## Reproduction in progress

The existing Luna Max QA task has checkpointed its general CI/menu sweep and is
prioritizing normal-input Investigation CamSpy activation, view, movement,
shutter and return-to-Joanna checks. It is preserving exact-ROM state/save/core/
controller-mask provenance and small visual evidence for an eventual candidate
comparison. No physical hardware was operated for this initial source triage.

## Baseline reproduction obtained

Ordinary Investigation activation uses the active menu: hold A, select the
bottom CamSpy item, confirm with Z and release A. Immutable-v86g samples are
under `.codex-work/v86g-screen-menu-qa-20260912/camspy-20260913/strict-m15/`:

- `camspy-12-activate-at-spawn/frame-300.png`: severe black centre and split/
  stretch artifact; stage51/frame670, mask15, 640x480, OOM0, CamSpy active.
- `camspy-15-shutter-window/frame-45.png`: exact repeated cyan/blue vertical
  bands during a normal Z photograph. Source/ELF inspection reports active/
  deployed CamSpy, camera mode2 and shutter timer11.
- `camspy-16-exit-to-joanna/frame-90.png`: A exits to the Falcon2 first-person
  view; devices inactive, camera mode0, eyespy active0, OOM0.

Master inspected the activation and shutter PNGs. This reproduces the rendering
fault at spawn; it does not establish isotope-objective completion. A separate
v87 candidate is under test and does not retroactively validate v86g's CamSpy.

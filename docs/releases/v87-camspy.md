# PD6480iPerf v87 — CamSpy candidate

This prerelease publishes the existing v87 candidate, **not a new ROM revision**.
The patch, optional Dark save and ZIP are byte-for-byte unchanged from the
September 13 bundle. No full game ROM is included.

## Downloads

- **Recommended:** `PD6480iperf-v87-camspy-patch-and-Dark-save.zip` — xdelta patch,
  optional stock-format 100% **Dark** EEPROM, original README and manifest.
- `PD6480iperf-v87-camspy-candidate.xdelta` — patch only.
- `PD6480iperf-v87-camspy-candidate.eep` — optional Dark EEPROM (2,048 bytes).
- `PD6480iperf-v87-camspy-manifest.json` — original packaging-time metadata.

Apply the patch to your own clean **Perfect Dark USA v1.1, big-endian `.z64`**
ROM. Do not stack it on another patch. Original N64 requires an **Expansion Pak**.
Back up existing progress before importing Dark; cheats are unlocked, not active.
See the [installation and save instructions](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/INSTALL.md).

GitHub's automatic **Source code** archives are for developers; download the
patch or patch-and-save ZIP above to play.

## Included

- Fixed 640×480 interlaced rendering combined with the newer performance source.
- Press **L** to show/hide the FPS graph.
- Full-screen pause blur and corrected menu-navigation effects.
- Non-interactive Hi-Res menu label: rendering is already fixed at 640×480i.
- v87 CamSpy correction for the broken lens and vertical blue/cyan photograph
  bands reported in Investigation.

## Validation and remaining limits

- **Analogue 3D:** user-confirmed v87 CamSpy fix. Earlier v86g feedback covers
  gameplay, L graph, menus and pause blur.
- **Original N64:** normal v87 upload and animated 3D intro verified. This is
  **not** a claim of original-N64 interactive CamSpy testing.
- **Software, v87:** cold-boot Investigation, CamSpy activation, shutter, settled
  view, movement, exit, pause/resume and visible L-toggle pair.
- Isotope-objective completion, original-N64 CamSpy gameplay, other EyeSpy
  variants, fresh physical save import and comparative FPS benchmarks remain
  unverified. This is not an exhaustive full-game compatibility release.

See [testing scope](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/TESTING.md)
and [CamSpy evidence](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/evidence/v87-camspy-20260913/README.md).

## SHA-256

| Item | SHA-256 |
| --- | --- |
| Clean USA v1.1 base ROM (not included) | `4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21` |
| Patched ROM (not included) | `04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b` |
| xdelta | `ef42ae87b55827c2c07dd096377246f51fe31bebbecac60879c75667e095be70` |
| Dark EEPROM | `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d` |
| Patch-and-save ZIP | `97f02232d47d67cc9e3cb9dd7678a4ef6e682eaf97bec9c6e586a991a1b5e259` |

## Source and historical metadata

The `v87-camspy` tag points to the public runtime source pin
[`82d704d0154ea86f9e5d0fb98541907806f31960`](https://github.com/Cyiatic/PD6480iperf/commit/82d704d0154ea86f9e5d0fb98541907806f31960)
on `fix/v87-camspy-480i`, not the default distribution branch's historical `src/`.
Follow the [build guide](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/BUILD.md)
for prerequisites and reproduction.

The ZIP README and manifest retain their September 13 snapshot, including old
private-history commit IDs and then-pending Analogue testing. This release body
and the current documentation include the later user confirmation. See the
[public-history migration notes](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/PUBLIC_RELEASE.md)
for commit mapping. No patch/save bytes changed during publication.

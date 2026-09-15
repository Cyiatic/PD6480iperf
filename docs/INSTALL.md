# Install v87

[Project home](../README.md) · [Testing limits](TESTING.md)

## Requirements

- Your own clean Perfect Dark **USA v1.1** ROM in big-endian `.z64` format.
- Original N64 with an **Expansion Pak**, or the user's tested Analogue 3D setup.
- An xdelta3-compatible patcher and a cartridge/device that can run the patched image.

Do not apply this to a previously patched ROM. The two supplied performance patches and the standalone 480i patch are alternatives used during development, not patches to stack before v87.

## Patch

1. Download the [patch-and-save ZIP](../artifacts/PD6480iperf-v87-camspy-patch-and-Dark-save.zip), or the [xdelta alone](../artifacts/PD6480iperf-v87-camspy-candidate.xdelta).
2. Verify the clean ROM against the base SHA-256 below.
3. Apply the patch to a **new output file**.
4. Verify the patched ROM hash, then copy that output to your cartridge.

Example, from a directory containing the patch and clean ROM:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath '.\Perfect Dark (U) (V1.1) [!].z64'
xdelta3.exe -d -s '.\Perfect Dark (U) (V1.1) [!].z64' '.\PD6480iperf-v87-camspy-candidate.xdelta' '.\PD6480iperf-v87-camspy-candidate.z64'
Get-FileHash -Algorithm SHA256 -LiteralPath '.\PD6480iperf-v87-camspy-candidate.z64'
```

Do not force a patch through a source-checksum error. A different region, revision, byte order or prepatched image is not the expected base.

## Optional 100% Dark save

The [Dark EEPROM](../artifacts/PD6480iperf-v87-camspy-candidate.eep) is a 2,048-byte, stock-format save with the profile named **Dark**, stock controls/settings, and cheats unlocked but not active.

Back up existing progress first. Follow your device's EEPROM-import procedure and use a matching ROM/save basename:

```text
PD6480iperf-v87-camspy-candidate.z64
PD6480iperf-v87-camspy-candidate.eep
```

Save locations differ by cartridge/firmware; placing the EEPROM beside the ROM is not a universal import procedure. A new physical EEPROM-import test was not part of v87 acceptance. You can use your existing save instead.

## In game

- Rendering is already fixed at **640×480i**. The Hi-Res item is a label, not an active resolution switch.
- **L** toggles the FPS graph.
- Pause blur covers the full screen; menu swipes retain their perspective effect.
- v87 fixes the CamSpy lens and blue/cyan photograph bands.
- Analogue's progressive output and horizontal scaling are display settings, separate from the ROM's internal framebuffer.

## Exact release hashes

| Item | SHA-256 |
| --- | --- |
| Clean USA v1.1 base | `4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21` |
| Patched retail-header ROM | `04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b` |
| xdelta | `ef42ae87b55827c2c07dd096377246f51fe31bebbecac60879c75667e095be70` |
| Dark EEPROM | `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d` |
| Patch-and-save ZIP | `97f02232d47d67cc9e3cb9dd7678a4ef6e682eaf97bec9c6e586a991a1b5e259` |

The original [release manifest](../artifacts/PD6480iperf-v87-camspy-manifest.json) remains unchanged. Its pending-test notes reflect September 13; [subsequent user feedback](../evidence/v87-camspy-20260913/analogue-user-feedback.md) confirms CamSpy on Analogue.

For a black screen, crash or visual regression, first verify the exact output hash and confirm an Expansion Pak on original N64. Report the platform, firmware, mission, action and last visible screen using the [bug-report checklist](TESTING.md#reporting-a-problem). An upload success message alone does not prove the game booted.

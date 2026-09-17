# Install: choose L graph or stock controls

[Project home](../README.md) · [Testing limits](TESTING.md)

## Choose an edition

| Option | Choose this for | Downloads |
| --- | --- | --- |
| **v87 — L graph** | The existing graph edition. L toggles the FPS graph; the graph mod disables stock L/D-pad bindings. User-confirmed CamSpy on Analogue 3D. | [ZIP + Dark save](https://github.com/Cyiatic/PD6480iperf/releases/download/v87-camspy/PD6480iperf-v87-camspy-patch-and-Dark-save.zip) · [xdelta](https://github.com/Cyiatic/PD6480iperf/releases/download/v87-camspy/PD6480iperf-v87-camspy-candidate.xdelta) · [Release](https://github.com/Cyiatic/PD6480iperf/releases/tag/v87-camspy) |
| **v88 — No graph / stock controls** | Stock L/D-pad bindings, including mirrored-grip 1.2: D-pad movement, stick camera, L aim. Graph removed entirely. **Analogue 3D testing pending.** | [ZIP + Dark save](https://github.com/Cyiatic/PD6480iperf/releases/download/v88-no-graph/PD6480iperf-v88-no-graph-patch-and-Dark-save.zip) · [xdelta](https://github.com/Cyiatic/PD6480iperf/releases/download/v88-no-graph/PD6480iperf-v88-no-graph-candidate.xdelta) · [Release](https://github.com/Cyiatic/PD6480iperf/releases/tag/v88-no-graph) |

Both retain fixed 640×480i, the newer performance foundation, menu/pause-blur
fixes and the v87 CamSpy correction. These are **alternatives**, not sequential
updates. Hiding v87's graph does not restore stock inputs. Neither edition is
an exhaustive full-game compatibility release.

## Requirements

- Your own clean Perfect Dark **USA v1.1** ROM in big-endian `.z64` format.
- Original N64 with an **Expansion Pak** (8 MiB); v87 also has user Analogue 3D feedback. Do not assume that feedback validates v88.
- An xdelta3-compatible patcher and a cartridge/device that can run the patched image.

**Apply either patch directly to the clean ROM.** Do not apply v88 on top of
v87, or stack either edition with a standalone performance or 480i patch.

## Patch

1. Download your chosen edition's patch-and-save ZIP or xdelta above. GitHub's automatic **Source code** archives are for developers, not the playable patch bundle.
2. Verify the clean ROM against the shared base SHA-256 below.
3. Apply the patch to a **new output file**.
4. Verify the matching edition's output hash, then copy that output to your cartridge.

Example for **v88**, from a directory containing the patch and clean ROM:

```powershell
Get-FileHash -Algorithm SHA256 -LiteralPath '.\Perfect Dark (U) (V1.1) [!].z64'
xdelta3.exe -d -s '.\Perfect Dark (U) (V1.1) [!].z64' '.\PD6480iperf-v88-no-graph-candidate.xdelta' '.\PD6480iperf-v88-no-graph-candidate.z64'
Get-FileHash -Algorithm SHA256 -LiteralPath '.\PD6480iperf-v88-no-graph-candidate.z64'
```

For **v87**, replace both `v88-no-graph` filename portions with `v87-camspy`.
Do not force a source-checksum error: a different region, revision, byte order
or prepatched image is not the expected base. No full ROM is supplied.

## Optional 100% Dark save

Both ZIPs contain the **same 2,048-byte stock-format EEPROM**, with the profile
named **Dark**, stock controls/settings and cheats unlocked but not active.
The filenames differ to match each ROM; the save bytes do not.
Standalone saves: [v87](https://github.com/Cyiatic/PD6480iperf/releases/download/v87-camspy/PD6480iperf-v87-camspy-candidate.eep)
or [v88](https://github.com/Cyiatic/PD6480iperf/releases/download/v88-no-graph/PD6480iperf-v88-no-graph-candidate.eep).

Back up existing progress first. Follow your device's EEPROM-import procedure
and use a matching ROM/save basename, for example:

```text
PD6480iperf-v88-no-graph-candidate.z64
PD6480iperf-v88-no-graph-candidate.eep
```

Save locations differ by cartridge/firmware; placing the EEPROM beside the ROM
is not a universal import procedure. Fresh physical EEPROM-import validation
is still outstanding. You can use your existing save instead. **Dark does not
force 1.2 controls**: choose your preferred style normally in the game.

## In game

- Both editions render at **640×480i**. Hi-Res is an informational label, not an active resolution switch.
- **v87:** L shows/hides the FPS graph; not suitable for mirrored-grip L-aim/D-pad play.
- **v88:** no graph/hotkey. Select controller style **1.2** for D-pad movement, analogue-stick look and L aim. L respects the hold/toggle aim option; R and C-buttons remain available. Other stock controller styles remain selectable. “Mirrored” refers to the handgrip, not mirrored levels.
- Pause blur covers the full screen; menu swipes retain their perspective effect. Both include the v87 CamSpy lens/blue-band fix.
- Analogue's progressive output and horizontal scaling are display settings, separate from the ROM's internal framebuffer.

## Exact release hashes

### Shared input and save

| Item | SHA-256 |
| --- | --- |
| Clean USA v1.1 base ROM (not included) | `4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21` |
| Dark EEPROM, either filename | `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d` |

### v87 — unchanged L-graph edition

| Item | SHA-256 |
| --- | --- |
| Patched retail-header ROM (not included) | `04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b` |
| xdelta | `ef42ae87b55827c2c07dd096377246f51fe31bebbecac60879c75667e095be70` |
| Patch-and-save ZIP | `97f02232d47d67cc9e3cb9dd7678a4ef6e682eaf97bec9c6e586a991a1b5e259` |

### v88 — no graph / stock controls

| Item | SHA-256 |
| --- | --- |
| Patched retail-header ROM (not included) | `7971eb42e66ba1d5773e7a5c557f4ea578e7800e862f350b2ce5908b21223891` |
| xdelta | `5c9754322c26d4e1b5782b946a1cbb47df6f5f7f949ff57304669fb9da17cfa2` |
| Patch-and-save ZIP | `217debfc38a510599e17d3b71e518890bada3de18bb5638439e87de0222341e1` |

The [v87 manifest](../artifacts/PD6480iperf-v87-camspy-manifest.json) and ZIP
retain their September 13 packaging snapshot; [later feedback](../evidence/v87-camspy-20260913/analogue-user-feedback.md)
confirms CamSpy on Analogue. The [v88 manifest](../artifacts/PD6480iperf-v88-no-graph-manifest.json)
records the separate input candidate's source, hashes and verification limits.

For a black screen, crash or regression, verify the exact output hash and
Expansion Pak. Report the edition, platform, firmware, mission, control style,
aim mode and last visible screen using the [bug-report checklist](TESTING.md#reporting-a-problem).
An upload success message alone does not prove the game booted.

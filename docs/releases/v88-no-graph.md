# PD6480iPerf v88 — No graph / stock controls

**A second option, not a replacement for [v87's L-graph edition](https://github.com/Cyiatic/PD6480iperf/releases/tag/v87-camspy).**
This candidate removes the FPS graph and restores stock L/D-pad bindings.
It retains the 640×480i/performance foundation, full-screen pause blur,
menu fixes and v87 CamSpy rendering correction.

## Which one should I download?

- Want **L to toggle the FPS graph**? Keep [v87](https://github.com/Cyiatic/PD6480iperf/releases/tag/v87-camspy); its patch/save assets are unchanged.
- Want **D-pad movement and L aiming**, including mirrored-grip 1.2 play? Use **v88**. Simply hiding v87's graph does not restore stock controls.

In v88, choose controller style **1.2** in the normal game options. Use the
D-pad to move, analogue stick to look and L to aim. L respects the existing
hold/toggle aim setting; R and C-buttons remain available. Other stock control
styles remain selectable. “Mirrored” describes the handgrip, not the levels.
There is no graph or graph hotkey in this edition.

## Downloads and installation

- **Recommended bundle:** `PD6480iperf-v88-no-graph-patch-and-Dark-save.zip` — patch, optional stock-format 100% **Dark** EEPROM, README and manifest.
- `PD6480iperf-v88-no-graph-candidate.xdelta` — patch only.
- `PD6480iperf-v88-no-graph-candidate.eep` — optional Dark save (2,048 bytes), byte-identical to v87's.
- `PD6480iperf-v88-no-graph-manifest.json` — source, hashes and test status.

Apply directly to your own clean **Perfect Dark USA v1.1, big-endian `.z64`**.
**Do not apply v88 on top of v87 or another patch.** Original N64 requires an
**Expansion Pak**. Hi-Res remains a non-interactive label because rendering is
already fixed at 640×480i. Back up your save before importing Dark; cheats are
unlocked, not active, and the save does not force 1.2 controls.
No full ROM is included. GitHub's automatic **Source code** archives are for
developers, not the playable patch bundle.

See the [installation guide and edition chooser](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/INSTALL.md).

## Verification — and what is still pending

- **Software:** cold Carrington Institute at 640×480; scheme 1.2 D-pad movement in all four directions, both stick camera axes, L hold/release and toggle on/off, R aim, graph absent.
- Software input tests instrumented only control-style/aim settings in RAM. A core-only EEPROM-header adapter loaded Dark. Neither alters the distributed on-disk ROM.
- **Source:** all 84 surviving original graph input-mask edits reversed; obsolete paths not reintroduced; negative controls rejected. CamSpy actual-C regression: 193,800 cases pass. Asset audit: 1,403 valid compressed streams, zero invalid; 608 raw assets unchecked.
- **Original N64:** exact candidate uploaded over ED64; Elgato confirms sustained animated intro beyond startup. This is boot/intro proof, **not physical-controller gameplay**.
- **Analogue 3D: not yet tested for v88.** v87's user acceptance is not evidence that v88 has passed. Long sessions, multiplayer and a complete live-input/menu matrix remain pending.
- Patch decoded onto the clean base matches the candidate; ZIP entries and save hashes verified. Publication changes package documentation, not the candidate ROM.

[Evidence and stills](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/evidence/v88-no-graph/README.md)
· [Testing ledger](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/TESTING.md)
· [Source scope and build findings](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/V88_NO_GRAPH.md)

## SHA-256

| Item | SHA-256 |
| --- | --- |
| Clean base ROM (not included) | `4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21` |
| Patched ROM (not included) | `7971eb42e66ba1d5773e7a5c557f4ea578e7800e862f350b2ce5908b21223891` |
| xdelta | `5c9754322c26d4e1b5782b946a1cbb47df6f5f7f949ff57304669fb9da17cfa2` |
| Dark EEPROM | `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d` |
| Patch-and-save ZIP | `217debfc38a510599e17d3b71e518890bada3de18bb5638439e87de0222341e1` |

## Source

Runtime source: [`cb4e30de6433bbd4cc47e4f0b739700db15efb96`](https://github.com/Cyiatic/PD6480iperf/commit/cb4e30de6433bbd4cc47e4f0b739700db15efb96)
on [`fix/v88-stock-controls-480i`](https://github.com/Cyiatic/PD6480iperf/tree/fix/v88-stock-controls-480i),
based on public v87 pin `82d704d0154ea86f9e5d0fb98541907806f31960`.
The `v88-no-graph` tag includes subsequent packaging/documentation commits;
these do not change runtime source. The default branch's historical `src/`
is not the v88 runtime.

The local v87 rebuild used as a baseline had identical readable matching
symbols but two differently compressed, content-identical asset streams;
it is not byte-identical to the published v87 ROM. See the
[build guide](https://github.com/Cyiatic/PD6480iperf/blob/mods/performance/docs/BUILD.md)
for provenance and the remaining clean-toolchain `mkrom` dependency gap.

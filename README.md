<img src="images/pd6480iperf-banner.svg" alt="PD6480iPerf" width="483">

# PD6480iperf

Perfect Dark for N64: fixed **640×480 interlaced rendering** combined with the newer performance source and fixes for the higher-resolution menus and camera effects. Choose an **L-toggle FPS graph** or **no graph with stock controls**.

## Choose your patch

Both editions include the CamSpy, menu-navigation and full-screen pause-blur fixes. These are separate alternatives, **not patches to stack**; v88 is not a replacement for players who want the graph.

| Option | Controls | Downloads |
| --- | --- | --- |
| **1. v87 — L graph** | L shows/hides the FPS graph. Stock L/D-pad bindings remain disabled by the graph mod. | [Patch + Dark save](https://github.com/Cyiatic/PD6480iperf/releases/download/v87-camspy/PD6480iperf-v87-camspy-patch-and-Dark-save.zip) · [Patch only](https://github.com/Cyiatic/PD6480iperf/releases/download/v87-camspy/PD6480iperf-v87-camspy-candidate.xdelta) · [Release notes](https://github.com/Cyiatic/PD6480iperf/releases/tag/v87-camspy) |
| **2. v88 — No graph / stock controls** | Restores stock L and D-pad inputs; supports mirrored-grip 1.2 play. No FPS graph or graph hotkey. | [Patch + Dark save](https://github.com/Cyiatic/PD6480iperf/releases/download/v88-no-graph/PD6480iperf-v88-no-graph-patch-and-Dark-save.zip) · [Patch only](https://github.com/Cyiatic/PD6480iperf/releases/download/v88-no-graph/PD6480iperf-v88-no-graph-candidate.xdelta) · [Release notes](https://github.com/Cyiatic/PD6480iperf/releases/tag/v88-no-graph) |

For **D-pad movement and L aiming**, choose v88 and select controller style **1.2** in game. The analogue stick controls the camera; L uses your existing hold/toggle aim setting. “Mirrored” describes the handgrip, not mirrored levels. Simply hiding v87's graph does not restore these controls.

**v87 has user-confirmed CamSpy operation on Analogue 3D. v88 has passed focused software input checks and an original-N64 intro boot, but has not yet been tested on Analogue 3D.** Both remain prerelease candidates.

- [Installation, base-ROM hash and save instructions](docs/INSTALL.md)
- [CamSpy comparison and validation evidence](evidence/v87-camspy-20260913/README.md)
- [No-graph changes and verification](docs/V88_NO_GRAPH.md)

Use your own clean **USA v1.1, big-endian `.z64`** ROM. An **Expansion Pak is required on original N64**. Resolution is already fixed at 640×480i; the Hi-Res menu item is intentionally non-interactive in both editions.

Both bundles contain the same optional stock-format **Dark** EEPROM: 100% unlocks with stock controls/settings; cheats are unlocked, not activated. It does not force controller style 1.2. Back up your existing save before importing it. No full ROM is included.

## What has actually been tested?

| Platform / check | Result and scope |
| --- | --- |
| Analogue 3D | User-confirmed v87 CamSpy fix. Earlier v86g feedback covers gameplay, L graph, menu navigation and pause blur. |
| Original N64 + Expansion Pak | Exact normal v87 ROM uploads and progresses through the animated 3D intro. **Not** an interactive CamSpy test. |
| Software, v87 | Cold-boot Investigation; CamSpy activation, shutter, settled view, movement and exit; pause/resume and visible L-toggle pair. |
| Software, v88 | Cold Carrington Institute at 640×480; four D-pad directions, both stick camera axes, L hold/toggle aim, R aim and graph absent. Source/CamSpy regression checks pass. |
| Original N64, v88 | Exact candidate uploaded; Elgato confirms progressing animated intro. **Not** physical-controller gameplay. Analogue testing pending. |
| Wider regression checks | v86g: 21/21 mission initialization gates, plus short AI co-op and four-player checks. **Not** full mission completion or a fresh v87 full-mode sweep. |

Neither edition claims exhaustive compatibility. Isotope-objective completion, original-N64 CamSpy gameplay, other EyeSpy variants and comparative FPS benchmarks remain unverified. v88's focused input tests do not replace a full mode/menu sweep. See the [testing matrix](docs/TESTING.md).

## Read the project

| I want to… | Start here |
| --- | --- |
| Apply the patch / import Dark | [Install](docs/INSTALL.md) |
| Understand the bugs and fixes | [Technical findings](docs/FINDINGS.md) |
| Check validation limits / report a bug | [Testing](docs/TESTING.md) |
| Reproduce or modify the runtime | [Source and build guide](docs/BUILD.md) |
| Follow development history | [Milestones and archive](docs/HISTORY.md) |
| Browse all documentation | [Documentation index](docs/README.md) |

### Distribution and runtime branches

| Branch | Purpose |
| --- | --- |
| `mods/performance` (this default branch) | Patch/save distribution, documentation, evidence and historical integration source. **Its `src/` does not reproduce either current edition.** |
| [`fix/v87-camspy-480i`](https://github.com/Cyiatic/PD6480iperf/tree/fix/v87-camspy-480i) | Buildable v87 runtime; public source pin [`82d704d01`](https://github.com/Cyiatic/PD6480iperf/commit/82d704d0154ea86f9e5d0fb98541907806f31960). |
| [`fix/v88-stock-controls-480i`](https://github.com/Cyiatic/PD6480iperf/tree/fix/v88-stock-controls-480i) | v88 no-graph runtime; source pin [`cb4e30de6`](https://github.com/Cyiatic/PD6480iperf/commit/cb4e30de6433bbd4cc47e4f0b739700db15efb96). Later commits package it without changing runtime code. |

The **v87** release payloads are unchanged. Their September 13 README/manifest are packaging-time snapshots; this front page and [dated acceptance update](evidence/v87-camspy-20260913/analogue-user-feedback.md) include the later user confirmation. v88 has its own package, source pin and test record.

## Credits and repository scope

Based on **Ryan Dwyer's Perfect Dark decompilation, performance work and 640×480i work**. Thanks to the user and Graslu00 for test feedback and the CamSpy report.

Source licensing is in [LICENSE](LICENSE). The code license does not grant rights to distribute the original game's ROM or extracted assets. Full ROMs and bundled host/IRIX binaries have been removed from the published history; local backups remain private. Patches, saves, source and small verification artifacts are retained.

The public history uses new commit IDs, but the v87 ROM/patch/save bytes and game source are unchanged. See [public-release audit and migration notes](docs/PUBLIC_RELEASE.md) for the cleanup scope and original-to-public commit map. If you have an old private clone, start with a fresh public clone rather than merging or force-pushing its history.

## AI Assistance Disclosure

This project was developed with AI assistance from OpenAI Codex for reverse
engineering support, scripting, documentation, visual comparison workflows, and
candidate iteration. The repository owner directed the work, reviewed the
resulting changes, and remains responsible for the project's technical claims
and final decisions. Hardware setup, real-console testing, and subjective visual
evaluation were performed by the repository owner.

The README logo was also generated with AI from the supplied Perfect Dark
lettering reference; see [logo provenance and prompt](images/README.md).
For this project's automated original-N64 checks, Codex operated the ED64,
Kasa and Elgato workflow under the owner's direction; the platform-specific
results remain distinguished in the [testing ledger](docs/TESTING.md).


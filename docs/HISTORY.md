# Development history

[Project home](../README.md) · [Current findings](FINDINGS.md)

This is a milestone index, not a list of interchangeable releases. **Use v87 for current testing.** Older documents preserve what was known at their date; words such as “current,” “final” and “pending” inside them are historical.

| Milestone | What changed / what was learned | Record |
| --- | --- | --- |
| Input comparison | Distinct performance payloads and standalone 480i control; clean USA v1.1 base required. | [Patch analysis](input-patch-analysis.md) |
| Early v7-era investigation | Boot/layout experiments and crash analysis; not a universal explanation of all later failures. | [Boot crash notes](v7-boot-crash-analysis.md) |
| v79/v80b | Audit exposed a 75-commit gap in the older integration base. | [Historical lineage audit](performance-lineage-gap-audit.md) |
| v81–v82b | Restarted from newer performance source; two full colour buffers; fixed lazy menu-scratch briefing regression. | [v82b record](PD6480iperf-v82b.md) |
| v84 | Full-screen pause blur and menu geometry; fixed Hi-Res label. | [Evidence](../evidence/v84-fullscreen-menu-blur/README.md) |
| v85 | Smaller correct blur allocation, but broader testing exposed stage-load failures. | [21-stage audit](../evidence/v85-full-mission-matrix/README.md) |
| v86–v86f | Budgeted room residency, model/menu reservations and safe quiescent reuse. | [v86f evidence](../evidence/v86f-quiescent-room-reuse/README.md) |
| v86g | Completion-queue reserve; 21/21 initialization gates; scoped co-op/four-player checks and user Analogue acceptance. | [Evidence index](../evidence/v86g-completion-reserve/README.md) |
| v87, September 13 | CamSpy lens/texture-step fix; cold software comparison, source tests and normal-N64 intro check; immutable patch/save bundle. | [Evidence](../evidence/v87-camspy-20260913/README.md) |
| v87, September 14 UTC | ED64 reconnect retry confirmed transfer and animated original-N64 intro. | [Retry record](../evidence/v87-camspy-20260913/hardware-retry-20260914/README.md) |
| v87, confirmation recorded September 15 | User reports CamSpy working on Analogue; candidate and patch bytes unchanged. | [User feedback](../evidence/v87-camspy-20260913/analogue-user-feedback.md) |

## Archive and repository layout

The [previous long README](archive/README-through-v87-packaging.txt) is preserved as plain text. It contains upstream descriptions, chronological experiments and now-superseded recommendations. It is not an installation guide.

The default `mods/performance` branch retains historical source alongside release docs and evidence. Current v87 runtime lives on `fix/v87-camspy-480i`; see the [build guide](BUILD.md). This split is explicit rather than silently replacing the historical source tree.

Current patch/save payloads were not regenerated during the documentation cleanup. Later acceptance is recorded separately from their packaging-time README/manifest.

The initial documentation cleanup only untracked old ROMs, leaving them in private history. The subsequent public-release cleanup removed full ROMs and bundled host/IRIX binaries across all published history, while retaining an independent private backup. Local ROMs and pre-existing work were not deleted.

Publication preserves the branch names and source contents but changes affected commit IDs. See the [public-release audit and mapping](PUBLIC_RELEASE.md). Old IDs inside dated notes and immutable release manifests are historical provenance, not instructions to fetch the private history.

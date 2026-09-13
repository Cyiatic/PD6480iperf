# v87 CamSpy candidate evidence

The user relayed Graslu00's report of vertical blue lines in Investigation's
CamSpy view. The unchanged v86g software reproduction shows a broken lens and
the exact cyan/blue bands during the photograph shutter. The candidate fixes
those sampled views while preserving the existing fixed 640x480i integration.

See [Luna's cold-boot software chain](v87-camspy-qa-report.md),
[provenance manifest](v87-camspy-qa-manifest.json),
[actual-C test result](actual-c-tests.json), and
[normal-ROM N64 boot scope / cleanup blocker](hardware-boot.md).

## Inspected visual comparison

| View | v86g comparator | v87 candidate |
| --- | --- | --- |
| Active CamSpy | [black centre / split sampling](v86g-activation.png) | [continuous lens](v87-activation.png) |
| Photograph shutter | [cyan vertical bands](v86g-shutter.png) | [clean aperture](v87-shutter.png) |

Master also inspected [graph shown after exit](v87-exit-graph-shown.png),
[graph hidden](v87-graph-hidden.png), [pause](v87-pause.png), and original-N64
[city](hardware-city.png), [roof](hardware-roof.png), [ship](hardware-ship.png)
intro stills. [Plug1 OFF](power-off.log) and [Relay0 status](power-status.log)
are actual post-trial logs. No hardware CamSpy or Analogue result is inferred.

Runtime branch `fix/v87-camspy-480i`, commit
`d533653ca75d98a875bac28a0369a2b33c5abc3d`, published only to the private
Cyiatic/PD6480iperf repository, not the public upstream origin.
The old v86g ROM and ELF hashes remain unchanged.

## Package checks

The xdelta round-trip matches the tested ROM exactly. The four ZIP entries
(patch, unchanged stock Dark EEPROM, README, manifest) were streamed back and
SHA256-compared to their sources; no ROM/state/RAM/core/executable/video is in
the ZIP. [Candidate instructions](../../artifacts/PD6480iperf-v87-camspy-README.md).

ZIP `PD6480iperf-v87-camspy-patch-and-Dark-save.zip`:1471120bytes,
SHA256 `97f02232d47d67cc9e3cb9dd7678a4ef6e682eaf97bec9c6e586a991a1b5e259`.
Cleanup is incomplete: the environment rejected recording deletion before
execution;99576788bytes remain in Timeshift. No deletion workaround was used.
The actual isotope objective route is ongoing separately.

# v87 Analogue user confirmation

Status recorded **September 15, 2026**. This is a later acceptance update, not a rewrite of the September 13 packaging manifest.

After the current v87 candidate and matching Dark EEPROM were provided for Analogue testing, the user reported:

> camspy works good

The candidate provided was `PD6480iperf-v87-camspy-candidate.z64`, SHA-256:

```text
04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b
```

Runtime: `fix/v87-camspy-480i` at `d533653ca75d98a875bac28a0369a2b33c5abc3d`. The subsequently supplied patch reconstructs this exact image; no runtime or release-payload change accompanied the confirmation.

## Scope

This closes the reported Analogue CamSpy first-person rendering issue for the user's tested setup. It is user-observed feedback, not a newly instrumented physical-hardware trace. No firmware version or additional objective-completion details accompanied the confirmation.

Do not infer successful isotope-objective completion, every EyeSpy variant, original-N64 CamSpy gameplay, a full-game playthrough or a measured speedup. The software route to the isotope was stopped after the reproduction target was clarified; completion remains unverified.

Earlier user feedback on v86g covers normal gameplay, menu navigation, full-screen pause blur and L graph operation. Keep that earlier coverage separate from the narrower v87 confirmation.

See the [current testing matrix](../../docs/TESTING.md) and [CamSpy comparison](README.md).

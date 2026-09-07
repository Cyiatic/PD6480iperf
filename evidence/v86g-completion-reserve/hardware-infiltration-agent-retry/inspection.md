# Labelled v86g Agent replay on original N64

Diagnostic source `a528d058fb23543af43841db13c73a1a3f11721b`, ROM
`cb3568848785e143d2c9adb1e7e0ce1bbdd72a3d11e08efce0df01f43e2157a3`, ELF
`a27f4cceddddaf40296fecb4fc406968d330a50302c4193044c88f798b62005a`.
It uses the reviewed main-input-partition replay and RAM-only Dark save.
Physical controller status is preserved; physical Pak writes blocked. Stock
Agent is selected through the normal difficulty handler. No health/AI patches.
V86G TEST is always visible. This is not the normal ROM or an Analogue run.

The first upload timed out and is preserved in the sibling failure record.
On this fresh retry, September7UTC: OFF02:00:42, exact ED64 FTDI restart02:00:47,
ON02:00:48, terminal UNFLoader PID25632 started02:01:24. It reported
`ROM successfully uploaded in 36.53 seconds!` then native0 at02:02:00.
No full-image readback claim. Owned GameCapture PID20540 started02:02:00,
startup allowance ended02:02:46,210-second observation ended02:06:17.
OFF/statusRelay0 verified02:06:19/20. Only Plug1 was controlled.

Two flushed TS segments were inspected:

| Segment | Bytes | SHA256 |
| --- | ---: | --- |
| 1 | 290959140 | d2b1e9cd8f1bf3050466745e082159813644271b4ed25d38ab5e090df5b62650 |
| 2 | 112447312 | b5c2fc0717392844fa33f3e1934266cc4caa8b0a6dad4ba0b02048ddd77de106 |

The descriptor reports a156.156-second first segment and60.060-second second
logical interval. Capture is Elgato-processed video, not direct VI measurement.
Several seeks emitted decoder POC warnings; all returned0 and yielded stills.
All twelve retained stills were visually inspected:

- Segment1+10s: file-menu lateral transition over full-screen blurred CI, with
  eyepiece and off-centre menu; +40s: CI3D; +80s: Infiltration opening.
- +120/+138s: alive paused Infiltration, different menu pages, blurred background
  spanning the screen rather than a top-left quarter.
- +145s: Video Options/fixed resolution and graph shown; +150/+154s: graph hidden
  while the diagnostic label remains. Segment2+10s: graph shown again.
- Segment2+35s: resumed gun/3D view, health depleted but not yet a failed menu.
- +55s: red damage/death transition; +59s: explicit mission-failed menu. This is
  ordinary unattended combat death, not a death-free completed replay.

Observed HUD shows OOM0/BGFAIL0/EVICT6; no exception screen was observed.
This verifies short alive pause/menu/L and resumed gameplay on real N64 for the
labelled build. It does not prove a complete mission, sustained play, every
menu animation, normal-ROM physical input handling, or Analogue compatibility.

After inspection, both exact TS files,81920/28672-byte metadata sidecars and
850-byte descriptor were permanently deleted:403517894bytes reclaimed.
Small stills, copied descriptor and logs remain; Timeshift contains only its
307-byte timeline. Plug1 remains OFF, with no owned uploader/capture running.

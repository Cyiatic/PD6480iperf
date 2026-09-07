# Requested v86g integration — completion evidence

September 7, 2026 UTC. The user has now confirmed the remaining current-build
L-toggle check after confirming Analogue blur/menu navigation and approving
the non-interactive Hi-Res option. The requested combined patch, visual fixes,
Dark save and private source handoff are complete. No ROM rebuild followed
the user's tests.

## Requirement-by-requirement check

| Requirement | Inspected authoritative evidence |
| --- | --- |
| Combine genuine 480i with newer performance code | Clean runtime HEAD 26cb92ae9d0ae2cba172999c0d5c1762f32d5a50 has modern performance base bf3245076d00fbbb29ca1e0906672381f2d43a52 as ancestor. Full-size colour/depth definitions, NTSC HAF1 field registers and authenticated normal-ROM 640x480 RAM samples are preserved; this is not the older 640x220 substitute. |
| Use Expansion Pak appropriately | Eight MiB address space; two 614400-byte colour buffers and 614464-byte depth allocation. Room partitions and allocation/cache faults checked across all 21 solo initialization samples, plus bounded Deep Sea, co-op and four-player exercises. Texture warmup and retained geometry are budgeted rather than dropping resolution. |
| L toggles FPS graph | Normal-ROM software hidden/shown images, separate original-N64 replay hidden/shown captures, and the user's explicit Yes to the current-build L question. |
| Correct pause blur and left/right menus | Actual-source blur tests and normal software images, labelled N64 pause/navigation captures, and the user's current Analogue confirmation that both look good. |
| Resolve confusing/crashing Hi-Res transition | Fixed 640x480i rendering, non-interactive label; saved Hi-Res preference does not change buffer geometry. User explicitly approves skipping this option. |
| Verify with available real hardware before Analogue handoff | Exact ED64 upload and Elgato rendered intro for the normal ROM. Separate labelled same-core replay reaches Infiltration gameplay and exercises pause/menu/L. Logs distinguish those scopes; no upload exit0 or black frame is counted as gameplay. User subsequently confirms the normal-build Analogue behavior. |
| Include stock-format 100% Dark save | Matching-name 2048-byte EEPROM is included; stock decoder/re-encoder validation, completion-field/checksum checks and all four save unit tests pass again. No installed save was overwritten. |
| Private PD6480iperf repository | GitHub reports Cyiatic/PD6480iperf is private. Runtime source and distribution evidence are published there; binaries containing the ROM remain local. |
| Power and disk hygiene | Only exact Plug 1 used; OFF/status logs after tests. No running capture/uploader/emulator test remains. Inspected recordings deleted; Timeshift contains only its 307-byte timeline. The unrelated N64 switch was not controlled. |
| Usable reproducible deliverables | Current ROM/patch/save hashes rechecked; xdelta-decoded local ROM matches the exact tested ROM. All four original ZIP entries and all four final ZIP entries streamed back and hash-compared to their source files. Final ZIP has no ROM. |

## Immutable payload and final package

Normal ROM: `79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`.
Patch: `1bc0b3606bd2eb69cb4c61876c632771b2c384d183c8bff6b26cb6af05c958bd`.
Dark EEPROM: `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d`.

New final handoff ZIP:
`artifacts/PD6480iperf-v86g-final-patch-and-Dark-save.zip`, 1,451,113 bytes,
SHA256 `f32b740337e5b8ec2b78c4e5494cf3cdcc12d924f963f1690edbd95466344d8c`.
Contains the unchanged patch (1,447,194 bytes), unchanged EEPROM (2048),
new final README (3175) and new final manifest (1691). The previously delivered
candidate ZIP is preserved as a dated test snapshot, not silently overwritten.

## Limits remain explicit

This completes the requested functional integration and handoff, not a claim
of exhaustive full-game endurance, every arena/weapon/mode, a measured FPS
increase or physical save import. No numeric speedup was requested or measured.
Modern CPU/AI/DMA/math code is retained, while guaranteed whole-geometry
preloading cannot fit every mission alongside the full 480i buffers.
Normal original-N64 direct physical-input gameplay is not misrepresented:
its recorded normal run is the intro; the interactive N64 run is labelled.
Analogue confirmations are the user's observations in response to the linked
build, not an independently captured ROM hash or direct VI-register measurement.

See [user feedback](analogue-user-feedback.md),
[hardware observations](hardware-infiltration-agent-retry/inspection.md),
[normal software exercise](deepsea-exercise/README.md), and
[final instructions](../../artifacts/PD6480iperf-v86g-final-README.md).

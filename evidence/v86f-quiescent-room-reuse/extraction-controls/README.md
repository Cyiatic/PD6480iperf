# Extraction: cold-boot/controller-history controls

These are software-only, ordinary-controller-input samples. No RAM pokes or
replay harness. Normal v86f is still held; these results do not certify Analogue.
All use the immutable host/core/layout identified in the parent evidence,
cached interpreter, cxd4/software video, 8 MiB and the in-memory EEPROM header
adapter. The supplied generated stock Dark EEPROM is unchanged.

| Run | Start / ticks / connected mask | Final result |
| --- | --- | --- |
| v86f-extraction-cold-four | Cold / 9150 / 15 | Extraction frame3, cutscene1, stalled |
| v86b-extraction-cold-four | Cold / 9150 / 15 | Extraction frame1437, alive/unpaused |
| v86f-extraction-fresh-seed-one | Fresh own menu state / 3000 / 1 | Extraction frame1434, alive/unpaused |
| v86f-extraction-fresh-seed-four | Same fresh menu state / 3000 / 15 | Extraction frame1434, alive/unpaused |

All four final snapshots are compiled-mode-verified Solo, health1, dead0,
with no OOM/cache/allocator failures, valid room partitions and no flagged CPU
exception. The game itself confirms controller masks15/15/1/15. The failed
run has zero idle-rule evictions, current RSP graphics state0x12, no current
RDP owner, and a queued graphics task. Its final image is a stale mission
briefing, not successful in-game video. Passing final images are very dark
with scope/HUD visible; their similar appearance does not certify all visual
effects. Native exit0 was observed for the older build and both restored
controls. The cold-f run's original tool session was lost during compaction;
its DONE marker, completed files and stopped process are preserved, not an
invented native exit code.

The cold-one timeline input is the parent `extraction-stall/` file
`v86f-extraction-cold-one-input.txt`, SHA256
`7f6e87ef409672360b908244c43ded7b0777ea1b08036aa6d496eb031cef763d`.
Both cold runs use it unchanged. The fresh seed is a new continuous cold v86f
run for its first6150 ticks with one controller and the Dark EEPROM. Its menu
image was inspected: Defection is selected; CI stage38/frame1478, Solo/no AI.
It completed native0. State SHA256
`ebb6d061f1908b5906b0e677aaeae75fc2f7330966d87398b89dfba7ab073f34`;
matching296960-byte save-memory SHA256
`ad1791c4ea908b7c3c069696672f7dbda31493cb49656d71c037593dd939bd1e`.
Both restored controls load these exact files, with no foreign-ROM state.
Their3000-tick input is parent `v86f-extraction-extended-input.txt`, SHA256
`44381bb9e452cb978626d17a2f49a000929cf63398f5ad398733ff4510ef83df`.

Final state hashes, in table order:

- `e1f0e1c5257e5f76cc72e97ce47281fcc84123dfdce4207b2c92ee1e4c96b325`
- `52064e1e98f99b2ae0cea3e4b932944a08023d55bbf47f1373d58fbe3845b058`
- `c7182ba6385823cce8c5b6e66eba2146f7f5dba814e1d438941259e547d4dd67`
- `b85b8aec76f7f2dde3900005fe0ab6e7bf5ea00ccd2df0e0df12630a9f44ea85`

v86b ROM/ELF hashes are
`c33ec1459b3092d89f5a3b00f82f6b4dd8e59c294b479aa7d039dc7471455df7` /
`a207b10b49eb024063751c403829e9fcf54416dac0026a8e1b3351ccdd2075f3`.
v86f ROM/ELF remain
`bf219fa49620be957f366cb2b84ba255d67712bb36faf3e494ddfabfae7fa41e` /
`82d6a0e7ffe479c2eb2e2b11efa9b992c0493d58ca4688dbf9be5804328d2511`.

Conclusion: restoration and four-controller presence at mission launch are
not sufficient explanations. The earlier boot/menu history matters in these
samples; a specific causal bug is not yet proved. Existing failures remain
failures. The separate no-retry event-drop diagnostic completed alive/unpaused
with zero counters, but did not reproduce the stall. Its changed layout/timing
prevents treating that as a normal-ROM fix or exclusion of queue drops in the
failed normal run. See [its evidence](../event-drop-diagnostic/README.md).

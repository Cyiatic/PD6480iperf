# Newer-core memory experiments

Software evidence, not console or Analogue validation. Normal cold runs use
cached interpreter, cxd4 RSP, Angrylion video, 8 MiB, the synthesized stock
Dark EEPROM, and headless-cold-briefing.txt controller input. No saved state
or gameplay RAM edits are used. The host's in-memory ED/16-Kbit EEPROM header
adapter changes only save identification; disk ROMs remain retail-header.

The layout is compiled from this newer source's headers and checked against
the matching ELF. It differs from v80b: player size 0x1c80 and pause offset
0x1a34, scheduler size 0xa8. Resident-code hashes are verified before reports
are written. `hardware_verified: false` is deliberate.

| Experiment | Outcome |
| --- | --- |
| v81, full modern triple buffering | OOM before CI, failed 43888-byte hand model load |
| v81 allocation trace, diagnostic only | Confirms 4x153600 eager CI menu buffers, plus 51200 global buffer |
| v81b, lazy model-preview buffers | CI visible, but OOM and only 114/140 rooms loaded; later briefing crash |
| v82, full modern double buffering | 140/140 CI room geometries, no OOM, 484688 bytes free; still briefing crash |
| v82b, scratch before callbacks | Fresh CI-to-briefing test completes; 140/140 rooms, no OOM/exception, 331040 bytes free |
| v82b, resumed mission transition | Accepts briefing and renders Skedar opening cutscene; 137/137 rooms, no OOM/exception, 363744 bytes free |

The v82 briefing crash is an integration regression: the deferred buffer is
also used by briefing/challenge callbacks before a model is rendered. v82b
allocates before dialog callbacks rather than at first model rendering.
None of v81, v81b or v82 is a new release candidate. v80b's earlier package
is unchanged; its older performance lineage and test limitations still apply.

`v81-allocation-trace.json` records requested allocations, not live retained
bytes. In particular the 2708784 requested file bytes cannot be interpreted
as live usage because reallocations shrink many of them. The trace ROM was
built on a separate diagnostic branch and is not used for normal test claims.

## v82b original-N64 boot check, 2026-09-06

Source `24995c1c66eaa0e4ac5568f5711f7af7678b5561`, private branch
`experiments/v82b-menu-scratch`. ROM SHA256
`9da54bbde7d42be0441af6031de1711fe647f3a4036e5ca9da381ccc0cea30b1`.
No synthetic input or RAM-save hooks are in this normal ROM.

Kasa token refresh worked; only Plug 1 was used. It was ON at 00:05:49.
The ED64 upload command ran 00:06:05.195 through 00:06:41.811 (36.616 s),
with capture closed. The surrounding PowerShell completed exit 0 but this
invocation did not separately log the native uploader exit code. Elgato and
FTDI USB device IDs both reported OK before testing.

Owned GameCapture PID 24740 started 00:07:13. Fresh timeshift segment 0001
was created 00:07:46. Stills at 10, 40 and 85 seconds show different animated
city/rooftop scenes, past product identification. This is a rendered-intro
boot observation, NOT interactive hardware play, Hi-Res interaction, native
resolution measurement from composite, physical save-import or Analogue proof.

Recording duration 89.239333 s, size 166299348 bytes, SHA256
`4522e39d6483f8447448ce7e992c29e0abfbd1306c4287866b29b4b60502d830`.
Capture was stopped and Plug 1 OFF confirmed twice at 00:09:16. The inspected
recording and three metadata files were permanently deleted by 00:10:45,
reclaiming 166345394 bytes; small stills remain. N64 outlet/parent untouched.

Skedar transition is a separate emulator run restored from this exact v82b
cold test's state, then ordinary scripted A input. It is not another cold boot
and the final frame is a cutscene, not controlled gameplay. Hi-Res interaction,
walking/shooting in missions, multiplayer and performance benchmarks remain.

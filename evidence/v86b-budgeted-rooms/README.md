# v86b — budgeted room residency on the modern 480i core

Development evidence, 2026-09-06. **Not a hardware-verified release.**

The Expansion Pak was already enabled: these tests use the real 8 MiB budget.
Two 614400-byte colour buffers plus 614464 bytes for depth occupy 1843264 bytes,
1280000 more than upstream's three 320x220 colour buffers plus depth. v85's
full-room preloading runs out of memory in 11 of 21 initial mission samples.
v86b retains warmed textures and as much room geometry as fits, loading and
evicting geometry/hit batches on demand. Current and two prior submitted graphics
epochs are pinned. Actual onboard/expansion free banks are separate; their
intervening framebuffer/stack region is not treated as free. General stage
headroom is 128 KiB plus CI's lazy 153600-byte per-player menu-model reserve.

The modern CPU/AI/DMA/math changes, generated assets, full 640x480 colour/depth
buffers, corrected menu blur, fixed-resolution label and L graph remain.
Full-level geometry preloading is no longer guaranteed. No measured speedup,
unchanged load time, full-playthrough, multiplayer or Analogue claim is made.

## Identity

- Runtime source: private branch `experiments/v86-budgeted-modern-rooms`,
  commit `ea2ad550b4862cb9fe1451e0da8d42ea4a32c1ef`.
- Normal ROM: `c33ec1459b3092d89f5a3b00f82f6b4dd8e59c294b479aa7d039dc7471455df7`.
- Matching ELF: `a207b10b49eb024063751c403829e9fcf54416dac0026a8e1b3351ccdd2075f3`.
- Compiled version-4 cache ABI layout:
  `d05a0af19e5587eb69c50e67d27fa5350121a8d7545c0335437d9b094463c3e2`.
- CRC header: `69c42a4a / 7729ddf3`.
- Fresh v86b Defection-highlighted seed:
  `4dc8c4e032d695130429d834a1427da0c8e197fcd175c6e87e7ab874cd5c5829`.

Normal disk ROM, no diagnostic selection or RAM pokes. Software uses the cached
interpreter, cxd4 and Angrylion with an EEPROM-header adapter. No foreign-build
state is restored. Cold stock-Dark boot precedes the seed. ROM/RAM/state binaries
remain local, not included in this evidence folder.

## Checks

`collected.json` reinspects all 33 startup/continuation samples. Its final
selection is a direct parent/state/RAM-authenticated chain, never a selection
of whichever result happens to pass. All 21 final samples are unpaused at the
correct mission with gameplay initialized, no cutscene, 640x480 dimensions,
no stage allocation marker, no main/scheduler CPU fault flags, no required-room
load failures and no cache allocator faults. Every required mission room was
warmed; every currently visible room has geometry and exact hit-batch counts.
Every room-heap byte is accounted for once as live geometry, batches or free.
Reports explicitly distinguish unloaded warmed rooms from full preloading.

16 original short samples pass initialization. Extraction, Infiltration, Rescue,
Villa and Escape are still in opening cutscenes, not allocation failures. One
late Start pulse per matching state yields gameplay. Seven other initialized
samples finish paused; a B continuation yields unpaused gameplay. Initial
reports remain intact. Example evictions: Air Base 20, Villa 9, Escape 8,
Infiltration 6. These are counts, not a performance benchmark.

Infiltration and Deep Sea additionally receive ordinary forward, Z fire,
Start pause and horizontal menu swipes. Both move, loaded ammunition changes
8 to 5, and the final pause image has full-screen blur, not a top-left quarter.
These two pause images and the final Attack Ship/WAR gameplay images were
visually inspected. Other visual inspections are described in the run notes;
do not infer every room has been visually traversed. A further ordinary B
continuation returns both exercises to unpaused gameplay: Infiltration frame
1945 and Deep Sea frame 995, still without OOM, cache-load or CPU faults.

Host verification also passes 25 Python inspection/input/provenance tests,
100000 randomized operations against the actual shared C allocator, task-epoch
pinning/wrap and gap/overlap guards, and the actual C menu blur/allocation test.
Quarter-screen sampling/quads and the old oversized allocation fail the
negative-control blur tests as expected. Dynamic room colours were reviewed:
`roomHighlight` uses per-frame `gfxAllocateColours` or resident room colours,
not an unfreed independent mema allocation on each room eviction.

The first v86 experiment (ROM `a8d1ecab3f0297614ad3331f4d88fd151788f9e70d53df052e8e874098d85c50`)
is rejected: CI's late menu scratch requested 153600 bytes after the room heap
consumed that headroom. v86b reserves it explicitly. The failed cold report is
retained, not relabeled a pass; that initial v86 was never uploaded.

## Hardware: transport/capture evidence, not a v86b boot pass

Only the exact Kasa **Plug 1** outlet was controlled. The unrelated **N64** outlet
was never queried or toggled. Elgato and FTDI device identities remain the saved
workflow's devices. No firmware flashing or permanent USB configuration changes.

| Attempt | Observation |
| --- | --- |
| UNFLoader old executable, attempts 1–3 | Each reaches the bounded 65-second timeout; no successful upload. Exact FTDI device restarted before attempt 3. |
| Capture-only preflight | Fresh EverDrive menu at +10/+20 s proves power and Elgato input. No candidate upload. |
| Prerelease UNFLoader, hidden | 65-second timeout; no successful upload. |
| Prerelease UNFLoader, terminal | USB opened and Uploading ROM printed, no completion. Cancel did not exit; Ctrl-C stopped it. +10/+65/+140 s capture remains EverDrive menu. |
| Existing reconnect2m serial utility, attempt 1 | Reports transfer speed 693 KB/s and Finished in 112.142 s, then process timeout at 120 s. No capture or verified handoff. |
| Serial attempt 2 | Refused before power-on because an exited process was still enumerable. Helper now distinguishes HasExited from a running process. |
| Serial attempt 3 | Stalls mid-transfer; 120-second timeout, no Finished message and no capture. |

Executable identities:

- Old UNFLoader: `01264203db211282e1d2ed6443e76d0272ba92ed36f291eeec61920a30ff55f2`.
- Prerelease: `76d28305fe9ddf209e269d7b5f45927d5069deacad5c5166b628e7f7d5a5ea88`.
- Serial utility: `9023bf0bff221cbf63be818707480f3071a99312da2f0a7842b1a8e65a7536cf`.

The bounded helper records serial completion-text/exit failures separately and
can inspect capture after that specific failure; this path has not yet yielded
a successful hardware test. An external terminal lease likewise never proves
uploader success. Do not equate an uploader message or worker exit with a ROM pass.

Final Plug 1 OFF: 19:19:46 UTC; Relay: 0 at 19:19:47 and independently afterward.
All live uploader/capture workers are stopped. The 57.8 MB preflight recording
and 273.5 MB terminal-attempt recording were inspected and permanently deleted;
small stills/metadata are retained. No recordings from the serial attempts.

Next gates: verified ED64 handoff and fresh original-N64 gameplay capture,
longer room transitions/combat and multiplayer memory pressure, Analogue 3D,
and controlled performance comparisons. Stock Dark EEPROM remains the existing
2048-byte stock-format save; it is not an emulator state. No new user-test ZIP
or hardware-verified release is issued by this evidence update.

# v86b — separating failed ED64 transfers from ROM failures

2026-09-06, continuation after the 21-mission software matrix. Normal ROM remains
`c33ec1459b3092d89f5a3b00f82f6b4dd8e59c294b479aa7d039dc7471455df7`.
Do not count any partial transfer below as a boot attempt or hardware pass.

The new experimental C# transport uses the existing ED64 X-series cmdW/cmdR/cmdt
protocol. It writes only volatile cartridge ROM space, reads bytes back against
the exact SHA-checked source ROM, and pings between transactions. A start command
is sent only after all 33554432 bytes match. There is no FPGA/firmware/N64-RAM
write. Only COM3, the saved FTDI device, is opened. A self-test checks packet
bytes, sector alignment rejection and SHA256 without accessing a device.

The separate hidden PowerShell worker owns uploader/capture processes and a
bounded test of exact Kasa **Plug 1**, with OFF and status verification in finally.
The unrelated **N64** outlet is not queried or toggled. External time limits
cover a hung driver/port close. Readback success and process exit are separate
from video evidence. No helper currently implies a game pass from a loader exit.

| Run | Authoritative result |
| --- | --- |
| v86b-verified-probe1 / tool v1 | With 12-second boot dwell, read-only ping times out before any ROM writes. Port closes and process returns 1. |
| v86b-verified-probe2 / tool v2 | With 35-second dwell, ping succeeds first try. 512, 4096, 65536 and 131072-byte probe blocks match exactly; process closes and exits 0. No start is sent. |
| v86b-verified-upload1 / tool v2 | 64-KiB transactions verify 6029312 bytes; the next write times out. No start. |
| v86b-verified-upload2 / tool v3 | Adds reconnects after verified idle 1-MiB boundaries. Verifies 26017792 bytes; a 4096-byte host write at 26034176 times out with partial-write extent unknown. No start. |
| v86b-verified-upload3 / tool v4 | Limits each verified transaction to one 4096-byte data write. Verifies 483328 bytes; the next read times out. No start. Fresh Elgato +5/+35/+55s frames all show the EverDrive menu. |

The delay/reconnect changes permit greater progress on some trials but do NOT
establish the root cause or a reliable transport. The 114086026-byte recording
from upload3 was visually inspected and permanently deleted, retaining three
stills, metadata and the exact identities in its inspection.md. Plug 1 was OFF
at 19:50:32 UTC and independently reported Relay: 0 at 19:50:33. No game crash
is visible in that capture. Do not diagnose the normal ROM from this result.

Transport executable SHA256 identities:

- v1: `4455c8b948ebab4f0086c84c4aa26065e233e57a5e6f1ba9aaff0a0851df0627`
- v2: `7c884727ddbb4453a698610136992162360ef59212865f8a9bfd11a7099731d3`
- v3: `5a9729f26edd84c4336c80ad2b948038c796fb2ab3cd5ea226d5b7c73abbc5fd`
- v4: `4ab8ee4ef5a04db692b3b10f99c759957de84395da86a9106feb6d0ffe71bc7c`

After upload3 cleanup, pnputil restarted only
USB\VID_0403&PID_6001\AB0NWMD3 successfully; that device and its COM3 child both
report OK. A subsequent native-prerelease-loader trial with 35-second dwell is
recorded separately; its result must be inspected, not inferred from this note.

That native trial **completed with exit0 in 36.6 seconds**. Fresh normal-ROM
Elgato frames show the Perfect Dark title (+5s), city flyover (+25s) and Joanna
on the rooftop (+55s), followed by Nintendo (+85s) and black (+110s). No crash
handler was observed in those samples. This establishes real-N64 3D intro,
not normal-ROM interactive gameplay or a demonstrated reason for the logo return.
No full-image readback is claimed for UNFLoader. Power OFF was verified at
19:58:03/19:58:04 UTC. The inspected 248081915-byte recording is deleted; five
stills, metadata and identities remain in that run's inspection.md.

## Separate gameplay diagnostic, not the normal ROM

Runtime branch diagnostics/v86b-infiltration-replay, code commit 89e484caa,
reuses the reviewed lean input/RAM-save harness atop the modern room cache.
The compiled diagnostic is `39082bc3857e1f1728e3f3dcfe2e733815774061d3b34f5469a617cb2bb09e59`,
matching ELF `a0f982ffc05213b64f43f3d8a4b300c3e0360d75741a747946b537080fb3405a`.
Input partition/presence and RAM EEPROM tests pass. No watchdog task is linked;
physical EEPROM writes are redirected to embedded stock Dark RAM and Controller
Pak/Transfer Pak writes are blocked. The V86B TEST HUD remains visible with L off.

Cold software7500 ticks reaches Infiltration on Perfect Agent, performs movement,
menu swipes, fixed-video-label visit and L toggles, then resumes 3D. Frames3900,
4800 and5700 were visually inspected. Final RAM shows phase8, one label check,
save reads56/writes24, zero OOM/cache/allocator/CPU faults and six evictions.
But the idle player then dies normally: dead2, health<0, pause3, level frame1673.
This is not a full mission or sustained-unpaused-play pass.

Hardware diagnostic1 uploaded natively and reached CI/Infiltration, but died
before the pause test. Its continuing death menus are NOT pause-blur evidence.
Both segments were inspected, 471237328 bytes deleted, stills/identities retained.

Diagnostic2 source fa662646b shortens the initial movement and adds death guards
plus HUD DEAD, without changing AI/health/difficulty/rendering/room memory.
ROM a200942799b7b9ed02b3513763dc1bc00f381ea22682f5d63b553b4a10734fc9;
ELF e348b1d7f09f946714db525434d86f791140639776acaec5642286597d21a008.
Native upload exit0 in36.8s. Fresh Elgato shows alive Infiltration/PerfectAgent,
full-screen pause blur, both menu directions, fixed640x480i label and L on/off.
The menu closes briefly to3D before enemy damage kills the unattended player;
phase99 correctly stops the replay. Do not claim a sustained-play or complete
replay pass. No exception screen observed, OOM0/BGFAIL0/EVICT6 in labelled HUD.
Matching software6000 finishes phase99/DEAD2/frame762/health<0, zero cache,
allocator or CPU faults, valid heap and640x480; final death is not hidden.
All detailed sampled-frame timing and limits are in the run inspection.md.

Worker stopped capture and confirmed Plug1OFF20:16:59/20:17:00UTC. Diagnostic2's
465302168-byte recording was inspected and permanently deleted. Only small
stills/metadata/logs remain. All three native uploads (normal, diagnostics1/2)
succeeded after the exact FTDI reset whileOFF and35s dwell; causality of either
individual change is not established. Experimental readback upload never fully
succeeded, so native uploads do not acquire a readback claim retroactively.

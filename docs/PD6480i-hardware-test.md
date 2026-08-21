# PD6480i hardware test

## Historical bootstrap candidate

- `artifacts/PD6480iperf-v2-retail-header.z64`
- Base: Perfect Dark (U) (V1.1) [!], MD5 `e03b088b6ac9e0080440efed07c1e40f`
- Candidate MD5: `daa0328540971ee5644907994437a292`
- Candidate SHA-256: `4d9dbaf2cb18ec92ca1ab3a6b3e167c0c635de7442522a3c3ba356322d1ea733`
- N64 header: `NPDE`, version `01`
- N64 header CRC1/CRC2: `0623a8f7/1eae0189`

## Loader workflow

The physical path is Kasa `Plug 1` for this N64 power, the EverDrive USB connection, and the Elgato Game Capture HD. The separately named Kasa device `N64` controls a different machine and must not be toggled. UNFLoader's EverDrive selector is `-f 3`:

```text
UNFLoader.exe -b -f 3 -r PD6480iperf-v27-fixed-game-framebuffers-retail-header.z64
```

For the v7 session, the upstream prerelease Windows x86 UNFLoader build was used. The older v2.2 executable uploaded data but did not start the ROM on this setup; the prerelease build completed the same command and booted it.

The EverDrive repository's USB loader was also used for the current candidate:

```text
usb64.exe -rom=PD6480iperf-v27-fixed-game-framebuffers-retail-header.z64 -start
```

## Current candidate

`artifacts/PD6480iperf-v27-fixed-game-framebuffers-retail-header.z64` is the current verified candidate. It keeps the performance branch, its L-trigger FPS graph, and the standalone patch's NTSC HAF1 interlaced register set, while using reserved high-memory gameplay framebuffers. Its SHA-256 is `6c5a04202b7943056e4b10151580be06cbe0dd53ff6c9ccfb7c0947c780ed4af`; the xdelta is based on Perfect Dark (U) (V1.1) [!].

## Result on 2026-08-15

After restarting Game Capture HD on the alternate USB port, `Plug 1` was power-cycled and the EverDrive USB device was present on COM3. The controller was connected. The prerelease UNFLoader completed the v7 upload, and the Elgato recording showed the boot logos followed by live 3D Perfect Dark at approximately 45–50 seconds. The black interval after the title logo was a loading interval; the game subsequently rendered normally.

The Game Capture HD application preview remained black, but its live Elgato timeshift stream contained actual decoded video. This confirms cartridge boot and video output on real hardware. The L-trigger graph was not exercised by scripted input, although the performance-branch code retaining it is present.

Evidence frames: `artifacts/PD6480iperf-v7-hardware-in-game-45s.png` and `artifacts/PD6480iperf-v7-hardware-in-game-50s.png`.

## v8/v9 follow-up on 2026-08-15

The v8 static-low two-buffer candidate was tested from a cold relay cycle with the controller connected. It reached the console crash screen on the real N64 during the same model-loading path reported on Analogue 3D; it is not a fix. Its SHA-256 is `a7c7886a80e448c4a0377e99100fdfb4130412949e028ce7f9c9d28c2a5fa172`.

The v9 candidate restores the performance branch's three-buffer VI/scheduler contract while keeping the raw-HAF 640x480i registers and static gameplay framebuffer layout. Its SHA-256 is `49f80369ce300bb4319c38a1a75505abdba29d9d661c7898345be81a04016f7a`.

The restarted Elgato path did not yield a reliable saved video frame for v9, so v9 remains a candidate for testing rather than a verified hardware result. `Plug 1` was left off after the session; the separately named `N64` device was not touched.

## v10 follow-up on 2026-08-16

v10 rounds the section-2 background allocation to the same 16-byte boundary as the DMA copy. This directly addresses the corrupted model/texture pointer pattern in the crash dump. The ROM SHA-256 is `9b721bc8088fd1f5208370c6afa5b797bb844c79a620bb2b0a125069225ab310`; the xdelta SHA-256 is `345c61cbdb981579c737dfe55195fea8462e9818ceaa19cea74d5f7946ab4d9c`.

The real-N64 attempt could not start: Game Capture HD reported `No Signal`, and Windows did not enumerate the EverDrive USB serial device that had been present during the v7 test. v10 is therefore packaged as an unverified candidate only. `Plug 1` was turned off afterward; the separately named `N64` device was not touched.

## v18 follow-up on 2026-08-17

The ED64 cable was restored and verified independently: Windows enumerated the converter and serial port as COM3, and `usb64-reconnect2m.exe -screen=...` read the EverDrive menu framebuffer successfully at approximately 797 KB/s. For this setup, N64 power is controlled only through `Plug 1`; the separately named `N64` device is unrelated and must remain untouched.

A known v7 480i control-ROM handoff completed through ED64, but the fresh Game Capture HD trace reported `RES_NO_SIGNAL` and then `Video signal lost`. Reinitialising `Plug 1` while the 480i control image was running produced no new input format or decoded frame. The v18 candidate is therefore packaged and xdelta-verified, but remains unverified on real hardware until the video path supplies a live frame. `Plug 1` was turned off afterward; the separately named `N64` device was not touched.

## Resume check after ED64 cable swap on 2026-08-17

The FTDI device was checked again after the ED64 cable was swapped back. Windows still reported instance `USB\\VID_0403&PID_6001\\AB0NWMD3` as **Disabled**, with no COM port, so no ROM was uploaded. The installed Game Capture HD application launched and the capture device was enumerated as **Started**, but its fresh trace again reported `RES_NO_SIGNAL` followed by `Video signal lost`. No Kasa relay was changed during this check.

## Source rebuild and loader retest on 2026-08-17

The v18 source tree was rebuilt with the local MIPS toolchain. The resulting `build/ntsc-final/pd.z64` is byte-for-byte identical to `artifacts/PD6480iperf-v18-raw-haf-3buf-dma-safe-retail-header.z64`:

- Size: 32 MiB
- SHA-256: `83344e1bbc296eb11e8f09e50a32d1416e63ff9ef029f787bbec9423a2debca2`

The current ED64 cable was tested with all three available upload/read paths. The prerelease UNFLoader command is `UNFLoader.exe -r <rom>`; it reported `No FTDI USB devices found`. The older `loader64.exe -v -w -f <rom>` reported `device not found`, and the ED64-X `usb64-reconnect2m.exe -screen=<file>` probe reported `EverDrive64 X-series device not found`. PnP still reports the USB converter as **Disabled**, the FTDI child as **Disconnected**, and no COM port is present. No ROM upload occurred.

Game Capture HD was restarted. Windows still enumerates `USB\\VID_0FD9&PID_0051\\110B14E2A7` as **Started**; the available capture trace ends with `Video signal lost`, and no live frame was available for this pass. No Kasa relay was changed. v18 remains source-built and xdelta-verified, but not hardware-verified.

## v19 title-allocation follow-up on 2026-08-17

The v19 source correction changes only the high-resolution title allocation and buffer rotation: two 1280x440 title buffers are allocated within the reserved stage window, while gameplay keeps the three-buffer performance path. The fresh build produced `artifacts/PD6480iperf-v19-title-2buf-gameplay-3buf-dma-safe-retail-header.z64` with SHA-256 `3f23972bb1d3b7a428b3f119c48e6b266b6be37e9197e389044c3384f140a212`. Its V1.1 xdelta decodes exactly to that ROM.

With the ED64 cable restored, the prerelease loader was run as `UNFLoader.exe -b -f 3 -r <v19-rom>` and completed the upload/PIFboot handoff. The ED64 probe then correctly disappeared because the cartridge had left the loader menu. After a 45-second wait, the live Game Capture HD graph still reported `RES_NO_SIGNAL`; a stock retail control upload produced the same capture result, so this does not distinguish the ROMs. `Plug 1` was turned off and verified off afterward; the separately named `N64` device was not touched. v19 remains unverified on real hardware because there is no visual capture evidence.

## v20 section-3 DMA follow-up on 2026-08-17

The v20 source correction retains v19 and additionally rounds the section-3 background scratch allocation to the same 16-byte boundary used by its DMA copy. The build produced `artifacts/PD6480iperf-v20-section2-section3-dma-safe-title-2buf-gameplay-3buf-retail-header.z64` with SHA-256 `9d4b9c987363fffc0d525bbcf2937217c8856a4e440d38c1cd2d596d9c011a74`; its xdelta decodes exactly to that ROM.

With `Plug 1` on, the prerelease loader completed `UNFLoader.exe -b -f 3 -r <v20-rom>` in 36.67 seconds and handed off through PIFboot. After restarting Game Capture HD, the device initialized, but both fresh format probes returned `RES_NO_SIGNAL`, followed by `Video signal lost`; no decoded live frame was available. `Plug 1` was turned off and verified off afterward. The separately named `N64` device was not accessed. v20 remains unverified on real hardware because the Elgato video path supplied no live signal.

## v20 capture-path retest on 2026-08-17

For a second v20 pass, Game Capture HD was restarted, only `Plug 1` was powered on, and the same ED64 command was run: `UNFLoader.exe -b -f 3 -r <v20-rom>`. The fresh trace again reported `RES_NO_SIGNAL` at `19:29:13`, followed by `Video signal lost` at `19:29:20`. Windows continued to enumerate the Elgato (`USB\\VID_0FD9&PID_0051\\110B14E2A7`) as present and healthy, so this remains a missing input-signal result rather than a capture-device enumeration failure. `Plug 1` was powered off and verified off afterward; the separately named `N64` device was not queried or toggled. This second pass supplies no visual boot evidence for v20.

## Clean post-upload power-cycle controls on 2026-08-17

The upload workflow was retested with the required clean boot sequence: upload through ED64, turn only `Plug 1` off and verify `Relay: 0`, wait, turn `Plug 1` on and verify `Relay: 1`, then restart Game Capture HD before sampling the native capture API.

- v20 uploaded in 35.97 seconds. The Elgato read-only probe returned `SIGNAL=0 / FORMAT=0` at 5-second intervals from `20:00:05` through `20:00:35`.
- The known-good v7 control ROM uploaded in 36.06 seconds and received the same clean power cycle. The probe again returned `SIGNAL=0 / FORMAT=0` from `20:03:24` through `20:03:59`.

Both passes ended with `Plug 1` off and verified `Relay: 0`. Since the control ROM also supplied no signal after the same clean boot sequence, these passes do not distinguish v20 from v7; current visual hardware verification remains blocked by the Elgato input path. The separately named `N64` device was not queried or toggled.

## Corrected upload semantics and control retest on 2026-08-17

The ED64 is volatile, so switching `Plug 1` off after an upload resets the cartridge to its menu. That sequence is useful for recovery/cleanup but is not a valid boot verification. The valid test sequence is: power on `Plug 1`, upload with the prerelease UNFLoader, leave power on while observing, and switch `Plug 1` off only when the test is finished.

Using that sequence, v20 uploaded successfully in 36.12 seconds. The ED64 framebuffer utility could read the menu after a reset, but after the upload/PIFboot handoff it could no longer access the loader service; this is consistent with the cartridge leaving the menu, but is not visual game evidence. Game Capture HD still returned `COUNT=1 / SIGNAL=0 / FORMAT=0` for 60 seconds. A stock Perfect Dark V1.1 control uploaded in 35.88 seconds and produced the same Elgato result. Enabling the capture application's interlaced-input flag did not change the result and was restored to its original value. The reference `usb64.exe` path reported an index error without transferring a ROM, so the prerelease UNFLoader remains the working upload path.

Both tests ended with `Plug 1` off and verified `Relay: 0`. The separately named `N64` device was not queried or toggled. v20 remains unverified on real hardware because the current Elgato path supplies no decoded signal.

## Retest after physical capture-path change on 2026-08-17

After the physical input path was changed, the corrected workflow was run again using only `Plug 1`. A framebuffer read before upload showed the EverDrive menu. The foreground prerelease UNFLoader then completed the v20 upload in 36.15 seconds. Fifteen seconds after handoff, the ED64 framebuffer utility could no longer connect and produced no image, consistent with PIFboot leaving the loader menu. This is an independent handoff indication, not visual gameplay evidence.

Game Capture HD still logged `Video signal lost` and the native probe remained `SIGNAL=0 / FORMAT=0`. `Plug 1` was turned off and verified `Relay: 0`; the separately named `N64` device was not queried or toggled. Visual confirmation of the game and L-trigger graph remains pending a live Elgato input signal.

## v27 clean power-cycle retest on 2026-08-18

The v27 candidate keeps the performance branch and 640x480i changes, while placing the gameplay framebuffers at the reserved high-memory addresses. The packaged ROM is `artifacts/PD6480iperf-v27-fixed-game-framebuffers-retail-header.z64` (SHA-256 `6c5a04202b7943056e4b10151580be06cbe0dd53ff6c9ccfb7c0947c780ed4af`); its xdelta is `artifacts/PD6480iperf-v27-fixed-game-framebuffers-retail-header.xdelta` (SHA-256 `03d979cf451c700880e0d1e968607b083a2ace3dc312d4e0a2d71ab4a9fab05`). Applying that xdelta to the V1.1 base reproduced the packaged ROM byte-for-byte.

After a full `Plug 1` off/on cycle, the ED64 enumerated as COM3. The prerelease UNFLoader command `UNFLoader.exe -b -f 3 -r <v27-rom>` completed in 36.06 seconds. The Elgato timeshift decode showed the normal RARE, Nintendo, and Perfect Dark boot sequence, followed by sustained live 3D frames through approximately 105 seconds; no crash handler appeared. The evidence was decoded from Timeshift segment `_0069.ts`. `Plug 1` was turned off and the ED64 probe then correctly reported no device. The separately named `N64` switch was not queried or toggled.

## v34 section-2 retail-bank retest on 2026-08-19

v34 keeps the retail V1.1 section-2 `+0x8000` background scratch fix and restores section 3 to its original allocation path after the v33 section-3 experiment produced no captured audio. The packaged ROM is `artifacts/PD6480iperf-v34-retail-section2-bank-safe.z64` (SHA-256 `ed6b8d244dc25b8ddde61fc33cf2edf0062642da28e03d29e1ae02841ea02e28`); its xdelta is `artifacts/PD6480iperf-v34-retail-section2-bank-safe.xdelta` (SHA-256 `d82265c78abc65106d785795a3822b6e8f4a623caa66c231ace3461e2163ff97`).

Only Kasa `Plug 1` was used for N64 power; the separately named `N64` switch was untouched. After `Plug 1` was powered on and a stale uploader process was cleared, ED64 enumerated on COM3. `UNFLoader.exe -b -f 3 -r <v34-rom>` completed the 32 MiB transfer in 36.73 seconds. Game Capture HD reported active N64 audio at approximately 8 seconds and 83 seconds after handoff, but its video pane and Timeshift video remained black/empty. This confirms the image remains alive far beyond the prior early failure, but does not provide visual gameplay or L-trigger graph evidence. No recording was made; the status frame is `artifacts/PD6480iperf-v34-elgato-83s.png`.

`Plug 1` was turned off after the observation window and the ED64 probe reported no device. The separately named `N64` switch was not queried or toggled.

## v49 VI-slot fix and hardware retest on 2026-08-20

The v49 candidate preserves the three colour framebuffers used by the current
performance merge, but changes `g_ViSlot` back to a two-entry ring. The
scheduler owns only two `OSViMode` slots; the previous modulo-3 rotation could
overwrite adjacent scheduler state on the third mode update. The packaged ROM
is `artifacts/PD6480iperf-v49-vi-slot-2-480i-performance.z64` (SHA-256
`38d1beabf0672f9e34dbe553d99473769afd17f2ba17a2b845316a5b57f10b4a`), and its
V1.1 xdelta round-trips byte-for-byte.

With only `Plug 1` powered on, the prerelease UNFLoader completed
`UNFLoader.exe -b -f 3 -r <v49-rom>` in 36.33 seconds. Game Capture HD held
`640x480p30` and active N64 audio at level 71 at approximately 18 and 56
seconds after handoff. The desktop `PrintWindow` capture remained black; the
same capture path is black for the stock/menu control, so it cannot distinguish
the ROM's video contents. No recording was made and no visual gameplay or
L-trigger graph claim is made. `Plug 1` was powered off after the observation;
the separately named `N64` switch was not touched.

## v51 v7-layout follow-up on 2026-08-20

v51 keeps v50's raw-HAF 640x480i registers and retail V1.1 section-2 scratch
fix, but restores the two-buffer stage allocation and VI unblank timing from
the v7 layout that reached live 3D on real N64 hardware. The packaged ROM is
`artifacts/PD6480iperf-v51-v7-layout-section2-safe.z64` (SHA-256
`8d6697fce38641fc6f2b45a3d74c655d5f259d94f7f73d913464ce97048a7449`),
and its base-specific xdelta round-trips byte-for-byte.

This candidate has not yet been uploaded. At the time of packaging, Kasa
`Plug 1` was offline, so the ED64 was unavailable and Elgato correctly showed
no signal. The separately named `N64` switch was not accessed.

## v52 performance-memory follow-up on 2026-08-20

v52 restores the performance branch's global `FRAMEBUFFER_SIZE` reservation
for boot, stack, and memory-pool boundaries while keeping a dedicated 640x480
colour-buffer size in the 480i VI path. The packaged ROM is
`artifacts/PD6480iperf-v52-perf-memory-reservation-480i.z64` (SHA-256
`7bef1bd3618b20d56ae364ca8f7a12836f9559c1e4135b5c512b65fe28b830c4`), and its
base-specific xdelta round-trips byte-for-byte.

Hardware testing is pending. The test must use Kasa `Plug 1` for the N64,
the ED64 USB path for upload, and Elgato for post-handoff video. The separately
named `N64` switch is not part of this workflow.

## v59 native-hires hardware verification on 2026-08-20

v59 is the current verified candidate:

* ROM: `artifacts/PD6480iperf-v59-hires-old-working.z64`
* ROM SHA-256: `97B0C9FD5E5216B42CFFC1A531F115581AC4FD66FABAAC148AB53EE17F9A635E`
* xdelta: `artifacts/PD6480iperf-v59-hires-old-working.xdelta`
* xdelta SHA-256: `9947F048B899E2DC0DEF22416F3A49424104077013C90B0D309BFE11D51473D3`

The ROM uploaded successfully through ED64 in 36.33 seconds with only Kasa
`Plug 1` powering the test N64. After waiting at least 65 seconds after the
upload handoff, the Elgato flashback contained the N64 logo, Perfect Dark logo,
and live 3D gameplay. The extracted live-gameplay frame is
`artifacts/PD6480iperf-v59-live-gameplay.png`.

The test recording was deleted after extraction. `Plug 1` was powered off at
the end of the test; the separately named `N64` switch was not touched.

The v60-v62 newer-`pd-perf` source-line variants were hardware-tested and each
produced uniform black after handoff. They are not release candidates. The
newer source line removed the high-resolution-aware renderer paths, so a
VI-width/buffer-only change cannot reproduce v59's working high-resolution
path.

## v69 640x480i resolution correction on 2026-08-20

The v59 source was audited against the supplied standalone 640x480i patch. Its
working path is 640x220 with NTSC LAN1 timing, so its live gameplay is not the
same resolution/timing as the standalone patch. v69 changes only the v59
resolution path: the high-resolution mode is 640x480, its mode selector enters
`VIMODE_HI`, and the existing NTSC HAF1 path is used for gameplay. The gameplay
buffers are enlarged to the matching 640x480 layout. The L-trigger FPS graph
and v59 performance code remain unchanged.

The packaged files are:

* `artifacts/PD6480iperf-v69-v59-hires-haf1-480i.z64`
* `artifacts/PD6480iperf-v69-v59-hires-haf1-480i.xdelta`

The ROM SHA-256 is
`941859DDEFE5C5E51CD818A64C4293176BBC07912ABCACAAD020D882B6DC87C8`; the
xdelta SHA-256 is
`A5248FFD42C35F7880D5C8E9277045C589B9629D5379C0F1B219AEF9DA75DE5B`.
The xdelta was decoded against `Perfect Dark (U) (V1.1) [!].z64` and reproduced
the ROM byte-for-byte.

The attempted console handoff did not constitute a hardware test. Only Kasa
`Plug 1` was power-cycled; the separately named `N64` switch was not touched.
Windows had no present FTDI/ED64 COM device, and both the installed and
prerelease UNFLoader attempts exited without transferring a ROM. A PnP rescan
did not restore the device, so there is no post-handoff Elgato result to report.
`Plug 1` was turned off afterward and no recording was created.

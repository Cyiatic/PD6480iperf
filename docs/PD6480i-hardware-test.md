# PD6480i hardware test

## Candidate

- `artifacts/PD6480iperf-v2-retail-header.z64`
- Base: Perfect Dark (U) (V1.1) [!], MD5 `e03b088b6ac9e0080440efed07c1e40f`
- Candidate MD5: `daa0328540971ee5644907994437a292`
- Candidate SHA-256: `4d9dbaf2cb18ec92ca1ab3a6b3e167c0c635de7442522a3c3ba356322d1ea733`
- N64 header: `NPDE`, version `01`
- N64 header CRC1/CRC2: `0623a8f7/1eae0189`

## Loader workflow

The physical path is the Kasa Plug 1 power switch, the EverDrive USB connection, and the Elgato Game Capture HD. UNFLoader's EverDrive selector is `-f 3`:

```text
UNFLoader.exe -b -f 3 -r PD6480iperf-v2-retail-header.z64
```

For the v7 session, the upstream prerelease Windows x86 UNFLoader build was used. The older v2.2 executable uploaded data but did not start the ROM on this setup; the prerelease build completed the same command and booted it.

The EverDrive repository's USB loader was also used for the current candidate:

```text
usb64.exe -rom=PD6480iperf-v2-retail-header.z64 -start
```

## Current candidate

`artifacts/PD6480iperf-v7-raw-haf-2buf-retail-header.z64` is the verified candidate. It keeps the performance branch and 640x480 framebuffer changes, uses the standalone patch's NTSC HAF1 interlaced register set, and matches its two-framebuffer layout. Its SHA-256 is `b1e95594dfe7197ba407af0616ad9ab2bb36f841fbfe93983101b7ce91fee19b`. The xdelta is based on Perfect Dark (U) (V1.1) [!].

## Result on 2026-08-15

After restarting Game Capture HD on the alternate USB port, both Kasa relays were power-cycled and the EverDrive USB device was present on COM3. The controller was connected. The prerelease UNFLoader completed the v7 upload, and the Elgato recording showed the boot logos followed by live 3D Perfect Dark at approximately 45–50 seconds. The black interval after the title logo was a loading interval; the game subsequently rendered normally.

The Game Capture HD application preview remained black, but its live Elgato timeshift stream contained actual decoded video. This confirms cartridge boot and video output on real hardware. The L-trigger graph was not exercised by scripted input, although the performance-branch code retaining it is present.

Evidence frames: `artifacts/PD6480iperf-v7-hardware-in-game-45s.png` and `artifacts/PD6480iperf-v7-hardware-in-game-50s.png`.

## v8/v9 follow-up on 2026-08-15

The v8 static-low two-buffer candidate was tested from a cold relay cycle with the controller connected. It reached the console crash screen on the real N64 during the same model-loading path reported on Analogue 3D; it is not a fix. Its SHA-256 is `a7c7886a80e448c4a0377e99100fdfb4130412949e028ce7f9c9d28c2a5fa172`.

The v9 candidate restores the performance branch's three-buffer VI/scheduler contract while keeping the raw-HAF 640x480i registers and static gameplay framebuffer layout. Its SHA-256 is `49f80369ce300bb4319c38a1a75505abdba29d9d661c7898345be81a04016f7a`.

The restarted Elgato path did not yield a reliable saved video frame for v9, so v9 remains a candidate for testing rather than a verified hardware result. Both Kasa relays were left off after the session.

## v10 follow-up on 2026-08-16

v10 rounds the section-2 background allocation to the same 16-byte boundary as the DMA copy. This directly addresses the corrupted model/texture pointer pattern in the crash dump. The ROM SHA-256 is `9b721bc8088fd1f5208370c6afa5b797bb844c79a620bb2b0a125069225ab310`; the xdelta SHA-256 is `345c61cbdb981579c737dfe55195fea8462e9818ceaa19cea74d5f7946ab4d9c`.

The real-N64 attempt could not start: Game Capture HD reported `No Signal`, and Windows did not enumerate the EverDrive USB serial device that had been present during the v7 test. v10 is therefore packaged as an unverified candidate only. Both Kasa relays were turned off afterward.

## v18 follow-up on 2026-08-17

The ED64 cable was restored and verified independently: Windows enumerated the converter and serial port as COM3, and `usb64-reconnect2m.exe -screen=...` read the EverDrive menu framebuffer successfully at approximately 797 KB/s. The N64 was power-cycled through the N64 Kasa relay and the capture path was power-cycled through Plug 1.

A known v7 480i control-ROM handoff completed through ED64, but the fresh Game Capture HD trace reported `RES_NO_SIGNAL` and then `Video signal lost`. Reinitialising Plug 1 while the 480i control image was running produced no new input format or decoded frame. The v18 candidate is therefore packaged and xdelta-verified, but remains unverified on real hardware until the video path supplies a live frame. Both Kasa relays were turned off afterward.

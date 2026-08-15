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

The EverDrive repository's USB loader was also used for the current candidate:

```text
usb64.exe -rom=PD6480iperf-v2-retail-header.z64 -start
```

## Result on 2026-08-15

After restarting Game Capture HD on the alternate USB port, both Kasa relays were power-cycled and the EverDrive returned `ED64 found at port COM3`. The source-built candidate uploaded and started through `usb64` successfully at approximately 917 KB/s.

The Game Capture HD application preview remained black, but its live Elgato timeshift stream contained actual decoded video. A frame extracted from the candidate's stream shows Perfect Dark running on the N64 with the in-game message `no controller in controller socket 1 - please power off and attach a controller`. This confirms cartridge boot and video output on real hardware. The L-trigger graph was not exercised because no controller was connected.

Evidence frame: `artifacts/PD6480iperf-hardware-boot-no-controller.png`.

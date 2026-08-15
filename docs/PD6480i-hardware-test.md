# PD6480i hardware test

## Candidate

- `artifacts/PD6480iperf-minimal-retail-header.z64`
- Base: Perfect Dark (U) (V1.1) [!], MD5 `e03b088b6ac9e0080440efed07c1e40f`
- Candidate MD5: `b39bfd8c348529b8a76c1775a7ae508e`
- Candidate SHA-256: `1a6a9132b2a9e8170e9841eaa1a42c9aed33cc13980eff83ed883446d33cc2ac`
- N64 header CRC1/CRC2: `5cea4e57/522f0b42`

## Loader workflow

The physical path is the Kasa Plug 1 power switch, the EverDrive USB connection, and the Elgato Game Capture HD. UNFLoader's EverDrive selector is `-f 3`:

```text
UNFLoader.exe -b -f 3 -r PD6480iperf-minimal-retail-header.z64
```

## Result on 2026-08-15

UNFLoader returned exit code 0 for the candidate upload. The Elgato detected a live `640x480p30` signal and active game audio, but the video image remained completely black at 5 and 15 seconds after boot.

As a control, the untouched CRC-valid retail ROM was also uploaded with exit code 0 after Plug 1 reset; it produced the same black Elgato image. The EverDrive USB returned to its menu-side state after Plug 1 reset, but no visible menu or in-game frame was captured. This leaves the current hardware video path unresolved; the candidate is not cleared for Analogue testing yet.

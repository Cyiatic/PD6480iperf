# PD6480i hardware test

## Candidate

- `artifacts/PD6480iperf-v2-retail-header.z64`
- Base: Perfect Dark (U) (V1.1) [!], MD5 `e03b088b6ac9e0080440efed07c1e40f`
- Candidate MD5: `daa0328540971ee5644907994437a292`
- Candidate SHA-256: `4d9dbaf2cb18ec92ca1ab3a6b3e167c0c635de7442522a3c3ba356322d1ea733`

## Loader workflow

The physical path is the Kasa Plug 1 power switch, the EverDrive USB connection, and the Elgato Game Capture HD. UNFLoader's EverDrive selector is `-f 3`:

```text
UNFLoader.exe -b -f 3 -r PD6480iperf-v2-retail-header.z64
```

## Result on 2026-08-14

UNFLoader returned exit code 0 for the candidate upload. The Elgato detected a live `640x480p30` signal and active game audio, but the video image remained completely black through the boot wait. This is a hardware-test failure for the current candidate; it has not been cleared for Analogue testing.

The untouched retail control-ROM upload was attempted after a Plug 1 power cycle but did not complete because the EverDrive was not at its main menu. That control comparison remains pending.

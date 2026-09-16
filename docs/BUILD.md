# Runtime source and build guide

[Project home](../README.md) · [Install an existing patch](INSTALL.md)

## Choose the right branch

The default `mods/performance` branch is the distribution/evidence branch. Its historical `src/` tree is **not the source of v87**.

| Source checkpoint | Commit |
| --- | --- |
| Newer performance base in public history | `d88dc100ef00e11d3c633cb384d4c51169b17b7d` |
| v86g parent runtime in public history | `9bce9e60addc08b3b658fb0224621f32a99f1bdd` |
| Maintained v87 source, branch `fix/v87-camspy-480i` | `82d704d0154ea86f9e5d0fb98541907806f31960` |

v87 changes only `src/game/bondview.c` at runtime relative to v86g; its additional documentation and source-test harness are not runtime changes. [Pinned source](https://github.com/Cyiatic/PD6480iperf/tree/82d704d0154ea86f9e5d0fb98541907806f31960).

The original release commit `d533653ca...` maps to sanitized commit `802059812519fef5d08c8f8e4ba86ff033c296ac`. The maintained pin above adds documentation, ignore rules and a corrected negative-control parent lookup only. Game-source blobs are identical. The unchanged release manifests retain their original IDs; use the [commit map](PUBLIC_RELEASE.md#source-identity).

Use a separate checkout instead of switching a dirty distribution checkout:

```powershell
git clone --branch fix/v87-camspy-480i --single-branch https://github.com/Cyiatic/PD6480iperf.git PD6480iperf-runtime-v87
Set-Location PD6480iperf-runtime-v87
git checkout --detach 82d704d0154ea86f9e5d0fb98541907806f31960
git status --short
```

No private-repository access is required. Detaching pins the documented source; create your own branch before making new work.

## Known Windows build environment

The release was built with native MIPS GCC/binutils, native make using BusyBox `sh`, Python 3, a host GCC/`cpp`, gzip and the MSYS runtime on PATH.

Tools inspected on the development host for this guide:

- MIPS GCC **12.2.0**, executable prefix `mips64-elf`.
- Python **3.12.14**.
- Host GCC **16.1.0** (MSYS2 MinGW).
- Native `make.exe` and `busybox.exe` supplied with the MIPS tool bundle.
- MSYS `usr/bin` for runtime DLLs and supporting utilities.

These are inspected host versions, not a complete dependency lockfile or a newly reproduced clean-room build. The recorded release build succeeded; compiler/package drift can affect byte identity. A Linux or other-host recipe has not been revalidated for this release.

Set these example paths to your installed tools:

```powershell
$pdPython = 'C:/tools/python/python.exe'
$pdMipsBin = 'C:/tools/mips/bin'
$pdHostBin = 'C:/msys64/mingw64/bin'
$pdMsysBin = 'C:/msys64/usr/bin'
$env:PATH = "$pdMipsBin;$pdHostBin;$pdMsysBin;$env:PATH"
$env:ROMID = 'ntsc-final'
```

Keep the native MIPS bundle first so `make.exe` resolves to the intended native make. Verify `mips64-elf-gcc`, `make.exe`, `busybox.exe`, `gcc`, `cpp` and `gzip` resolve before building. Do not substitute an unrelated compiler simply because it has the same executable name.

## Extract and build

In the fresh runtime checkout, place your verified clean USA v1.1 big-endian ROM at `pd.ntsc-final.z64`. Its SHA-256 must be:

```text
4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21
```

Then:

```powershell
& $pdPython tools/extract
if ($LASTEXITCODE -ne 0) { throw 'Asset extraction failed' }

make.exe -j4 'SHELL=busybox.exe sh' HOST_EXE=.exe MIPS_BINUTILS_PREFIX=mips64-elf "PYTHON=$pdPython" ROMID=ntsc-final rom
if ($LASTEXITCODE -ne 0) { throw 'ROM build failed' }
```

The Makefile defaults to nonmatching GCC (`MATCHING=0`, `COMPILER=gcc`, `-Os`). The host `mkrom` helper is built from `tools/mkrom/`; keep its runtime dependencies available. A historical packaging failure was a missing `msys-2.0.dll`; adding the correct MSYS `usr/bin` resolved it.

The public repository does not bundle `tools/gzip` or the legacy `tools/irix/` binaries. Install gzip on PATH and obtain your build dependencies separately. The current asset tool already prefers gzip on PATH. This publication pass re-ran the CamSpy source regression test, not a clean-room ROM rebuild.

Outputs include `build/ntsc-final/pd.z64`, `stage1.elf` and `pd.map`. Extracted assets and full ROMs remain local. Do not commit them.

## Header normalization and exact identity

The build's source header uses the upstream ED/save identifier. The released candidate instead uses the USA1.1 retail identifier. [The normalization helper](../tools/normalize_pd_retail_header.py), on the **distribution branch**, changes only offsets `0x3c` and `0x3f`; the ROM body and N64 CRC fields are unchanged.

| Output | Recorded SHA-256 |
| --- | --- |
| Source-header ROM | `91d16398c307b3f4ad597ee8bab2924be4bf821f218caa014d3034b1b947ebc9` |
| Retail-header candidate | `04275ac845eeae6dd22358fefd9bfdd0bdcb28d4cfcac3ee57264dbfc9f2785b` |
| `stage1.elf` | `f23de5f65bfa0e366e49a891752360ff082f1b4c5102d0403ecdb2c351f46f4b` |
| Compiled v6 inspection layout | `a62708d1ec9097dc0688cd43aff0b594513b7b7af92cf6cf6dcd6d590c5aabdd` |

For the unchanged release, point `$pdDistribution` to your separate distribution checkout:

```powershell
$pdDistribution = 'C:/work/PD6480iperf-distribution'
New-Item -ItemType Directory -Path .codex-work -Force | Out-Null
& $pdPython "$pdDistribution/tools/normalize_pd_retail_header.py" build/ntsc-final/pd.z64 .codex-work/v87-retail.z64 --source-sha256 91d16398c307b3f4ad597ee8bab2924be4bf821f218caa014d3034b1b947ebc9
```

Create the output directory first; the helper refuses to overwrite its output and rejects a source-hash mismatch. A differently rebuilt ROM is not the authenticated v87 artifact. For intentional new source changes, assign a new candidate/version and revalidate it rather than weakening the old release's hash check.

## Focused checks

The CamSpy source test belongs to the runtime branch. It requires native GCC, the v86g parent in Git history, and a **new** output directory:

```powershell
& $pdPython tools/test_eyespy_480i.py --source . --cc "$pdHostBin/gcc.exe" --out .codex-work/camspy-source-check
```

Expected: 193,800 cases pass and the original radius negative control exits 17. This extracts actual source functions into a recording graphics-argument shim; it is not an RDP or console test.

The distribution branch's [compressed-asset auditor](../tools/audit_rom_assets.py) accepts the candidate ROM as a positional argument. Expected v87 result: 1,403 valid compressed assets, zero invalid streams; 608 raw assets are unchecked.

For emulator provenance use the matching ELF and freshly compiled layout with the [modern inspection tools](../tools/emulator/README.md). Some old generic auditors assume symbols or dynamic-buffer layouts absent from the modern runtime; do not treat those incompatibilities as passed checks.

For patch verification, decode onto the clean base and compare the output to the retail-header hash in [Install](INSTALL.md). Keep the existing v87 patch, save, manifest and ZIP immutable. A documentation edit requires link/hash checks, not a new console run.

## Repository maintenance

Use a fresh clone of **https://github.com/Cyiatic/PD6480iperf.git**. Old development checkouts contain pre-cleanup history and may have an `origin` pointing at Ryan Dwyer's upstream; inspect `git remote -v` and do not push project artifacts upstream.

Do not merge or force-push an old private branch into the public repository. Transfer reviewed changes as patches or cherry-pick isolated commits onto the cleaned history. The original working folders and private backup were not erased.

Stage only reviewed paths and use normal fast-forward pushes. Preserve provenance and failed controls. Keep ROMs, extracted assets, states, recordings, host binaries and credentials out of new commits; ignore rules alone are not a history audit.

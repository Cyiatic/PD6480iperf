# Runtime source and build guide

[Project home](../README.md) · [Install an existing patch](INSTALL.md)

## Choose the right branch

The default `mods/performance` branch is the distribution/evidence branch. Its historical `src/` tree is **not the source of either current edition**.

| Source checkpoint | Commit |
| --- | --- |
| Newer performance base in public history | `d88dc100ef00e11d3c633cb384d4c51169b17b7d` |
| v86g parent runtime in public history | `9bce9e60addc08b3b658fb0224621f32a99f1bdd` |
| Maintained v87 source, branch `fix/v87-camspy-480i` | `82d704d0154ea86f9e5d0fb98541907806f31960` |
| v88 no-graph source, branch `fix/v88-stock-controls-480i` | `cb4e30de6433bbd4cc47e4f0b739700db15efb96` |

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

## v88 no-graph alternative

v88 restores stock L/D-pad inputs and removes graph processing. Its branch
contains the source, focused input tests, evidence and release packaging.
The `v88-no-graph` release tag points to its packaging commit; runtime source
is pinned above. Later packaging commits do not change `src/`.

```powershell
git clone --branch fix/v88-stock-controls-480i --single-branch https://github.com/Cyiatic/PD6480iperf.git PD6480iperf-runtime-v88
Set-Location PD6480iperf-runtime-v88
git checkout --detach cb4e30de6433bbd4cc47e4f0b739700db15efb96
```

For a linked worktree, disable inherited sparse checkout before extracting.
Supply the same clean USA v1.1 base and run `tools/extract`. The successful
v88 host used MIPS GCC 12.2.0 with native make, **MSYS bash rather than the old
BusyBox shell**, and MSYS utilities ahead of stale BusyBox aliases:

```powershell
# Set $pdPython and your compiler/PATH locations as described below first.
& $pdPython tools/extract
if ($LASTEXITCODE -ne 0) { throw 'Asset extraction failed' }
make.exe -j4 SHELL=C:/msys64/usr/bin/bash.exe MAKE=make.exe HOST_EXE=.exe MIPS_BINUTILS_PREFIX=mips64-elf "PYTHON=$pdPython" ROMID=ntsc-final rom
if ($LASTEXITCODE -ne 0) { throw 'ROM build failed' }
& $pdPython tools/test_stock_controls.py --source .
```

**Reproduction limit:** this build reused the archived original `mkrom.exe`;
the unmodified helper's `crypt.h` dependency remains a clean-toolchain gap.
It is not distributed. The preliminary v87 rebuild matched all 8,443 readable
matching symbols but differed in two compressed asset streams that decompressed
identically. Neither that rebuild nor v88 should be assigned v87's release hash.
See [v88 build provenance and tests](V88_NO_GRAPH.md) for details.

| v88 output | Recorded SHA-256 |
| --- | --- |
| Source-header ROM | `2d418f2a010eb99d3d36cf1d28df6494236f70dd89c7562d8b13b3fa51ea0cc9` |
| Retail-header candidate | `7971eb42e66ba1d5773e7a5c557f4ea578e7800e862f350b2ce5908b21223891` |
| `stage1.elf` | `7a8873ebae5626c6e02ea76c64c4bc45a4d80055991728da8638bc947bb40e8b` |

Use the same header-normalization helper described below with **v88's**
source-header hash and a new output filename. Decode the released xdelta onto
the clean base to verify the exact retail-header candidate. Patch/save/ZIP
hashes are in [Install](INSTALL.md); v88's Analogue testing is pending.

## Recorded v87 Windows build environment

The v87 release was built with native MIPS GCC/binutils, native make using BusyBox `sh`, Python 3, a host GCC/`cpp`, gzip and the MSYS runtime on PATH. The following historical recipe and output hashes refer to v87; use the v88 adjustments above for that edition.

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

## v87: extract and build

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

## v87: header normalization and exact identity

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

For patch verification, decode onto the clean base and compare the output to the edition's retail-header hash in [Install](INSTALL.md). Keep published patch/save/manifest/ZIP assets immutable. A documentation edit requires link/hash checks, not a new console run.

## Repository maintenance

Use a fresh clone of **https://github.com/Cyiatic/PD6480iperf.git**. Old development checkouts contain pre-cleanup history and may have an `origin` pointing at Ryan Dwyer's upstream; inspect `git remote -v` and do not push project artifacts upstream.

Do not merge or force-push an old private branch into the public repository. Transfer reviewed changes as patches or cherry-pick isolated commits onto the cleaned history. The original working folders and private backup were not erased.

Stage only reviewed paths and use normal fast-forward pushes. Preserve provenance and failed controls. Keep ROMs, extracted assets, states, recordings, host binaries and credentials out of new commits; ignore rules alone are not a history audit.

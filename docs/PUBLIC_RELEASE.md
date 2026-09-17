# Public-release audit and migration

[Project home](../README.md) · [Build guide](BUILD.md)

Cleanup performed September 15, 2026 (America/Phoenix). This is a repository-publication change, **not a new game candidate**. The v87 patch, Dark save, release ZIP and game-source blobs remain unchanged.

This page records that original cleanup. The subsequent **September 17 v88
no-graph publication** is a separate source candidate based on the sanitized
v87 history, not another history rewrite. Its new source branch, patch and
test limits are documented in [v88 notes](V88_NO_GRAPH.md). The v87 release
assets and tag remain unchanged; only its release notes gain a cross-link.

## What was removed

The complete history of all **41 branches** was inspected, not just the default branch's latest files.

- **20 distinct full 32 MiB ROM blobs**, previously represented by 24 tracked ROM paths.
- Bundled `tools/gzip` and legacy `tools/irix/` toolchain payloads, including 31 detected executable blobs. Install external build dependencies instead.
- An empty historical file whose entire name was one space; Windows Git rejected it during import.
- ROM/capture/state filename patterns were excluded across history as a further guard.

The filtered payload audit found **zero ROM/capture/state payloads and zero bundled executables**. Seven historical patch/save ZIPs were inspected: their contents are patches, EEPROM saves, README files and manifests, not full ROMs.

Preserved: source and authorship/history, branch names, patches, stock-format Dark saves, screenshots, findings and small ABI-layout evidence. Two layout binaries (104 and 148 bytes) are inspection structures, not RAM dumps. All 41 filtered branch tips were compared against their original tips; no other file-content or mode differences were found.

## Credential review

Gitleaks 8.30.1 scanned all 6,892 original commits (about 2.23 GB of diff content). It reported one generic-key match in an assembly instruction changing a game character's hidden flag.

This is game assembly, not an API key. The exact sanitized commit/file/rule/line is documented in [the narrow ignore entry](../.gitleaksignore); no credential rule or entire source directory is disabled. The final rewritten-history scan covered 6,893 commits and about 2.38 GB of diff content and reported no remaining findings with that exact allowance. It uses `--no-renames` to avoid the baseline's rename-detection limit warning. Subsequent publication-only commits are scanned separately.

Automated scanning and manual review are useful checks, not a guarantee against every possible encoding or credential format.

## Source identity

| Checkpoint | Original private-history ID | Sanitized public-history ID |
| --- | --- | --- |
| Newer performance base | `bf3245076d00fbbb29ca1e0906672381f2d43a52` | `d88dc100ef00e11d3c633cb384d4c51169b17b7d` |
| v86g runtime | `26cb92ae9d0ae2cba172999c0d5c1762f32d5a50` | `9bce9e60addc08b3b658fb0224621f32a99f1bdd` |
| v87 runtime | `d533653ca75d98a875bac28a0369a2b33c5abc3d` | `802059812519fef5d08c8f8e4ba86ff033c296ac` |
| Logo/disclosure distribution snapshot | `73de8d4934358858466e83854dc93dec5596c46b` | `12812e6e32c45c1ed5fa96c118bc7b01e7860937` |

The [complete original-to-filtered commit map](public-history-commit-map.txt) preserves the lookup for old IDs in dated evidence and immutable package manifests. Those documents were not rewritten to pretend they were produced after publication.

The maintained runtime source pin is **`82d704d0154ea86f9e5d0fb98541907806f31960`**. Its only changes after the sanitized v87 commit are the source test's v86g lookup, README guidance and ignore rules. No game code changed. The updated actual-C CamSpy test again passes **193,800 cases**, with the old-radius negative control failing as expected. Fresh-checkout line endings can change a working-file hash; Git source-blob identity was compared independently.

A clean-room ROM rebuild was not performed for this publication-only update. The existing release hashes and ZIP entries were reverified; see [Install](INSTALL.md).

## Why a fresh public repository?

Untracking a ROM does not remove it from history. A history rewrite alone also does not guarantee that old objects cached by a hosting service become inaccessible. [GitHub documents that limitation](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository).

The owner retains both an integrity-checked local mirror and the original remote repository as a **private archive**. Only the filtered history is pushed to a fresh repository, then published at the original **Cyiatic/PD6480iperf** URL. No issues, pull requests or release objects required migration.

Local ROMs, old development folders and pre-existing uncommitted changes were not deleted. The private archive is not linked as a public download. No original-N64 power, upload or recording was needed for publication.

## Existing-clone migration

Use a fresh clone from `https://github.com/Cyiatic/PD6480iperf.git`.

Do **not** merge, mirror-push or force-push old private history into the public repository. Transfer only reviewed new work as patches or isolated cherry-picks onto the sanitized branch. An old source hash may need translating through the commit map.

The default branch remains `mods/performance`; buildable current runtime remains on `fix/v87-camspy-480i`. Retained experiment/diagnostic branches are historical references, not additional recommended releases.

## Repeating the checks

```powershell
New-Item -ItemType Directory -Path .codex-work -Force | Out-Null
python tools/publication/audit_git_payloads.py . --out .codex-work/publication-payload-audit.json
gitleaks git . --log-opts='--all --no-renames' --ignore-gitleaks-allow --gitleaks-ignore-path=.gitleaksignore --redact=100
```

The payload auditor checks reachable Git filenames, non-source payload magic and ZIP contents. It is not a full license analyzer or replacement for source review. Keep audit scratch files and host executables local. GitHub Actions are disabled for initial publication; no unattended ROM build or secret-dependent workflow is enabled.

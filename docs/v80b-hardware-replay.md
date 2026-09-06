# V80B hardware replay diagnostic

This branch remains **diagnostic-only**. Relative to `diagnostics/v79-console-replay`
(`72c02046c9`), it applies the same `main.c` / `sched.c` changes as normal v80b
source `c76b706cbba427324698d4bbc65b7fc74d437528`. A source diff confirms those
two files match the normal candidate exactly.

The RAM-only Dark save and synthetic input replay are unchanged. A shorter
medium-font yellow `V80B TEST P... / HI ... CHECK ...` label distinguishes fresh
v80b recordings from the earlier diagnostic. No diagnostic input/save hooks or
label are included in the normal v80b ROM.

ROM `PD6480iperf-v80b-HW-REPLAY-NOT-RELEASE.z64`:
SHA256 `4379810d596b620325dd78448125959ad9d368cccaa3ac90547bbc923f0cc377`.
ELF SHA256 `d6ae2bfb028ce2f094d39d9554413ce3f36e579c67c676f7c56aa39e608c3ef9`.
CRC1/CRC2 `ceb9e53a` / `87bdebf9`.

Static checks confirm the physical pak-write blocker and RAM EEPROM shim, both
640x480 modes and the full colour/depth allocations. See
`docs/PD6480iperf-v80b.md` and `artifacts/tests/v80b/` on the distribution branch
for completed runtime evidence and limitations. This branch must not be merged
into a normal candidate or represented as unchanged-ROM acceptance.

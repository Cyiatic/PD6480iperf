# Newer pd-perf lineage gap audit

> Historical scope: this September 5 audit describes v79/v80b, not v87.
> v81 and later start from the newer bf3245076 source directly. The missing-
> commit statuses and proposed Hi-Res UI below are superseded; see the
> [current findings](FINDINGS.md) and [runtime source guide](BUILD.md).

Working audit, 2026-09-05. The v79/v80b development-candidate source is based on
`f96d9ff901fc96a0c42b7010dd2cdf89ac5b16c2` (May 2, 2023). The local source used
for the supplied newer pd-perf comparison ends at
`bf3245076d00fbbb29ca1e0906672381f2d43a52` (May 19, 2023). Git identifies f96d9ff
as their merge base, with **75 later commits**. v79 must not be described as
preserving every optimization or fix in that newer patch.

The older core still includes compiled ASM AI, unpacked pads, weapon preloading,
GCC size optimization, the L graph and other performance work already present
at f96d9ff. Whole-level room preloading was disabled to fit the full 640x480
colour and depth buffers; the replacement bounded/adaptive cache is not full
preload parity. Neither a boot pass nor the L graph proves a performance gain.

The ledger below records source inclusion, not pass/fail judgments about the
upstream changes. 'Not integrated/reviewed' is an open requirement assessment,
not a decision to drop the improvement. Adapt compatible optimizations while
preserving true 640x480i, toggle-safe Hi-Res, save compatibility, and validated
original-N64 operation. Changes tied to the newer triple-buffer memory/scheduler
model need integration work, not blind cherry-picking. Benchmarks and Analogue
verification remain open.

| Upstream commit | Change | Current status |
| --- | --- | --- |
| `60947bfdf` | Remove hi-res video option | Conflicts with requested Hi-Res UI; retain fixed-480i, toggle-safe option. |
| `fcc63f763` | Set Everdrive ROM ID and save configuration in the ROM header | Header differs deliberately for retail/ED64/Analogue title identification; validate save behavior. |
| `7ef3e9d00` | Introduce triple buffer and remove RDP freeze | Not carried over: triple-buffer memory cost and scheduler integration require adaptation. |
| `a85ea9d7c` | Make main thread start building second task without waiting for retrace | Not integrated/reviewed in current candidate. |
| `880db1568` | Move framebuffers to separate memory banks | Not carried over as a complete change; framebuffer bank placement remains to assess. |
| `f54c812fd` | Fix two profiling bugs | Not integrated/reviewed in current candidate. |
| `6b016ffd4` | Show bottleneck on profile output | Not integrated/reviewed in current candidate. |
| `e423eac69` | Make scheduler pass message IDs instead of pointers | Not integrated/reviewed in current candidate. |
| `4acb095c6` | Joy: Don't block if there's no read data | Not integrated/reviewed in current candidate. |
| `039469fcd` | Update roommtx function names to same ones used in master | Not integrated/reviewed in current candidate. |
| `b1516774d` | Fix room matrix bug | Not integrated/reviewed in current candidate. |
| `c3c2617e7` | Optimise room mtx functions | Not integrated/reviewed in current candidate. |
| `681fc1111` | Avoid iterating stage table where possible | Not integrated/reviewed in current candidate. |
| `9a56b3ce3` | Fix random aimer taps when there's no controller samples | Not integrated/reviewed in current candidate. |
| `09d6ccae4` | Remove unused code from joy.c | Not integrated/reviewed in current candidate. |
| `261be8d70` | Improve roomproplist code | Not integrated/reviewed in current candidate. |
| `e0236c3cb` | Make profiler use thread-specific cycle counts for page 2 metrics | Not integrated/reviewed in current candidate. |
| `870f090b8` | Fix wrong arguments to model00018680 | Not integrated/reviewed in current candidate. |
| `863b5d7da` | Fix early mine detonation in G5 Building | Not integrated/reviewed in current candidate. |
| `414c2c6b1` | Replace objFindByTagId with a direct array lookup | Not integrated/reviewed in current candidate. |
| `726ac90f4` | Use uncached memory for gfx data writes | Not integrated/reviewed in current candidate. |
| `86feae85c` | Remove unused global variables | Not integrated/reviewed in current candidate. |
| `c9879d951` | Use inline sqrt.s instruction | Not integrated/reviewed in current candidate. |
| `9692b51a0` | Fix sqrtf in ailist files | Not integrated/reviewed in current candidate. |
| `d16ea9cef` | Make functions static where possible | Not integrated/reviewed in current candidate. |
| `0449bfa4d` | Remove __FILE__ and __LINE__ function arguments | Not integrated/reviewed in current candidate. |
| `4a9075d9f` | Replace strcpy(buf, "") | Not integrated/reviewed in current candidate. |
| `c693fd78b` | Fix texture corruption on Extraction thumbnail | Not integrated/reviewed in current candidate. |
| `2c7cc32d5` | Fix inefficient string management | Not integrated/reviewed in current candidate. |
| `77148cc62` | Fix light glares | Not integrated/reviewed in current candidate. |
| `bcaea5d7e` | Move functions from utils.c, collisionutils.c, crc.c and gfxreplace.c into the files where they're called | Not integrated/reviewed in current candidate. |
| `f39432946` | Remove arg parser | Not integrated/reviewed in current candidate. |
| `6e8249b8b` | Tidy up gfxmemory.c | Not integrated/reviewed in current candidate. |
| `ae4687917` | Use inline floor and ceil instructions | Not integrated/reviewed in current candidate. |
| `bb4d3458c` | Replace array copies with static arrays | Not integrated/reviewed in current candidate. |
| `01ce3dc21` | Remove g_SndDisabled and g_SndMp3Enabled | Not integrated/reviewed in current candidate. |
| `bacc2b92f` | Remove unused global variables | Not integrated/reviewed in current candidate. |
| `b4441522c` | Fix buffer that needs to be initialised | Not integrated/reviewed in current candidate. |
| `8fc5f5b21` | Fix crash when a guard spawns | Not integrated/reviewed in current candidate. |
| `e3317f206` | Remove pdmode.c | Not integrated/reviewed in current candidate. |
| `6edc8681d` | Remove a heap of one-liner functions | Not integrated/reviewed in current candidate. |
| `c24afbddb` | ai2asm: Store current chr in s0 instead of repeatedly loading it from g_Vars.chrdata | Not integrated/reviewed in current candidate. |
| `a9d0a1e02` | ai2asm: Implement some commands in assembly if using CHR_SELF | Not integrated/reviewed in current candidate. |
| `dc04fbc16` | Fix crash when a guard spawns at a pad | Not integrated/reviewed in current candidate. |
| `161bdd958` | Preload BG rooms for Area 51 stages | Not integrated/reviewed in current candidate. |
| `2e3cb7b5f` | Use uncached memory for room matrices | Not integrated/reviewed in current candidate. |
| `309a20879` | Remove vanilla profiling from audio manager | Not integrated/reviewed in current candidate. |
| `b76d108c4` | Use uncached memory for audio command lists | Not integrated/reviewed in current candidate. |
| `f9f4df209` | Optimise z-buffer functions | Not integrated/reviewed in current candidate. |
| `c863898de` | Remove osGetCount calls from weather and lighting code | Not integrated/reviewed in current candidate. |
| `43bcc9a57` | Don't report mema OOM | Diagnostic OOM reporting intentionally retained; not a speed optimization claim. |
| `4c99495cc` | Optimise chr bdlist handling | Not integrated/reviewed in current candidate. |
| `cba20b1e2` | Use abs.s instruction where possible | Not integrated/reviewed in current candidate. |
| `517f2206f` | Remove mod operations that use div where possible | Not integrated/reviewed in current candidate. |
| `4ae165254` | Change depth buffer allocation back to hi-res size | Full 640x480 depth allocation implemented separately in v74; upstream's native-hires size is insufficient here. |
| `ceb3238c4` | Fix spark group index | Not integrated/reviewed in current candidate. |
| `b83d5a427` | Fix bdlist | Not integrated/reviewed in current candidate. |
| `614579ac7` | HTM: Remove sqrtf in range check | Not integrated/reviewed in current candidate. |
| `36ea3a008` | Fix standby rooms | Not integrated/reviewed in current candidate. |
| `ec746d606` | Fix flicker when changing VI mode | Not integrated/reviewed in current candidate. |
| `a7b854782` | Restore the crash handler | Not integrated/reviewed in current candidate. |
| `7073aa6d0` | Fix cover count | Equivalent emitted-cover-count correction implemented in v79; not this exact commit. |
| `cbae3f8ab` | Fix scheduler's handling of yielded RSP tasks where the RDP completes | Backported with two-buffer/boot adaptation in v80b. Host event tests, short normal emulator checks, normal N64 intro and separate synthetic-input N64 checks pass; broader validation remains open. |
| `a66342977` | Tidy up crash handler | Not integrated/reviewed in current candidate. |
| `72640f7db` | Make debris behave like vanilla | Not integrated/reviewed in current candidate. |
| `739f9049f` | Use thread metrics for dynamic profiling | Not integrated/reviewed in current candidate. |
| `ca370adf9` | Remove two unnecessary portals in Air Force One | Not integrated/reviewed in current candidate. |
| `df29001ed` | Prevent rooms from loading outside of preload | Not integrated/reviewed in current candidate. |
| `47e37e5cc` | Tighten the Area 51 room preloading | Not integrated/reviewed in current candidate. |
| `1f97533e0` | Juggle memory so Rescue works on co-op | Not integrated/reviewed in current candidate. |
| `c911ee9b2` | Use pointer iterators in matrix ASM code | Not integrated/reviewed in current candidate. |
| `87af76dc3` | Optimise ultra/gu functions | Not integrated/reviewed in current candidate. |
| `9bd41837a` | Optimise string functions | Not integrated/reviewed in current candidate. |
| `a45acb282` | Optimise DMA functions | Not integrated/reviewed in current candidate. |
| `bf3245076` | Optimise lang functions | Not integrated/reviewed in current candidate. |

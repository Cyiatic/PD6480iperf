# v86d: prewarm the default AI buddy head

Source `1e45bfaf2`, based on normal v86c. Normal ROM SHA256
`b450743aa0284ee25a84f4204c2e0a7de29a9d3319064b6da94f0dee65b65ead`;
ELF `22c03aa2194d27f5c15d3151ebd0047650522e785fed38c6a0a57aaa4558b75a`;
CRC `af026169/e8f46633`. No allocation trace or synthetic replay is linked.

The v86c trace proves the AI-co-op crash occurs at Velvet head file0x561:
52960-byte model allocation with43120 available after room-cache budgeting.
`modeldefLoadToNew` uses FILELOADMETHOD_EXTRAMEM (+32KiB), then shrinks the result.
v86d loads just this pending default buddy head before bgPreload. It does not
spawn the buddy early, consume model-instance slots, or change framebuffer size.
The helper excludes solo, Combat Simulator, CI, Mr Blonde's special model and
alternate-buddy cheats; an already-cached head is not loaded twice.

The extracted actual-C helper passes eligibility/idempotency tests, all15
alternate-buddy cheat combinations, and a call-order check. Native build passes;
all1403 compressed file-table assets validate. Raw assets are not covered by that
compressed-stream audit.

Cold10800-tick ordinary-input test with external stock Dark and one frontend
controller reaches Agent AI-co-op Infiltration, shows the buddy, full-screen pause
blur, horizontal menu inputs, graph-off and resumed living3D. Final frame631,
health1, pause0, OOM0, CPU flags0,640x480. The former model-allocation crash is not
present in this sample. This is not a hardware or whole-mission pass.

**Still fails the strict cache gate:**15 evictions and43 room-load failures,
despite no missing visible room in the final snapshot and a valid partition.
The room bank is only38512 bytes after prewarming the retained head. This must
not be called a clean pass: the change shifts pressure onto room geometry.
Keep the128KiB general reserve unchanged until another reduction is justified
by allocation lifetimes or a proven smaller model-load workspace. No user
candidate/patch bundle is promoted from this experiment.

A further600-tick no-input continuation reaches frame1001, still alive/unpaused,
with Velvet clearly visible and no allocation fault. The temporary menu eyepiece
overlay has disappeared after teardown. The room-failure counter remains43.

No v86d hardware attempt: current ED64 interface was absent even with Plug1ON
during the v86c preflight. Plug1 was switched OFF after that bounded attempt.

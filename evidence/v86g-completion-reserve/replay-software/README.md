# Labelled v86g Agent replay, software

Source `a528d058fb23543af43841db13c73a1a3f11721b` on
`diagnostics/v86g-infiltration-replay`. The reviewed replay is applied to normal
v86g; the label says V86G TEST. Scheduler/buffer/memory code is unchanged from
normal v86g. It is not a release ROM or normal-ROM interactive gameplay proof.

Retail diagnostic ROM `cb3568848785e143d2c9adb1e7e0ce1bbdd72a3d11e08efce0df01f43e2157a3`;
source-header ROM `f5291ae335ea39cdf8d4a32bc71e70522e9b85e675bfa84d490c98baf7d9857b`;
ELF `a27f4cceddddaf40296fecb4fc406968d330a50302c4193044c88f798b62005a`.
Only header offsets0x3c/0x3f differ between ROM forms.

The static audit checks the compiler-inlined save wrappers' complete direct
call graph, both EEPROM branches to the RAM shim, the exact Controller Pak
write-blocking stub, stock Dark seed hash and no external calls to physical
EEPROM routines. Two retained library-internal EEPROM calls are not gameplay
save accesses. An initial missing-symbol rejection led to disassembly review
and the inlined-call audit, not an assumed pass. Actual input-writer tests pass
all400 ring boundaries and reject the fake-presence control. Scheduler headroom
tests pass with one/no-slot controls rejected.

6000 cold host ticks, original core, cached interpreter, Angrylion/cxd4,8MiB,
mask1, no host input/state/save/RAM writes: setup is deliberately inside replay.
Native0. Final Infiltration47/frame754, Solo/Agent, alive, health0.4742265,
unpaused,640x480, graph enabled, phase7/tick490, one fixed-label visit, RAM
save45reads/10writes. OOM/cache/heap faults0, six evictions, valid partition.
Final image inspected: resumed3D, gun/nearby character, test HUD and graph.
Phase8 is not reached; no completed or death-free whole replay is claimed.

State `ffe0655902bcc0b77f969100d3f0151e8866b717f7bc7836d3158afbada50825`;
RAM `86b669b83c7a0af01413d1f7182480c646a549a79578b2bbd9cd098cb52941de`.
Physical results are recorded separately.

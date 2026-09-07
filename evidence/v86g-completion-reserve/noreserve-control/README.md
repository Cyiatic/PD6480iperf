# Same-layout zero-reserve negative control also advances

Only the two immediate bytes at `0x800021e8` change in the authenticated
normal-v86g ELF/raw stage1: `addiu v1,v1,-2` becomes `addiu v1,v1,0`.
No instructions, symbols, data, addresses or allocations are relocated.
The original map/mkrom recompress the result. Normal artifacts are untouched.
See [the authenticated change manifest](manifest.json).

Control ROM SHA256 `c83306dbca01caa40b44882256a835e25adf46935f4128ee45700de4d8ed553b`;
ELF `07674181904a2e8418b5d6e00c510304aea6a3a33697d3acb7ee11e062807079`.
The same original-core9150-tick cold-four input and Dark EEPROM also reach
Extraction: frame1437, Solo/Perfect Agent, alive/full health, unpaused, not in
cutscene, mask15,640x480, graph enabled. No allocation/cache/heap/thread faults;
valid partition. Native exit0. The final dark scope/HUD image was inspected.
No state restoration, host RAM writes or hardware upload of this control.

State `b92f1abd4f098cd1bb81483a8c7e459737c2aa516d4fb65716ea863f336d8b42`;
RAM `0ceb04a85e2aceeb073ecac1ef7a875e26565bf90d65a9321992c2322a29b24d`.
The inspector authenticates the patched ELF, not the original ELF.

This means the cold script is **not policy-sensitive on the new layout**.
Do not claim it reproduced the old stall or proved v86g's runtime improvement
was caused specifically by the reserve. The original-v86f read-only trace still
directly shows queue loss; actual-C saturation tests still establish the headroom
invariant and fail with one/no slots. Broader runtime checks remain necessary.
This deliberately disabled diagnostic is never a release candidate.

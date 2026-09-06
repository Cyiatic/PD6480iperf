# v82f watched replay diagnostic

Parent v82e 8d66b7e0f restored visible city intro on original N64, without
synthetic input. This revision restores only the status-preserving pdHwReplay
call in joyDebugJoy and updates both diagnostic labels to V82F. Checkpoint
watcher, memory/render/scheduler and save isolation are otherwise unchanged.
Normal v82b is unchanged; this is not a candidate.

ROM SHA256 a8d392ee27966de8f7b929c1e06cff4b9a867a304e619cada182821f827a9b37.
ELF SHA256 364358463a2e0e549b9bde3b9bf7696e2ad8038faa1eff09e136f00690631983.
CRC1/2 020d0fd2 / 0adb6495.

Hardware/software results belong in separate evidence records. The scripted
setup and RAM save remain modifications, not physical save-import or
unchanged-ROM interactive gameplay proof. Phase counts use game samples,
not elapsed seconds, and run slower on hardware than in the software test.

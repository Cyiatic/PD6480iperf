# v82b synthetic console replay — diagnostic branch only

Based directly on normal `24995c1c66eaa0e4ac5568f5711f7af7678b5561`.
No rendering, room-preloading, allocator, VI or scheduler changes. The normal
candidate must not contain any of these hooks or the embedded save.

The modern core removed the earlier separate joy playback interface. This
diagnostic replaces only newly acquired samples in the main thread's current
partition, after its existing partition handover. The scheduler still polls
real hardware and owns the other partition; the previous sample is preserved
for edge detection. Each newly acquired sample receives the same test input.

File selection and opening the Video dialog are programmatic setup. L, two
down-C focus changes, A checkbox toggles and stick movement are then consumed
by the normal game/menu handlers. Phase 5 checks on/off/on against the actual
Hi-Res variable and focused menu item. Phase 99 is failure. Phase 8 is replay
completion, not a claim about the unchanged normal ROM or Analogue hardware.

The always-visible yellow V82B TEST overlay identifies phase, Hi-Res, checked
toggle count, RAM save I/O counters and position. The diagnostic redirects the
game's EEPROM probe/read/write routines to a 2048-byte RAM copy of synthesized
stock Dark. __osContRamWrite returns PFS_ERR_NOPACK before hardware I/O, blocking
Controller Pak and Transfer Pak writes. Do not include this binary in a user
candidate package. The normal save remains external and stock-format.

# v86b Infiltration hardware replay — diagnostic only

Based on modern v86b (`ea2ad550b`, documentation update `ca431f547`). The normal
candidate remains the immutable c33ec145... ROM; this branch must never be
distributed as that candidate or merged into its runtime branch.

Reuse the previously reviewed lean v85 input/save diagnostic, not its old
runtime files. Select stock Dark and Infiltration / Perfect Agent through actual
menu handlers, then exercise ordinary input consumers for movement, L graph and
menu swipes. Video Options must contain the fixed-mode label; no resolution
checkbox toggling is claimed. Sample injection occurs only in the main thread's
newly acquired controller partition, preserving physical presence/error status.

The 2048-byte stock Dark EEPROM is embedded as mutable RAM. Physical EEPROM
access is replaced only in this diagnostic. Controller/Transfer Pak writes are
blocked. No watchdog task is linked. An always-visible V86B TEST label includes
phase, stage, difficulty, OOM, required BG-load failures, eviction/miss counts,
framebuffer size, RAM save counters and position. It remains visible when L hides
the normal graph, so synthetic footage cannot be mistaken for an unmodified ROM.

Actual input-partition and RAM-EEPROM C tests pass. Build/runtime/hardware tests
are pending at creation; do not infer success from compilation or a loader exit.
No save is written to the user's cartridge/controller pak by this diagnostic.

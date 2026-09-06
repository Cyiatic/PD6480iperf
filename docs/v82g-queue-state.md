# v82g queue-state diagnostic

Parent v82f, whose physical timeout showed step 107, two graphics tasks, no
active RSP/RDP. Extend ONLY timeout reporting to show main/scheduler wait
queues before stopping them, known SI/IRQ/GFX queues, VI current/next images,
scheduled/queued images, two queued tasks' buffers/states, stage/frame/replay
progress. Update both labels to V82G. No proposed scheduler fix yet.

ROM SHA256 93978bb55b9aa1bfe5dc9675b07c3d05bf76ef6ccb528ce5b0b3566f0e95c718.
ELF SHA256 d28b996027a7d64b382579eba894978724683dbc869509640e403d8d68ea327d.
CRC1/2 a1e35f35 / 6db97d3d.

Not a user candidate; normal v82b unchanged. The watchdog display uses CPU
320x240 fallback and cannot demonstrate patch rendering resolution/gameplay.

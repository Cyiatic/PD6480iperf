# Isolated AI-co-op allocation trace, not a normal ROM

Source `942e6a5ee`, based on normal v86c. Trace implementation reuses the reviewed
`d2f6eb171` caller/file recorder and resets counters per stage. It records requested
bytes, not retained live memory. No synthetic input or RAM writes are in the ROM;
the frontend supplies ordinary inputs, one connected port, external stock Dark,
and the documented in-memory EEPROM-header adapter.

ROM SHA256: `01539904e60a47f13152fb9932ea18c51201f1c72a36309cd5bad703913b2c53`.
ELF SHA256: `c7e4be963975f072d91e2e7ac52d61ccfed07d63b086138376265b64ba5d5a9d`.
Host v2: `7bbf4ea551832a170ed7e6111acd2ec9f030beccf19567baacae6ef576ac419a`.
Core: `4f239ad5ba11887d70e6887b648237f81ab9dfeb6f80f463153abc513e0ebad7`.
Stock EEPROM: `fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d`.

The11000-tick cold run ends in Infiltration's intro, frame826, Agent, cooperative
true and one configured AI buddy. It has no allocation failure yet. Its input
SHA is `2a8bdcea0a467beba0733ab3ee52719ce36bee0859a8a2ba8b5625ca18040e2b`;
final state `78bbb8abdd4003a363c744600d67d525e7bad3902f768619d562a90c715ba441`.

The900-tick continuation restores that exact state and presses Start once to skip
the intro. Input SHA `00584e21871f9346a5b43c0dd9dfd21e2035a2f550a9d541ac5f21f6df48c816`.
It fails at level-frame849: `fileLoadToNew+0x90`, file0x561/Velvet head, request52960
with43120 bytes available. Main PC80005644, cause8, badVA b330, flags2. Final state
`c4cf056faaaa855c1e28834709645168222f98c6e08bd7a44dcf3a08ef54989a`.
The post-spawn image visibly shows the game's crash handler. Both reports include
RAM/ELF/layout hashes. This is software diagnosis, not hardware or a passing run.

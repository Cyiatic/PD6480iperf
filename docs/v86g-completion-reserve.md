# v86g: prevent graphics completion starvation by advisory retraces

Parent: `df1e767a014e0c17b1a354959fe380ed614201b3` (normal v86f).

A read-only emulator observer reproduces normal-v86f Extraction's frame-3
stall without changing guest code or state. Main's 32-message queue fills with
retrace traffic. Scheduler blocks sending graphics DONE; its own eight-message
interrupt queue fills with retraces. The next SP completion is acknowledged but
discarded by the kernel's full-queue branch. The matching DP completion runs,
leaving a graphics task awaiting an SP completion that will never arrive.

The sole runtime change reserves two main-queue slots for the existing maximum
of two outstanding graphics completions. Advisory retraces are suppressed above
that threshold. No buffer, RAM partition, queue allocation, task ownership,
priority, interrupt code, resolution, gameplay or input change is made.

Source-header ROM SHA256:
`0474d95e44bb7dd1a47683e4f8bf484a2b1c54c8f4d4746566059ec0a0961e46`.
Retail-header ROM SHA256:
`79a8f9698190aa76c8600b22f2f35de49abe62b8be2b5ce8dcd84bb834815e40`.
ELF SHA256:
`07595b1d4c7466bf3ac53f1df29bc21779c8d494eb41978a2c47d735e84ac010`.
Only header offsets 0x3c/0x3f differ between ROM forms; body identical.

Actual-C tests pass 93 slow-consumer states, 500,000 interleavings, boot retraces
and the existing atomic graphics-idle tests. One/no-slot negative controls fail.
The v6 ABI is unchanged. See private distro evidence
`evidence/v86g-completion-reserve/` on branch `mods/performance` for trace,
provenance, limitations and subsequent software/hardware outcomes.

Still a development build. No whole-game, sustained-play or Analogue pass is
claimed. Full 640x480 colour/depth, full 8 MiB, L graph and the existing menu fixes
are retained; the generated stock 100% Dark save is unchanged.

The original-core continuous cold-four 9150-tick software regression now passes
the old stall: Extraction frame1436, Solo/Perfect Agent, alive full health,
unpaused, no cutscene, graph enabled, game controller mask15, full640x480,
no allocation/cache/CPU faults and valid room partition. No state restoration
or RAM writes were used. State SHA256
`f07501488211b01b738482b86c90bd6ffde230ff84f7975a2ea408110eabde77`.
The final dark scope/HUD view was inspected; it is not whole-mission evidence.

Normal retail-ID ROM uploaded to N64 in35.81s. Inspected Elgato footage shows
city/ship/rooftop intro, not interactive gameplay. Plug1OFF/statusRelay0 verified;
157349816bytes of recording/sidecars deleted after inspection. No new bundle
promoted. Next gates include same-layout negative control, broader regressions
and physical gameplay evidence, retaining all earlier failure records.

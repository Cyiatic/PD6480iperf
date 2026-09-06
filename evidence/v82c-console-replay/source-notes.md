# v82c diagnostic: preserve physical controller-presence status

Normal candidate v82b is unchanged. This revision changes only the diagnostic
input writer and the visible test label from V82B TEST to V82C TEST.

The previous port of the old separate replay-ring logic wrote errno=0 into
the modern shared ring. Scheduler polling compares adjacent sample errno to
detect controller removal/insertion and initiate SI queries. A diagnostic
must not fake those statuses. The new helper preserves them and writes only
buttons/stick fields in the acquired main-thread partition.

Compiled host tests cover all 400 ring boundary pairs, preserving prior/next
partitions and physical status. Reintroducing errno=0 is a negative control
and fails. RAM EEPROM boundary/null/round-trip tests still pass. The old replay
passes the emulator but repeatedly blackscreens after product identification
on original N64; this change remains a hypothesis for that hardware failure.

ROM SHA256 c5326346c1fcab27913f4b6b3ddde9c2b726fd0c96e4c35349958117069e3d9f
ELF SHA256 a0811c72c3c06e59c982ed16da27653f01f3a1a37c3163e9decbb359478731cd
CRC1/2 3f73a12e / 3b0524e2

Do not distribute this replay/RAM-save binary as a normal candidate or count
its software success as unchanged-ROM interactive hardware/Analogue proof.

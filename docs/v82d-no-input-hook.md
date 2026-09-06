# v82d isolation diagnostic

Parent v82c 554a82ae7: remove only the pdHwReplay call from joyDebugJoy.
Keep the unused replay code, RAM EEPROM, physical Pak-write blocker and HUD
unchanged. With no synthetic input, expect normal title/intro progression,
not autonomous gameplay. This is not a user candidate or normal-save test.

Purpose: distinguish failure introduced by input-hook execution from the
other changes in the diagnostic. A rendered logo alone is not a gameplay pass.

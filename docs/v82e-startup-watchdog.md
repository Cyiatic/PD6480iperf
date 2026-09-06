# v82e startup watchdog diagnostic

Parent v82d, still no synthetic input. RAM EEPROM and physical Pak-write
blocker unchanged. Normal v82b source/ROM are not modified.

Adds a dedicated resident thread (ID 7, priority 31, private aligned 8 KiB
stack, private timer/queue). Main startup/tick checkpoints refresh a CP0 Count
heartbeat. Ten seconds without refresh causes it to stop main and scheduler,
print their saved PC/RA/cause/bad address/state plus task/SI/save counters and
the last checkpoint, and repeatedly show a CPU-written 320x240 timeout screen
using the OS VI manager. That timeout display is explicitly NOT gameplay or
480i proof. No controller/EEPROM writes are introduced.

Checkpoints: 1 before dma/amgr/vars/VI/joy/copyright; 2 before vmInit; 3 after
vmInit; 4 after filesInit; 5 before challenges/texture init; 6 after texInit;
7 before paksInit; 8 after paksInit; 9 end mainInit; 10 before sndInit; 11 after
sndInit; 12 mainLoop entry; 13 before gfx/joy reset; 14 after joyReset;
15 after lvReset; 16 after VI reset/frametime; 100 mainTick entry; 101 before
joyDebugJoy; 102 after it; 103 before lvTick; 104 after it; 105 before lvRender;
106 after it; 107 after task creation. A live tick loop keeps refreshing, so
this does not diagnose a non-stalling black display or disabled interrupts.

Fresh emulator: 1500 ticks/1296 video frames, title frame 1181, no OOM or
main/scheduler exception, 25 RAM reads/zero writes. Does not falsely time out
in that software run. Physical result must be recorded separately.

ROM SHA256 9e66c964e6e168c28e86d72bae83edeb3e3af63066682fdc173739b828a0db03.
ELF SHA256 5340859bae546ad2035456f7ab0873d7d033f2f4aa64690a261daac0109e05a5.
CRC1/2 854aa1c6 / 5e1a1727.

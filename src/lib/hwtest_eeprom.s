# DIAGNOSTIC ONLY: mutable RAM copy, not a physical EEPROM write.
.section .data
.balign 16
.globl g_PdHwEeprom
.type g_PdHwEeprom, @object
g_PdHwEeprom:
.incbin "src/assets/hwtest-Dark.eep"
.size g_PdHwEeprom, . - g_PdHwEeprom

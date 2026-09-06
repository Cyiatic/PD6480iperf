# DIAGNOSTIC ONLY: mutable RAM copy of the generated Dark EEPROM image.
.section .data
.balign 16
.globl g_PdHwEeprom
.type g_PdHwEeprom, @object
g_PdHwEeprom:
.incbin "src/assets/hwtest-Dark.eep"
.size g_PdHwEeprom, . - g_PdHwEeprom

"""Exercise modern replay safety checks against actual ELF and corrupted controls."""
import argparse
from pathlib import Path
import struct
import tempfile
from audit_modern_hw_replay import audit, Elf32


def check(path):
    result=audit(path)
    elf=Elf32(path)

    def offset(address):
        sections=[s for s in elf.sections if s[1]!=8 and s[3]<=address<s[3]+s[5]]
        if len(sections)!=1:raise ValueError('Ambiguous executable/data mapping')
        return sections[0][4]+address-sections[0][3]

    unsafe_pak=bytearray(elf.data)
    struct.pack_into('>I',unsafe_pak,offset(elf.symbols['__osContRamWrite'][0])+4,0x24020000)
    unsafe_save=bytearray(elf.data)
    start,size=elf.symbols['pakReadWriteBlock']
    shadow=elf.symbols['pdHwEeprom'][0]
    calls=[]
    for delta in range(0,size,4):
        word=struct.unpack_from('>I',elf.read(start+delta,4))[0]
        if word>>26==3 and (((start+delta+4)&0xf0000000)|((word&0x3ffffff)<<2))==shadow:
            calls.append(start+delta)
    if len(calls)!=2:raise ValueError('Expected two RAM EEPROM branches')
    physical=elf.symbols['osEepromLongWrite'][0]
    struct.pack_into('>I',unsafe_save,offset(calls[0]),(3<<26)|((physical>>2)&0x3ffffff))
    bad_seed=bytearray(elf.data)
    bad_seed[offset(elf.symbols['g_PdHwEeprom'][0])]^=1
    bad_label=bytearray(elf.data)
    label=bad_label.index(b'V86G TEST P%d ST%d D%d')
    bad_label[label:label+4]=b'FAIL'
    with tempfile.TemporaryDirectory(prefix='pd-replay-audit-') as temporary:
        for name,data in (('write-blocker',unsafe_pak),('physical-eeprom-call',unsafe_save),('seed',bad_seed),('label',bad_label)):
            target=Path(temporary)/(name+'.elf')
            target.write_bytes(data)
            try:audit(target)
            except ValueError as error:print(name+' negative rejected: '+str(error))
            else:raise AssertionError(name+' unsafe control was accepted')
    print('PASS: actual ELF and four independent unsafe controls; '+result['elf_sha256'])


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf',type=Path)
    check(parser.parse_args().elf)

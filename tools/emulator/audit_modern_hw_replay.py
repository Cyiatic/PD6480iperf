"""Safety/identity audit for the labelled modern-core replay, not release proof."""
import argparse
import hashlib
import json
from pathlib import Path
import struct

from audit_hw_replay import direct_jumps, Elf32
from inspect_modern_rdram import inspect


def audit(elf_path,ram_path=None,layout_path=None):
    elf=Elf32(elf_path)
    if elf.symbol_data('__osContRamWrite') != bytes.fromhex('03e0000824020001'):
        raise ValueError('Physical Controller Pak write blocker changed')
    shadow=elf.symbols['pdHwEeprom'][0]
    # GCC inlines the EEPROM wrappers into pakReadWriteBlock in this runtime.
    # Its two EEPROM branches must both call the RAM shim. The retained PFS
    # branch is separately protected by the audited physical write blocker.
    expected=('joyDisableCyclicPolling','joyCheckPfs','osPfsReadWriteFile',
              'joyEnableCyclicPolling','pdHwEeprom','pdHwEeprom')
    if direct_jumps(elf,'pakReadWriteBlock')!=[elf.symbols[n][0] for n in expected]:
        raise ValueError('Unexpected inlined pakReadWriteBlock call graph')
    if direct_jumps(elf,'pdHwEeprom'):
        raise ValueError('Unexpected external RAM-save shim call')
    physical_names=('osEepromProbe','osEepromRead','osEepromWrite','osEepromLongRead','osEepromLongWrite')
    physical={elf.symbols[n][0] for n in physical_names}
    library_ranges=[elf.symbols[n] for n in physical_names]
    physical_calls=0
    for section in elf.sections:
        if section[1]==8 or not section[2]&4:continue
        data=elf.section_data(section)
        for i in range(0,len(data)-3,4):
            word=struct.unpack_from('>I',data,i)[0]
            if word>>26 not in (2,3):continue
            pc=section[3]+i
            target=((pc+4)&0xf0000000)|((word&0x3ffffff)<<2)
            if target not in physical:continue
            if not any(start<=pc<start+size for start,size in library_ranges):
                raise ValueError(f'External physical EEPROM call at {pc:#x}')
            physical_calls+=1
    seed_hash=hashlib.sha256(elf.symbol_data('g_PdHwEeprom')).hexdigest()
    if seed_hash!='fa86c003d8cf71cb099c2c55a92cdea3f00b4d482370a48202d7a0d4b0184a7d':
        raise ValueError('Wrong stock Dark save')
    if b'V86G TEST P%d ST%d D%d' not in elf.data:
        raise ValueError('Diagnostic identifier is missing')
    result=dict(diagnostic_only=True,hardware_verified=False,
                elf_sha256=hashlib.sha256(elf.data).hexdigest(),seed_sha256=seed_hash,
                physical_controller_pak_writes_blocked=True,game_eeprom_access_redirected_to_ram=True,
                retained_library_internal_eeprom_calls=physical_calls,
                label='V86G TEST',limits='Code guards only; gameplay/input-partition/physical video require separate checks.')
    if ram_path:
        if not layout_path:raise ValueError('RAM inspection requires the compiled modern layout')
        ram=ram_path.read_bytes()
        result['snapshot']=inspect(elf_path,ram_path,layout_path)
        result['replay']={}
        for name in ('g_PdHwPhase','g_PdHwPhaseTicks','g_PdHwToggleChecks','g_PdHwSaveReads','g_PdHwSaveWrites'):
            address,size=elf.symbols[name]
            if size!=4 or not 0x80000000<=address<=0x807ffffc:raise ValueError('Invalid replay scalar ABI')
            result['replay'][name]=struct.unpack_from('<I',ram,address&0x7fffff)[0]
        result['limits']='Labelled software snapshot, not normal-ROM interactive gameplay or hardware proof. Phase99/dead is failure to finish alive.'
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('elf',type=Path)
    parser.add_argument('--ram',type=Path)
    parser.add_argument('--layout',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=audit(args.elf,args.ram,args.layout)
    with args.output.open('x') as output:output.write(json.dumps(result,indent=2)+'\n')
    print(json.dumps({key:val for key,val in result.items() if key!='snapshot'},indent=2))

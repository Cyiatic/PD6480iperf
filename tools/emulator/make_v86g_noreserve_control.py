"""Create a same-layout NEGATIVE control, never a release candidate.

Only the immediate at the authenticated retrace queue threshold changes:
addiu v1,v1,-2 -> addiu v1,v1,0. No instruction, symbol, asset or allocation
is relocated. Recompress the new stage1 binary with the original mkrom/map.
"""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from audit_480i_elf import Elf32


def create(elf_path, binary_path, output_prefix):
    elf=Elf32(elf_path)
    if hashlib.sha256(elf.data).hexdigest() != '07595b1d4c7466bf3ac53f1df29bc21779c8d494eb41978a2c47d735e84ac010':
        raise ValueError('Not the immutable normal-v86g ELF')
    address=0x800021e8
    before=bytes.fromhex('8c8300108c8200082463fffe0043102a1040000a')
    if elf.read(address-8,len(before)) != before:
        raise ValueError('Unexpected retrace threshold code')
    start=elf.symbols['_libSegmentStart'][0]
    rom_start=elf.symbols['_libSegmentRomStart'][0]
    length=elf.symbols['_libSegmentLen'][0]
    original_binary=binary_path.read_bytes()
    if original_binary[rom_start:rom_start+length] != elf.read(start,length):
        raise ValueError('Raw lib bytes do not match authenticated ELF')
    bin_offset=rom_start+address-start
    backed=[s for s in elf.sections if s[1]!=8 and s[3]<=address< s[3]+s[5]]
    if len(backed)!=1:
        raise ValueError('Ambiguous ELF section')
    elf_offset=backed[0][4]+address-backed[0][3]
    new_bin,new_elf=bytearray(original_binary),bytearray(elf.data)
    for data,offset in ((new_bin,bin_offset),(new_elf,elf_offset)):
        if struct.unpack_from('>I',data,offset)[0]!=0x2463fffe:
            raise ValueError('Expected exact addiu v1,v1,-2')
        struct.pack_into('>I',data,offset,0x24630000)
    for old,new,offset in ((original_binary,new_bin,bin_offset),(elf.data,new_elf,elf_offset)):
        if old[:offset]!=new[:offset] or old[offset+4:]!=new[offset+4:]:
            raise ValueError('Control changed bytes outside the one instruction')
    outputs=[Path(str(output_prefix)+'.bin'),Path(str(output_prefix)+'.elf')]
    if any(p.exists() for p in outputs):
        raise FileExistsError('Control output exists; refusing overwrite')
    for path,data in zip(outputs,(new_bin,new_elf)):
        with path.open('xb') as output: output.write(data)
    return dict(diagnostic_only=True,negative_control=True,layout_identical=True,
                instruction_address=hex(address),before='2463fffe',after='24630000',
                original_bin_sha256=hashlib.sha256(original_binary).hexdigest(),
                control_bin_sha256=hashlib.sha256(new_bin).hexdigest(),
                control_elf_sha256=hashlib.sha256(new_elf).hexdigest(),hardware_verified=False)


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('elf','binary','output_prefix'):parser.add_argument(name,type=Path)
    args=parser.parse_args()
    print(json.dumps(create(args.elf,args.binary,args.output_prefix),indent=2))

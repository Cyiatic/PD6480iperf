"""Read graphics queue ownership using compiler-derived ABI offsets, without writes."""
import argparse
import hashlib
import json
from pathlib import Path
import struct
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit_480i_elf import Elf32

KEYS = 'magic version sched_size task_size rsp rdp next next2 state type gfx_type audio_type'.split()


def inspect(elf_path, ram_path, layout_path):
    elf = Elf32(elf_path)
    ram, layout = Path(ram_path).read_bytes(), Path(layout_path).read_bytes()
    if len(ram) != 0x800000 or len(layout) != 4 * len(KEYS):
        raise ValueError('Wrong RAM or layout length')
    offsets = dict(zip(KEYS, struct.unpack('>' + 'I' * len(KEYS), layout)))
    if offsets['magic'] != 0x50444746 or offsets['version'] != 1:
        raise ValueError('Unknown layout')
    if (offsets['gfx_type'], offsets['audio_type']) != (1, 2):
        raise ValueError('Unexpected task-type ABI')
    base, size = elf.symbols['g_Sched']
    if size != offsets['sched_size']:
        raise ValueError('Scheduler ABI mismatch')
    for key in ('rsp', 'rdp', 'next', 'next2', 'state', 'type'):
        extent = offsets['task_size'] if key in ('state', 'type') else size
        if offsets[key] & 3 or offsets[key] + 4 > extent:
            raise ValueError('Invalid compiled offset')

    def word(address):
        if not 0x80000000 <= address <= 0x807ffffc or address & 3:
            raise ValueError('Invalid aligned KSEG0 address')
        return struct.unpack_from('<I', ram, address & 0x7fffff)[0]

    queues = {}
    for key in ('rsp', 'rdp', 'next', 'next2'):
        pointer = word(base + offsets[key])
        queues[key] = {'address': hex(pointer)}
        if pointer:
            queues[key].update(state=word(pointer + offsets['state']), type=word(pointer + offsets['type']))
    idle = (queues['rdp']['address'] == '0x0' and queues['next']['address'] == '0x0'
            and queues['next2']['address'] == '0x0'
            and (queues['rsp']['address'] == '0x0' or queues['rsp']['type'] == offsets['audio_type']))
    return dict(hardware_verified=False, snapshot_only=True, graphics_idle=idle, queues=queues,
                elf_sha256=hashlib.sha256(elf.data).hexdigest(),
                rdram_sha256=hashlib.sha256(ram).hexdigest(),
                layout_sha256=hashlib.sha256(layout).hexdigest())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ('elf', 'ram', 'layout'):
        parser.add_argument(name, type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = inspect(args.elf, args.ram, args.layout)
    if args.output:
        with args.output.open('x') as output:
            output.write(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))

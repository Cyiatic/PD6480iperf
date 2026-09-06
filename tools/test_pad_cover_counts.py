"""Run the actual pad generator in memory and validate emitted cover bounds.

The performance generator intentionally omits special cover records. This
test verifies that its advertised count follows the emitted data, not JSON
records which were omitted. It does not prove full AI/gameplay equivalence.
"""
import argparse
import ast
import json
from pathlib import Path
import struct
from types import SimpleNamespace


def generator(source):
    tree = ast.parse(source)
    # Load the actual App class/constants without executing its CLI or writers.
    selected = [node for node in tree.body if isinstance(node, ast.ClassDef) or
                (isinstance(node, ast.Assign) and any(isinstance(target, ast.Name)
                 and target.id.startswith('PADFLAG_') for target in node.targets))]
    helpers = SimpleNamespace(pad4=lambda data: data + bytes((-len(data)) % 4),
                              pad16=lambda data: data + bytes((-len(data)) % 16))
    namespace = {'struct': struct, 'assetmgr': helpers}
    exec(compile(ast.Module(body=selected, type_ignores=[]), '<actual mkpads>', 'exec'), namespace)
    return namespace['App']


def check(source_root):
    app_class = generator((source_root / 'tools/assetmgr/mkpads').read_text())
    paths = sorted((source_root / 'src/assets/ntsc-final/pads').glob('*.json'))
    if not paths:
        raise ValueError('No NTSC-final pad JSON inputs found')
    mixed = 0
    for path in paths:
        app = app_class()
        app.json = json.loads(path.read_text())
        app.pad_names = app.make_names(app.json['pads'])
        app.waypoint_names = app.make_names(app.json['waypoints'])
        app.waygroup_names = app.make_names(app.json['waygroups'])
        app.populate_waygroup_waypoints()
        data = app.make_binary()
        count = struct.unpack_from('>I', data, 4)[0]
        offset = struct.unpack_from('>I', data, 16)[0]
        expected = sum(row['special'] == 0 for row in app.json['cover'])
        if count != expected or not 0 <= len(data) - offset - count * 28 < 16:
            raise ValueError(f'{path.name}: count={count}, emitted={expected}, size={len(data)}')
        mixed += expected != len(app.json['cover'])
    print(f'PASS: {len(paths)} pad generators, {mixed} with omitted special covers; counts/bounds match')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_root', type=Path)
    check(parser.parse_args().source_root)

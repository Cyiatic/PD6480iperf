"""Check the no-graph variant against the exact v87 runtime and graph history.

Source-level regression, not a console/controller test. Requires Git history.
"""
import argparse
import json
from pathlib import Path
import re
import subprocess
import difflib

BASE = '82d704d0154ea86f9e5d0fb98541907806f31960'
GRAPH = '5430099310f52d0e34aae4f8af4ca7222358c18d'
INPUT_FILES = ['src/game/' + name + '.c' for name in (
    'activemenutick', 'bondbike', 'bondeyespy', 'bondmove', 'bondview',
    'credits', 'menu', 'player')]
ABSENT_LEGACY = {
    # These entire legacy code paths had already been removed before v87.
    'src/game/menu.c': ['if (joyGetButtons(0, 0)) {'],
    'src/game/player.c': ['&& joyGetButtonsPressedThisFrame(contpad1, A_BUTTON | B_BUTTON | Z_TRIG | START_BUTTON | 0 | R_TRIG)) {'],
}


def git(source, *args):
    return subprocess.check_output(['git', '-C', str(source), *args], text=True)


def inverse_input_changes(source, filename='src/game/bondmove.c'):
    diff = git(source, 'show', '--format=', GRAPH, '--', filename)
    pairs = []
    removed, added = [], []
    for line in diff.splitlines() + [' ']:
        if line.startswith(('---', '+++')):
            continue
        if line.startswith('-'):
            removed.append(line[1:])
        elif line.startswith('+'):
            added.append(line[1:])
        elif removed or added:
            assert len(removed) == len(added), 'Unexpected graph input diff'
            pairs.extend(zip(added, removed))
            removed, added = [], []
    base = git(source, 'show', BASE + ':' + filename)
    lines = base.splitlines(keepends=True)
    cursor = 0
    skipped = []
    restored = 0
    normalize = lambda line: line.strip().removesuffix('\\').rstrip()
    for disabled, stock in pairs:
        found = next((i for i in range(cursor, len(lines))
                      if normalize(lines[i]) == normalize(disabled)), None)
        if found is None:
            skipped.append(normalize(disabled))
            continue
        lines[found] = lines[found].replace(normalize(disabled), normalize(stock))
        cursor = found + 1
        restored += 1
    assert skipped == ABSENT_LEGACY.get(filename, []), (filename, skipped)
    return ''.join(lines), restored, skipped


def check(source, bondmove, lv):
    expected, count, skipped = inverse_input_changes(source)
    assert not skipped
    assert bondmove == expected, 'Input source differs from exact inverse of graph bindings'
    match = re.search(r'static Gfx \*lvPrint\(Gfx \*gdl\)\n\{(.*?)\n\}', lv, re.S)
    assert match, 'Graph entry point missing'
    body = re.sub(r'/\*.*?\*/', '', match[1], flags=re.S).strip()
    assert body == 'return gdl;', 'Graph entry point still reads input or renders'
    # Every changed mask must retain C/R input and restore its stock L/D alias.
    assert not re.search(r'0 \| [LRUD]_(?:CBUTTONS|TRIG)', bondmove)
    assert 'L_CBUTTONS | R_CBUTTONS | L_JPAD | R_JPAD' in bondmove
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('.'))
    parser.add_argument('--emit-input-patch', action='store_true')
    args = parser.parse_args()
    source = args.source.resolve()
    if args.emit_input_patch:
        patch = ['*** Begin Patch\n']
        for filename in INPUT_FILES:
            expected, count, skipped = inverse_input_changes(source, filename)
            print(json.dumps(dict(file=filename, restored=count, absent_legacy_lines=skipped)), file=__import__('sys').stderr)
            current = (source / filename).read_text()
            if current == expected:
                continue
            patch.append('*** Update File: ' + (source / filename).as_posix() + '\n')
            for line in list(difflib.unified_diff(current.splitlines(True), expected.splitlines(True), n=3))[2:]:
                patch.append('@@\n' if line.startswith('@@') else line)
        patch.append('*** End Patch\n')
        print(''.join(patch), end='')
        return
    bondmove = (source / 'src/game/bondmove.c').read_text()
    lv = (source / 'src/game/lv.c').read_text()
    count = check(source, bondmove, lv)
    input_counts = {}
    for filename in INPUT_FILES:
        expected, restored, skipped = inverse_input_changes(source, filename)
        assert (source / filename).read_text() == expected, filename + ': not stock bindings'
        input_counts[filename] = dict(restored=restored, absent_legacy_lines=skipped)
    # Fail-closed negative controls: old input file and old graph entry point.
    for bad_input, bad_lv in [
        (git(source, 'show', BASE + ':src/game/bondmove.c'), lv),
        (bondmove, git(source, 'show', BASE + ':src/game/lv.c')),
    ]:
        try:
            check(source, bad_input, bad_lv)
        except AssertionError:
            pass
        else:
            raise AssertionError('A v87 negative control incorrectly passed')
    print(json.dumps(dict(stock_input_lines_restored=sum(x['restored'] for x in input_counts.values()),
        input_files=input_counts,
        exact_inverse_of_graph_input_changes=True, graph_entry_point_inert=True,
        negative_controls_rejected=2, hardware_test=False), indent=2))


if __name__ == '__main__':
    main()

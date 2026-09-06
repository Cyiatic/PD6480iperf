import copy
import unittest
from collect_modern_mission_chains import verify_continuation
from continue_modern_missions import continuation_input


class MissionChainTests(unittest.TestCase):
    def test_bounded_ordinary_continuation_input(self):
        for cutscene, pause, button in ((1,0,8),(0,3,2),(0,0,None)):
            text = continuation_input(dict(in_cutscene=cutscene,player_pause_mode=pause))
            self.assertEqual(text, f'30 42 {button} 0 0\n' if button else '')
        snap = dict(in_cutscene=0,player_pause_mode=0)
        text = continuation_input(snap,True)
        rows = [list(map(int,line.split())) for line in text.splitlines()]
        self.assertEqual(len(rows),5)
        self.assertTrue(all(len(r)==5 and 0<=r[0]<r[1]<600 for r in rows))
        self.assertEqual([r[2] for r in rows],[0,4096,8,0,0])
        for changes in (dict(in_cutscene=1),dict(player_pause_mode=3)):
            with self.assertRaises(ValueError):
                continuation_input(dict(snap,**changes),True)

    def setUp(self):
        self.parent = dict(requested_stage='VILLA', requested_stage_id=44,
            snapshot=dict(rdram_sha256='ram', oom_marker=0,
                threads={'main': {'flags': 0}},
                room_cache=dict(load_failures=0, allocator_faults=0)))
        self.child = dict(requested_stage='VILLA', requested_stage_id=44,
            parent_rdram_sha256='ram', parent_state_sha256='state')

    def test_matching_chain(self):
        verify_continuation(self.parent, self.child, 'state')

    def test_foreign_ram_or_state_rejected(self):
        for field in ('parent_rdram_sha256', 'parent_state_sha256'):
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_continuation(self.parent, dict(self.child, **{field: 'foreign'}), 'state')

    def test_mission_change_rejected(self):
        for field, value in (('requested_stage', 'WAR'), ('requested_stage_id', 22)):
            with self.subTest(field=field), self.assertRaises(ValueError):
                verify_continuation(self.parent, dict(self.child, **{field: value}), 'state')

    def test_cannot_hide_prior_failures(self):
        for fault in ('oom', 'load', 'allocator', 'cpu'):
            parent = copy.deepcopy(self.parent)
            snap = parent['snapshot']
            if fault == 'oom': snap['oom_marker'] = 1
            if fault == 'load': snap['room_cache']['load_failures'] = 1
            if fault == 'allocator': snap['room_cache']['allocator_faults'] = 1
            if fault == 'cpu': snap['threads']['main']['flags'] = 2
            with self.subTest(fault=fault), self.assertRaises(ValueError):
                verify_continuation(parent, self.child, 'state')


if __name__ == '__main__':
    unittest.main()

import unittest
from run_modern_menu_missions import evaluate_snapshot, input_sequence


class MenuMissionTests(unittest.TestCase):
    def snapshot(self):
        return dict(stage=48, oom_marker=0, active_dimensions=[640,480],
                    level_frame_number=200, tick_mode=1, in_cutscene=0,
                    loaded_rooms=[1,2], rooms_missing_vertex_batches=[],
                    player_pause_mode=0, threads={'g_MainThread':{'flags':0},
                                                  'g_SchedThread':{'flags':0}})

    def test_ordinary_inputs_all_indices(self):
        for index in range(21):
            text, ticks = input_sequence(index)
            inputs = [list(map(int, line.split())) for line in text.splitlines()]
            self.assertEqual(sum(row[4] == 22000 for row in inputs), index)
            self.assertTrue(all(len(row) == 5 for row in inputs))
            self.assertEqual([row[2] for row in inputs[-5:]], [1,1,1,8,8])
            self.assertTrue(all(0 <= row[0] < row[1] < ticks for row in inputs))
            self.assertTrue(all(a[1] < b[0] for a,b in zip(inputs, inputs[1:])))

    def test_ready_but_paused_is_not_unpaused(self):
        snapshot = self.snapshot()
        snapshot['player_pause_mode'] = 3
        report = evaluate_snapshot(snapshot,48,{1,2})
        self.assertTrue(report['load_gate_passed'])
        self.assertFalse(report['unpaused_snapshot'])

    def test_fault_after_initialization_is_not_a_pass(self):
        snapshot = self.snapshot()
        snapshot['threads']['g_MainThread']['flags'] = 2
        report = evaluate_snapshot(snapshot,48,{1,2})
        self.assertFalse(report['load_gate_passed'])
        self.assertEqual(report['thread_faults'], ['g_MainThread'])

    def test_every_required_condition(self):
        changes = [{'stage':38}, {'oom_marker':112}, {'active_dimensions':[320,240]},
                   {'level_frame_number':3}, {'tick_mode':2}, {'in_cutscene':1},
                   {'loaded_rooms':[1]}, {'rooms_missing_vertex_batches':[2]}]
        for change in changes:
            snapshot = self.snapshot()
            snapshot.update(change)
            with self.subTest(change=change):
                self.assertFalse(evaluate_snapshot(snapshot,48,{1,2})['load_gate_passed'])
        self.assertFalse(evaluate_snapshot(self.snapshot(),48,set())['load_gate_passed'])
        self.assertTrue(evaluate_snapshot(self.snapshot(),48,{1,2})['unpaused_snapshot'])

    def test_budgeted_cache_requires_warmup_and_complete_live_geometry(self):
        snapshot = self.snapshot()
        snapshot['loaded_rooms'] = [1]
        snapshot['room_cache'] = dict(mode=3, partition_valid=True, load_failures=0,
            allocator_faults=0, missing_visible_rooms=[],
            rooms=[dict(room=1,warmed=1),dict(room=2,warmed=1)])
        report = evaluate_snapshot(snapshot,48,{1,2})
        self.assertTrue(report['load_gate_passed'])
        self.assertEqual(report['missing_preload_rooms'],[2])
        self.assertEqual(report['room_policy'],'budgeted-retained-cache')
        for changes in (dict(mode=2),dict(partition_valid=False),dict(load_failures=1),
                        dict(allocator_faults=1),dict(missing_visible_rooms=[2]),
                        dict(rooms=[dict(room=1,warmed=1)])):
            cache = snapshot['room_cache'].copy()
            cache.update(changes)
            changed = dict(snapshot,room_cache=cache)
            self.assertFalse(evaluate_snapshot(changed,48,{1,2})['load_gate_passed'])


if __name__ == '__main__':
    unittest.main()

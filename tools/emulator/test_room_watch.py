import unittest
from unittest.mock import patch
from collect_room_watch import event_snapshot


class WatchEvidenceTests(unittest.TestCase):
    def test_success_retains_actual_result(self):
        result = {'room_cache': {'partition_valid': True}}
        with patch('collect_room_watch.inspect', return_value=result):
            self.assertEqual(event_snapshot('elf', 'ram', 'layout'), {'snapshot': result})

    def test_rejected_partition_is_preserved_not_promoted(self):
        with patch('collect_room_watch.inspect', side_effect=ValueError('Cache hole/overlap before free')):
            result = event_snapshot('elf', 'ram', 'layout')
        self.assertIsNone(result['snapshot'])
        self.assertEqual(result['snapshot_validation_error'], 'Cache hole/overlap before free')

    def test_unexpected_errors_still_stop_collection(self):
        with patch('collect_room_watch.inspect', side_effect=RuntimeError('tool failure')):
            with self.assertRaises(RuntimeError):
                event_snapshot('elf', 'ram', 'layout')


if __name__ == '__main__':
    unittest.main()

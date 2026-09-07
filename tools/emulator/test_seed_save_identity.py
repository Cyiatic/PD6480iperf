"""Do not silently erase or substitute the save paired with a mission seed."""
import hashlib
from pathlib import Path
import tempfile
import unittest
from run_modern_menu_missions import validate_seed_save
from collect_modern_mission_chains import verify_save_policy


class SeedSaveIdentity(unittest.TestCase):
    def test_legacy_is_explicit(self):
        self.assertIsNone(validate_seed_save(None,None))
        with self.assertRaises(ValueError):validate_seed_save(None,'0'*64)

    def test_full_matching_save(self):
        data=bytes(296960)
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'save-memory.bin'
            path.write_bytes(data)
            digest=hashlib.sha256(data).hexdigest()
            self.assertEqual(validate_seed_save(path,digest.upper()),digest)
            with self.assertRaises(ValueError):validate_seed_save(path,None)
            with self.assertRaises(ValueError):validate_seed_save(path,'0'*64)

    def test_eeprom_only_not_a_full_restored_save(self):
        data=bytes(2048)
        with tempfile.TemporaryDirectory() as temporary:
            path=Path(temporary)/'dark.eep'
            path.write_bytes(data)
            with self.assertRaises(ValueError):validate_seed_save(path,hashlib.sha256(data).hexdigest())

    def test_collector_checks_save_and_controller_identity(self):
        data = bytes(296960)
        metadata = dict(save_policy='preserve-matching', connected_mask=15)
        report = dict(save_memory_sha256=hashlib.sha256(data).hexdigest(),
                      connected_mask=15, snapshot=dict(connected_controller_mask=15))
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            (directory / 'save-memory.bin').write_bytes(data)
            verify_save_policy(metadata, report, directory)
            for changes in (dict(save_memory_sha256='0'*64), dict(connected_mask=1),
                            dict(snapshot=dict(connected_controller_mask=1))):
                with self.assertRaises(ValueError):
                    verify_save_policy(metadata, dict(report, **changes), directory)
            with self.assertRaises(ValueError):
                verify_save_policy(dict(metadata, connected_mask=0), report, directory)


if __name__=='__main__':unittest.main()

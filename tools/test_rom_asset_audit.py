"""Optional integration regressions using local ROMs, never downloaded fixtures."""
from pathlib import Path
import unittest
from audit_rom_assets import audit

ROOT = Path(__file__).resolve().parents[1]


class AssetAuditTests(unittest.TestCase):
    def inspect(self, path):
        if not path.exists():
            self.skipTest(f'Local fixture unavailable: {path.name}')
        return audit(path)

    def test_archived_v7_is_rejected(self):
        report = self.inspect(ROOT / 'artifacts/PD6480iperf-v7-raw-haf-2buf-retail-header.z64')
        self.assertEqual(report['sha256'], 'b1e95594dfe7197ba407af0616ad9ab2bb36f841fbfe93983101b7ce91fee19b')
        self.assertEqual(report['compressed_invalid'], 686)
        self.assertEqual(report['compressed_valid'], 717)
        self.assertEqual(report['rare_logo']['rom_bytes'], 16)
        self.assertEqual(report['rare_logo']['header'], '11730070000000000000000000000000')

    def test_v69_has_valid_compressed_files(self):
        report = self.inspect(ROOT / 'artifacts/PD6480iperf-v69-v59-hires-haf1-480i.z64')
        self.assertEqual(report['compressed_invalid'], 0)
        self.assertEqual(report['compressed_valid'], 1403)
        self.assertEqual(report['rare_logo']['rom_bytes'], 12336)

    def test_stock_has_valid_compressed_files(self):
        report = self.inspect(ROOT / 'pd.ntsc-final.z64')
        self.assertEqual(report['sha256'], '4e51142acac686d96861cecc58cf7cb7c3b06b21733b7f8ed609a709dc039a21')
        self.assertEqual(report['compressed_invalid'], 0)
        self.assertEqual(report['compressed_valid'], 1403)


if __name__ == '__main__':
    unittest.main()

import os
import tempfile
import unittest
from unittest.mock import patch

import pandas as pd

from utils import data_loader


class TestDataLoader(unittest.TestCase):
    def test_get_dataset_uses_fresh_cached_csv(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cached_csv = os.path.join(tmpdir, "cyber_security_attacks.csv")
            pd.DataFrame({"a": [1], "b": [2]}).to_csv(cached_csv, index=False)

            with patch.object(data_loader, "DATA_RAW_DIR", tmpdir):
                with patch("utils.data_loader.time.time", return_value=1_000_000):
                    with patch("utils.data_loader.os.path.getmtime", return_value=999_000):
                        with patch("utils.data_loader.download_dataset") as mock_download:
                            df = data_loader.get_dataset(cache=True)

            mock_download.assert_not_called()
            self.assertEqual(df.shape, (1, 2))
            self.assertEqual(df.iloc[0]["a"], 1)

    def test_get_dataset_downloads_when_cache_stale_and_refreshes_cache(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cached_csv = os.path.join(tmpdir, "cyber_security_attacks.csv")
            pd.DataFrame({"a": [0]}).to_csv(cached_csv, index=False)

            source_csv = os.path.join(tmpdir, "source.csv")
            pd.DataFrame({"a": [7], "b": [9]}).to_csv(source_csv, index=False)

            with patch.object(data_loader, "DATA_RAW_DIR", tmpdir):
                with patch("utils.data_loader.time.time", return_value=1_000_000):
                    # stale: older than 12 hours
                    with patch("utils.data_loader.os.path.getmtime", return_value=900_000):
                        with patch(
                            "utils.data_loader.download_dataset",
                            return_value=source_csv,
                        ) as mock_download:
                            df = data_loader.get_dataset(cache=True)

            mock_download.assert_called_once()
            self.assertEqual(df.shape, (1, 2))
            self.assertEqual(df.iloc[0]["a"], 7)
            # Cache should have been refreshed with downloaded content.
            reloaded = pd.read_csv(cached_csv)
            self.assertEqual(reloaded.iloc[0]["a"], 7)


if __name__ == "__main__":
    unittest.main()

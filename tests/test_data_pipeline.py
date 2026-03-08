import unittest
from unittest.mock import patch

import pandas as pd

import data_pipeline


class TestDataPipeline(unittest.TestCase):
    def test_run_data_pipeline_skips_when_processed_is_fresh(self):
        with patch("data_pipeline.os.path.exists", return_value=True):
            with patch("data_pipeline.time.time", return_value=1_000_000):
                with patch("data_pipeline.os.path.getmtime", return_value=999_000):
                    with patch("data_pipeline.get_dataset") as mock_get:
                        out = data_pipeline.run_data_pipeline()

        mock_get.assert_not_called()
        self.assertEqual(out, data_pipeline.PROCESSED_PATH)

    def test_run_data_pipeline_executes_steps_in_order(self):
        raw_df = pd.DataFrame({"x": [1]})
        mapped_df = pd.DataFrame({"y": [2]})
        eu_df = pd.DataFrame({"z": [3]})

        with patch("data_pipeline.os.path.exists", return_value=False):
            with patch("data_pipeline.get_dataset", return_value=raw_df) as mock_get:
                with patch(
                    "data_pipeline.map_ips_to_countries", return_value=mapped_df
                ) as mock_map:
                    with patch(
                        "data_pipeline.filter_eu_attacks", return_value=eu_df
                    ) as mock_filter:
                        with patch(
                            "data_pipeline.export_filtered_dataset",
                            return_value="data/processed/out.csv",
                        ) as mock_export:
                            out = data_pipeline.run_data_pipeline()

        mock_get.assert_called_once_with()
        mock_map.assert_called_once_with(raw_df)
        mock_filter.assert_called_once_with(mapped_df, data_pipeline.EU_COUNTRIES)
        mock_export.assert_called_once_with(eu_df)
        self.assertEqual(out, "data/processed/out.csv")


if __name__ == "__main__":
    unittest.main()

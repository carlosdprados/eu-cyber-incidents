import unittest
from unittest.mock import patch

from utils import dashboard_service


class TestDashboardService(unittest.TestCase):
    def test_falls_back_to_existing_csv_when_refresh_fails(self):
        with patch("utils.dashboard_service.os.path.exists", return_value=True):
            with patch("utils.dashboard_service.time.time", return_value=1_000_000):
                # stale file triggers refresh attempt
                with patch("utils.dashboard_service.os.path.getmtime", return_value=900_000):
                    with patch(
                        "utils.dashboard_service.data_pipeline.run_data_pipeline",
                        side_effect=RuntimeError("kaggle login failed"),
                    ):
                        out = dashboard_service.ensure_processed_dataset(
                            csv_path="data/processed/filtered_attacks.csv",
                            refresh_window_seconds=12 * 3600,
                        )

        self.assertEqual(out, "data/processed/filtered_attacks.csv")

    def test_raises_when_refresh_fails_and_no_fallback_exists(self):
        def fake_exists(path: str) -> bool:
            return False

        with patch("utils.dashboard_service.os.path.exists", side_effect=fake_exists):
            with patch(
                "utils.dashboard_service.data_pipeline.run_data_pipeline",
                side_effect=RuntimeError("kaggle login failed"),
            ):
                with self.assertRaises(RuntimeError):
                    dashboard_service.ensure_processed_dataset(
                        csv_path="data/processed/filtered_attacks.csv",
                        refresh_window_seconds=12 * 3600,
                    )


if __name__ == "__main__":
    unittest.main()

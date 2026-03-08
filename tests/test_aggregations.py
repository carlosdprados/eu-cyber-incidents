import unittest

import pandas as pd

from utils.aggregations import country_insight_metrics, selected_country_insight_metrics


class TestAggregations(unittest.TestCase):
    def test_country_insight_metrics_global_rankings(self):
        df = pd.DataFrame(
            [
                # Destination A (blocked-heavy)
                {
                    "destination_country": "A",
                    "source_country": "United States",
                    "Action Taken": "Blocked",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "A",
                    "source_country": "United States",
                    "Action Taken": "Blocked",
                    "Attack Type": "DDoS",
                    "Severity Level": "Low",
                },
                {
                    "destination_country": "A",
                    "source_country": "France",
                    "Action Taken": "Blocked",
                    "Attack Type": "Malware",
                    "Severity Level": "Medium",
                },
                {
                    "destination_country": "A",
                    "source_country": "France",
                    "Action Taken": "Ignored",
                    "Attack Type": "DDoS",
                    "Severity Level": "Low",
                },
                # Destination B (ignored/high-severity heavy)
                {
                    "destination_country": "B",
                    "source_country": "United States",
                    "Action Taken": "Ignored",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "B",
                    "source_country": "United States",
                    "Action Taken": "Logged",
                    "Attack Type": "Intrusion",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "B",
                    "source_country": "Germany",
                    "Action Taken": "Blocked",
                    "Attack Type": "DDoS",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "B",
                    "source_country": "Germany",
                    "Action Taken": "Ignored",
                    "Attack Type": "Malware",
                    "Severity Level": "Low",
                },
            ]
        )

        insights = country_insight_metrics(df, min_incidents=1)
        self.assertEqual(len(insights), 3)
        self.assertEqual(insights[0]["country"], "A")
        self.assertEqual(insights[1]["country"], "B")
        self.assertEqual(insights[2]["country"], "B")

    def test_selected_country_insights_default_threshold(self):
        df = pd.DataFrame(
            [
                # United States: 4 incidents
                {
                    "destination_country": "Lithuania",
                    "source_country": "United States",
                    "Action Taken": "Ignored",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "Lithuania",
                    "source_country": "United States",
                    "Action Taken": "Logged",
                    "Attack Type": "DDoS",
                    "Severity Level": "Low",
                },
                {
                    "destination_country": "Lithuania",
                    "source_country": "United States",
                    "Action Taken": "Blocked",
                    "Attack Type": "Malware",
                    "Severity Level": "Medium",
                },
                {
                    "destination_country": "Lithuania",
                    "source_country": "United States",
                    "Action Taken": "Ignored",
                    "Attack Type": "Intrusion",
                    "Severity Level": "High",
                },
                # Germany: 3 incidents
                {
                    "destination_country": "Lithuania",
                    "source_country": "Germany",
                    "Action Taken": "Blocked",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "Lithuania",
                    "source_country": "Germany",
                    "Action Taken": "Ignored",
                    "Attack Type": "DDoS",
                    "Severity Level": "Low",
                },
                {
                    "destination_country": "Lithuania",
                    "source_country": "Germany",
                    "Action Taken": "Blocked",
                    "Attack Type": "Intrusion",
                    "Severity Level": "Low",
                },
                # Italy: 2 incidents (excluded by default threshold=3)
                {
                    "destination_country": "Lithuania",
                    "source_country": "Italy",
                    "Action Taken": "Ignored",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "Lithuania",
                    "source_country": "Italy",
                    "Action Taken": "Logged",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
            ]
        )

        insights = selected_country_insight_metrics(df, "Lithuania")
        self.assertEqual(len(insights), 3)
        self.assertEqual(insights[0]["title"], "Most Effective Penetrator")
        self.assertIn("United States (4 incidents)", insights[0]["country"])
        self.assertEqual(insights[0]["unit"], "non-blocked share")
        self.assertEqual(insights[1]["title"], "Most Malware-Focused Attacker")
        self.assertIn("United States (4 incidents)", insights[1]["country"])
        self.assertEqual(insights[2]["title"], "Highest High-Severity Attacker")
        self.assertIn("United States (4 incidents)", insights[2]["country"])

    def test_selected_country_insights_threshold_override(self):
        df = pd.DataFrame(
            [
                {
                    "destination_country": "Lithuania",
                    "source_country": "United States",
                    "Action Taken": "Ignored",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "Lithuania",
                    "source_country": "United States",
                    "Action Taken": "Logged",
                    "Attack Type": "DDoS",
                    "Severity Level": "Low",
                },
                {
                    "destination_country": "Lithuania",
                    "source_country": "Italy",
                    "Action Taken": "Ignored",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "Lithuania",
                    "source_country": "Italy",
                    "Action Taken": "Logged",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
            ]
        )

        insights = selected_country_insight_metrics(df, "Lithuania", min_source_incidents=2)
        self.assertEqual(len(insights), 3)
        # Italy has 100% for all three ratios under this setup.
        self.assertIn("Italy (2 incidents)", insights[0]["country"])
        self.assertIn("Italy (2 incidents)", insights[1]["country"])
        self.assertIn("Italy (2 incidents)", insights[2]["country"])

    def test_selected_country_insights_fallback_when_no_source_meets_threshold(self):
        df = pd.DataFrame(
            [
                {
                    "destination_country": "Latvia",
                    "source_country": "United States",
                    "Action Taken": "Ignored",
                    "Attack Type": "DDoS",
                    "Severity Level": "Low",
                },
                {
                    "destination_country": "Latvia",
                    "source_country": "United States",
                    "Action Taken": "Blocked",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
                {
                    "destination_country": "Latvia",
                    "source_country": "Italy",
                    "Action Taken": "Logged",
                    "Attack Type": "Malware",
                    "Severity Level": "High",
                },
            ]
        )

        # No source has >= 10 incidents, so function should fall back to all sources.
        insights = selected_country_insight_metrics(df, "Latvia", min_source_incidents=10)
        self.assertEqual(len(insights), 3)
        self.assertIn("Italy (1 incident)", insights[1]["country"])
        self.assertIn("Italy (1 incident)", insights[2]["country"])

    def test_missing_columns_returns_empty(self):
        df = pd.DataFrame([{"destination_country": "A"}])
        self.assertEqual(country_insight_metrics(df), [])
        self.assertEqual(selected_country_insight_metrics(df, "A"), [])


if __name__ == "__main__":
    unittest.main()

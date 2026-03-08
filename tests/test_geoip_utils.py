import unittest
from unittest.mock import patch

import pandas as pd

from utils.geoip_utils import map_ips_to_countries


class _FakeCountry:
    def __init__(self, name: str):
        self.name = name


class _FakeResponse:
    def __init__(self, name: str):
        self.country = _FakeCountry(name)


class _FakeReader:
    instances = 0

    def __init__(self, *_args, **_kwargs):
        _FakeReader.instances += 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def country(self, ip: str):
        return _FakeResponse(f"country_for_{ip}")


class TestGeoIPUtils(unittest.TestCase):
    def test_map_ips_uses_single_reader_instance_per_call(self):
        _FakeReader.instances = 0
        df = pd.DataFrame(
            {
                "Source IP Address": ["1.1.1.1", "2.2.2.2"],
                "Destination IP Address": ["3.3.3.3", "4.4.4.4"],
            }
        )

        with patch("utils.geoip_utils.geoip2.database.Reader", _FakeReader):
            out = map_ips_to_countries(df, db_path="dummy.mmdb")

        self.assertEqual(_FakeReader.instances, 1)
        self.assertListEqual(
            out["source_country"].tolist(),
            ["country_for_1.1.1.1", "country_for_2.2.2.2"],
        )
        self.assertListEqual(
            out["destination_country"].tolist(),
            ["country_for_3.3.3.3", "country_for_4.4.4.4"],
        )

    def test_map_ips_fallbacks_to_none_when_reader_fails(self):
        df = pd.DataFrame(
            {
                "Source IP Address": ["1.1.1.1", "2.2.2.2"],
                "Destination IP Address": ["3.3.3.3", "4.4.4.4"],
            }
        )

        with patch(
            "utils.geoip_utils.geoip2.database.Reader",
            side_effect=RuntimeError("db unavailable"),
        ):
            out = map_ips_to_countries(df, db_path="dummy.mmdb")

        self.assertTrue(out["source_country"].isna().all())
        self.assertTrue(out["destination_country"].isna().all())


if __name__ == "__main__":
    unittest.main()

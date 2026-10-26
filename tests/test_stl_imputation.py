"""Meaningful additive identities, mask checks and real-input invariants."""

import unittest

import numpy as np
import pandas as pd

from sessions.ch11.imputation import load_smoothed_input
from sessions.ch11.stl_imputation import seasonal_imputation, stl_impute, summarize_stages


class STLImputationTests(unittest.TestCase):
    def test_known_season_recovers_linear_deseasonalized_gap(self):
        index = pd.date_range("2020-01-05", periods=8, freq="W-SUN")
        season = pd.Series([0, 3, 0, -3, 0, 3, 0, -3], index=index, dtype=float)
        trend = pd.Series(10 + np.arange(8), index=index, dtype=float)
        source = trend + season
        expected = source.copy()
        source.iloc[2:5] = np.nan
        original = source.copy()
        gapped, filled, final = seasonal_imputation(source, season)
        pd.testing.assert_series_equal(gapped.isna(), source.isna())
        np.testing.assert_allclose(filled, trend)
        np.testing.assert_allclose(final, expected)
        pd.testing.assert_series_equal(source, original)

    def test_rejects_misaligned_season_and_boundary_gaps(self):
        index = pd.date_range("2020-01-05", periods=120, freq="W-SUN")
        source = pd.Series(np.arange(120, dtype=float), index=index)
        with self.assertRaises(ValueError):
            seasonal_imputation(source, source.iloc[:-1])
        source.iloc[0] = np.nan
        with self.assertRaises(ValueError):
            stl_impute(source)
        with self.assertRaises(ValueError):
            stl_impute(source.iloc[:60])

    def test_synthetic_additive_reconstruction_and_no_missing_reuse(self):
        index = pd.date_range("2020-01-05", periods=160, freq="W-SUN")
        t = np.arange(160)
        source = pd.Series(100 + 0.5 * t + 10 * np.sin(2 * np.pi * t / 8), index=index)
        source.iloc[42:47] = np.nan
        config = {"period": 8, "seasonal": 7, "trend": 15, "low_pass": 9, "robust": True}
        stages, _ = stl_impute(source, config)
        np.testing.assert_allclose(stages.trend + stages.seasonal + stages.residual,
                                   stages.preliminary_linear, atol=1e-10)
        self.assertEqual(stages.deseasonalized_gaps.isna().sum(), 5)
        self.assertEqual(stages.final_imputed.isna().sum(), 0)
        self.assertTrue(np.array_equal(stages.final_imputed[source.notna()], source.dropna()))

    def test_actual_approved_data_all_stages(self):
        _, source = load_smoothed_input()
        original = source.copy()
        stages, _ = stl_impute(source)
        result = summarize_stages(stages)
        self.assertEqual(result["rows"], 1044)
        self.assertEqual(result["observed"], 677)
        self.assertEqual(result["missing_deseasonalized"], 367)
        self.assertEqual(result["missing_final"], 0)
        self.assertTrue(result["same_deseasonalized_mask"])
        self.assertTrue(result["observed_exactly_preserved"])
        self.assertLess(result["additive_reconstruction_max_abs"], 1e-9)
        self.assertTrue(np.isfinite(stages.drop(columns=["smoothed_gaps", "deseasonalized_gaps"])).all().all())
        pd.testing.assert_series_equal(source, original)


if __name__ == "__main__":
    unittest.main()

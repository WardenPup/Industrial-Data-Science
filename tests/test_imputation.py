"""Independent analytical examples for Exercise 11.2."""

import unittest

import numpy as np
import pandas as pd

from sessions.ch11.imputation import impute_series, load_smoothed_input, gap_table, METHODS, summarize_methods


class ImputationTests(unittest.TestCase):
    def series(self, values):
        return pd.Series(values, index=pd.date_range("2020-01-05", periods=len(values), freq="W-SUN"), dtype=float)

    def test_linear_ramp_and_no_mutation(self):
        source = self.series([0, 1, 2, np.nan, np.nan, 5, 6, 7, 8, 9])
        original = source.copy()
        for method in ["linear", "polynomial2", "polynomial5", "pchip"]:
            np.testing.assert_allclose(impute_series(source, method), np.arange(10), atol=1e-12)
        pd.testing.assert_series_equal(source, original)
        np.testing.assert_allclose(impute_series(source, "ffill").iloc[3:5], [2, 2])
        np.testing.assert_allclose(impute_series(source, "bfill").iloc[3:5], [5, 5])

    def test_boundary_policy(self):
        source = self.series([np.nan, 1, 2, 3, 4, 5, 6, 7, np.nan])
        self.assertTrue(np.isnan(impute_series(source, "ffill").iloc[0]))
        self.assertEqual(impute_series(source, "ffill").iloc[-1], 7)
        self.assertEqual(impute_series(source, "bfill").iloc[0], 1)
        self.assertTrue(np.isnan(impute_series(source, "bfill").iloc[-1]))
        for method in ["linear", "polynomial2", "polynomial5", "pchip"]:
            self.assertTrue(impute_series(source, method).iloc[[0, -1]].isna().all())

    def test_quadratic_interpolation(self):
        x = np.arange(10, dtype=float)
        source = self.series(x ** 2)
        source.iloc[3:5] = np.nan
        np.testing.assert_allclose(impute_series(source, "polynomial2"), x ** 2, atol=1e-12)

    def test_gap_description_and_anchor_diagnostic(self):
        source = self.series([0, np.nan, np.nan, 3, 4, 5, 6])
        gaps = gap_table(source)
        self.assertEqual(gaps.weeks.tolist(), [2])
        self.assertEqual(gaps.left.iloc[0], 0)
        self.assertEqual(gaps.right.iloc[0], 3)
        result = impute_series(source, "linear")
        summary = summarize_methods(source, pd.DataFrame({"linear": result}))
        self.assertEqual(summary.loc["linear", "filled"], 2)
        self.assertEqual(summary.loc["linear", "outside_gap_anchors"], 0)

    def test_invalid_method_calendar_and_insufficient_support(self):
        source = self.series([1, np.nan, 3])
        with self.assertRaises(ValueError):
            impute_series(source, "unknown")
        with self.assertRaises(ValueError):
            impute_series(source, "polynomial5")
        with self.assertRaises(ValueError):
            impute_series(source.iloc[::-1], "linear")

    def test_official_input_and_preserved_known_values(self):
        frame, source = load_smoothed_input()
        self.assertEqual(len(frame), 1044)
        self.assertEqual(source.isna().sum(), 367)
        self.assertEqual(len(gap_table(source)), 32)
        self.assertEqual(gap_table(source).weeks.max(), 23)
        for method in METHODS:
            result = impute_series(source, method)
            self.assertEqual(result.isna().sum(), 0)
            pd.testing.assert_series_equal(result[source.notna()], source.dropna())


if __name__ == "__main__":
    unittest.main()

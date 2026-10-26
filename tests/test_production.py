"""Independent small examples for scientific smoothing invariants."""

import unittest

import numpy as np
import pandas as pd

from sessions.ch11.production import load_production, smooth_with_gaps


class ProductionTests(unittest.TestCase):
    def test_isolated_spike_robustness(self):
        values = pd.Series([10., 10., 1000., 10., 10.])
        self.assertEqual(smooth_with_gaps(values).iloc[2], 10.)
        self.assertEqual(smooth_with_gaps(values, aggregation="mean").iloc[2], 208.)

    def test_mask_edges_and_sparse_windows(self):
        values = pd.Series([np.nan, 10., np.nan, np.nan, 20., np.nan, np.nan])
        original = values.copy()
        result = smooth_with_gaps(values)
        pd.testing.assert_series_equal(result.isna(), values.isna())
        self.assertEqual(result.iloc[1], 10.)
        self.assertEqual(result.iloc[4], 20.)
        pd.testing.assert_series_equal(values, original)

    def test_even_support_median_and_boundaries(self):
        values = pd.Series([0., 10., np.nan, 30., 40.])
        result = smooth_with_gaps(values)
        self.assertEqual(result.iloc[0], 5.)
        self.assertEqual(result.iloc[1], 10.)
        self.assertEqual(result.iloc[4], 35.)

    def test_all_missing_and_window_validation(self):
        self.assertTrue(smooth_with_gaps(pd.Series([np.nan] * 5)).isna().all())
        for window in [0, 2, -1, True, 2.5]:
            with self.assertRaises(ValueError):
                smooth_with_gaps(pd.Series([1.]), window)
        with self.assertRaises(ValueError):
            smooth_with_gaps(pd.Series([1.]), aggregation="sum")

    def test_official_data_calendar_and_gaps(self):
        frame = load_production()
        self.assertEqual(len(frame), 1044)
        self.assertEqual(frame.pieces_gaps.isna().sum(), 367)
        pd.testing.assert_series_equal(smooth_with_gaps(frame.pieces_gaps).isna(),
                                       frame.pieces_gaps.isna())


if __name__ == "__main__":
    unittest.main()

"""Numerical and binning checks for 10.3's descriptive analysis."""

import unittest

import numpy as np
import pandas as pd

from sessions.ch10.ai4i_data import load_ai4i
from sessions.ch10.ai4i_eda import AIR, MEASUREMENTS, SPEED, TORQUE, add_bins, iqr_summary, pearson_reference, strongest_pair


class AI4IEDATests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = load_ai4i()

    def test_iqr_on_known_values(self):
        report = iqr_summary(pd.DataFrame({"x": [0, 1, 2, 3, 100]}))
        self.assertEqual(report.loc["x", "lower_fence"], -2)
        self.assertEqual(report.loc["x", "upper_fence"], 6)
        self.assertEqual(report.loc["x", "flagged_count"], 1)

    def test_bins_cover_all_observations_without_mutation(self):
        original = self.data.copy()
        binned, edges = add_bins(self.data)
        pd.testing.assert_frame_equal(self.data, original)
        for column, expected in (("speed_band", 3), ("torque_band", 10)):
            self.assertEqual(len(binned[column].cat.categories), expected)
            self.assertEqual(int(binned[column].value_counts(sort=False).sum()), 10000)
            self.assertFalse(binned[column].isna().any())
        self.assertTrue(np.all(np.diff(edges["speed_edges"]) > 0))

    def test_decimal_values_on_iqr_fences_are_not_outliers(self):
        values = pd.DataFrame({"x": [12.8, 33.2, 33.2, 40, 46.8, 46.8, 67.2]})
        self.assertEqual(iqr_summary(values).loc["x", "flagged_count"], 0)

    def test_pearson_matches_independent_reference(self):
        corr = self.data[MEASUREMENTS].corr()
        self.assertAlmostEqual(corr.loc[TORQUE, SPEED], pearson_reference(self.data[TORQUE], self.data[SPEED]), places=12)
        np.testing.assert_allclose(corr, corr.T)
        np.testing.assert_allclose(np.diag(corr), 1)
        self.assertTrue(((corr >= -1) & (corr <= 1)).all().all())

    def test_strongest_pair_excludes_diagonal_and_uses_magnitude(self):
        corr = pd.DataFrame([[1, -0.9, 0.2], [-0.9, 1, 0.1], [0.2, 0.1, 1]], columns=MEASUREMENTS, index=MEASUREMENTS)
        self.assertEqual(strongest_pair(corr), (TORQUE, SPEED, -0.9))


if __name__ == "__main__":
    unittest.main()

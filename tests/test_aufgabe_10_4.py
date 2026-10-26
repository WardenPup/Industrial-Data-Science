"""Independent numerical checks for claims actually made in the paper."""

import unittest
from decimal import Decimal

import numpy as np
from scipy.stats import spearmanr

from sessions.ch10.ai4i_eda import AIR, SPEED, TORQUE
from sessions.ch10.report_10_4 import report_data


class ReportClaims(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data, cls.summary, cls.pearson, cls.spearman, cls.iqr = report_data()

    def test_correlations_against_independent_libraries(self):
        for a, b in [(TORQUE, SPEED), (TORQUE, AIR), (SPEED, AIR)]:
            self.assertAlmostEqual(self.pearson.loc[a, b], np.corrcoef(self.data[a], self.data[b])[0, 1], places=12)
            self.assertAlmostEqual(self.spearman.loc[a, b], spearmanr(self.data[a], self.data[b]).statistic, places=12)

    def test_rounded_paper_values_and_decimal_fences(self):
        self.assertEqual(round(self.data[TORQUE].mean(), 3), 39.987)
        self.assertEqual((self.data[TORQUE].min(), self.data[TORQUE].max()), (3.8, 76.6))
        for column, low, high, count in [(TORQUE, '12.8', '67.2', 64),
                                         (SPEED, '1139.5', '1895.5', 418),
                                         (AIR, '293.5', '306.3', 0)]:
            exact = [Decimal(str(v)) for v in self.data[column]]
            flagged = sum(v < Decimal(low) or v > Decimal(high) for v in exact)
            self.assertEqual(flagged, count)
            self.assertEqual(self.iqr.loc[column, 'flagged_count'], count)
        self.assertEqual(int((self.data[SPEED] < 1139.5).sum()), 0)

    def test_published_quartiles_and_distribution_claims(self):
        for column, q1, q3 in [(TORQUE, 33.2, 46.8), (SPEED, 1423.0, 1612.0),
                               (AIR, 298.3, 301.5)]:
            self.assertAlmostEqual(float(self.data[column].quantile(0.25)), q1)
            self.assertAlmostEqual(float(self.data[column].quantile(0.75)), q3)
        self.assertLess(abs(self.data[TORQUE].skew()), 0.1)
        self.assertGreater(self.data[SPEED].skew(), 1.0)
        self.assertLess(abs(self.data[AIR].skew()), 0.2)


if __name__ == '__main__':
    unittest.main()

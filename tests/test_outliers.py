"""Threshold boundaries, invariants and course-data integration."""
import unittest
import numpy as np
import pandas as pd
from sessions.ch11.outliers import sigma_flags, detect_outliers
from sessions.ch11.production import load_production

class OutlierTests(unittest.TestCase):
    def test_strict_boundary_and_sample_std(self):
        values = pd.Series([-1., 0., 1.], index=["a", "b", "c"])
        flags, lower, upper = sigma_flags(values, 1)
        self.assertEqual((lower, upper), (-1., 1.))
        self.assertFalse(flags.any())
        self.assertTrue(flags.index.equals(values.index))
        self.assertEqual(sigma_flags(values, .5)[0].tolist(), [True, False, True])

    def test_constant_and_invalid(self):
        self.assertFalse(sigma_flags(pd.Series([4.,4.,4.]))[0].any())
        for values in [[1.], [1., np.nan], [1., np.inf]]:
            with self.assertRaises(ValueError): sigma_flags(pd.Series(values))
        with self.assertRaises(ValueError): sigma_flags(pd.Series([1.,2.]), -1)

    def test_original_data_and_independent_threshold(self):
        source=load_production().pieces.copy()
        before=source.copy(deep=True)
        table, lower, upper=detect_outliers(source)
        pd.testing.assert_series_equal(source,before)
        np.testing.assert_array_equal(table.pieces,source)
        np.testing.assert_allclose(table.trend+table.seasonal+table.residual,source,atol=1e-10)
        residual=table.residual.to_numpy()
        mean=sum(residual)/len(residual)
        std=(sum((r-mean)**2 for r in residual)/(len(residual)-1))**.5
        np.testing.assert_array_equal(table.outlier_candidate, np.abs(residual-mean)>3*std)
        self.assertEqual(int(table.outlier_candidate.sum()),26)
        self.assertEqual(int((table.residual>upper).sum()),0)
        with self.assertRaises(ValueError): detect_outliers(source.iloc[::-1])
        broken=source.copy();broken.iloc[1]=np.nan
        with self.assertRaises(ValueError): detect_outliers(broken)

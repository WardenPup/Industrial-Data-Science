"""Scientific contracts for the additional interval classifier."""
import unittest
from unittest.mock import patch

import numpy as np
from aeon.classification.interval_based import TimeSeriesForestClassifier
from aeon.utils.numba.stats import row_mean, row_std, row_slope

from sessions.ch12 import forest
from sessions.ch12.classification import load_uwave, transform


class ForestTests(unittest.TestCase):
    def test_interval_statistics_against_aeon(self):
        for values in [np.array([1., 3., 5., 7.]), np.ones(5), np.array([3., -2., 8., 0.])]:
            expected = [feature(values[None, :])[0] for feature in [row_mean, row_std, row_slope]]
            np.testing.assert_allclose(forest.interval_statistics(values), expected, atol=1e-12)
        np.testing.assert_allclose(forest.interval_statistics([1, 3, 5, 7]), [4, np.sqrt(5), 2])

    def test_actual_training_boundary(self):
        train = np.arange(8*3*12, dtype=float).reshape(8, 3, 12)
        labels = np.array(['a', 'b']*4)
        original = train.copy()
        with patch.object(forest, 'TimeSeriesForestClassifier') as constructor:
            model, scaler, seconds = forest.fit_forest(train, labels)
            constructor.assert_called_once_with(**forest.CONFIG)
            args = constructor.return_value.fit.call_args.args
            np.testing.assert_array_equal(args[0], transform(train, scaler))
            np.testing.assert_array_equal(args[1], labels)
            np.testing.assert_allclose(scaler[0], train.mean(axis=(0, 2), keepdims=True))
            self.assertGreaterEqual(seconds, 0)
        np.testing.assert_array_equal(train, original)

    def test_multichannel_seed_and_probabilities(self):
        rng = np.random.default_rng(17)
        x = rng.normal(size=(16, 3, 30)); y = np.array(['a', 'b']*8)
        x[y == 'b', 2, 10:20] += 5
        settings = dict(n_estimators=4, n_intervals=3, random_state=42, n_jobs=1)
        first = TimeSeriesForestClassifier(**settings).fit(x, y)
        second = TimeSeriesForestClassifier(**settings).fit(x, y)
        a = first.predict_proba(x); b = second.predict_proba(x)
        np.testing.assert_array_equal(a, b)
        np.testing.assert_allclose(a.sum(axis=1), 1)
        np.testing.assert_array_equal(first.predict(x), first.classes_[a.argmax(axis=1)])
        manual = np.mean([tree.predict_proba(interval[0].transform(x)) for tree, interval
                          in zip(first.estimators_, first.intervals_)], axis=0)
        np.testing.assert_allclose(a, manual, atol=1e-12)

    def test_invalid_values_and_labels(self):
        x = np.ones((4, 3, 12))
        for labels in [['a']*4, ['a', 'b'], [['a'], ['b'], ['a'], ['b']]]:
            with self.assertRaises(ValueError): forest.fit_forest(x, labels)
        x[0, 0, 0] = np.nan
        with self.assertRaises(ValueError): forest.fit_forest(x, ['a', 'b']*2)
        for values in [[1, 2], [1, np.inf, 3]]:
            with self.assertRaises(ValueError): forest.interval_statistics(values)

    def test_approved_reference_identity_and_order(self):
        _, labels = load_uwave('TEST')
        table, _ = forest.load_reference(labels)
        self.assertEqual(len(table), 320)
        wrong = labels.copy(); wrong[0] = 'wrong'
        with self.assertRaises(AssertionError): forest.load_reference(wrong)


if __name__ == '__main__': unittest.main()

"""Focused scientific and split-integrity checks for Exercise 14.2."""
import unittest
import numpy as np
import pandas as pd
from unittest.mock import patch
from sessions.ch14.overstrain import prepare, analyze, GROUPS, TORQUE
from sessions.ch14.tool_wear import load_data, WEAR

class OverstrainTests(unittest.TestCase):
    def test_feature_definition_and_nonmutation(self):
        data = load_data(); before = data.copy(deep=True); result = prepare(data)
        pd.testing.assert_frame_equal(data, before)
        np.testing.assert_array_equal(result.wearadjTorque, data[TORQUE]*data[WEAR])
        for variant in ["M", "H"]:
            np.testing.assert_array_equal(result["Type_"+variant], data.Type.eq(variant).astype(int))
        for columns in GROUPS.values():
            self.assertFalse(set(columns) & {"UDI", "Product ID", "OSF", "Machine failure", "TWF", "PWF", "HDF", "RNF"})

    def test_rule_and_comparison(self):
        data, fit, heldout, models, summary = analyze()
        self.assertEqual((summary["rows"], summary["osf"], summary["rule_mismatches"]), (10000, 98, 0))
        rule = data.wearadjTorque > data.Type.map({"L":11000,"M":12000,"H":13000})
        np.testing.assert_array_equal(rule.astype(int), data.OSF)
        self.assertEqual(len(fit), 24)
        self.assertEqual(heldout.Fehler.tolist(), [14, 8, 1])
        np.testing.assert_allclose(heldout.F1, [22/36, .8, 38/39])
        self.assertEqual(fit.loc[(fit.Merkmale == "+ Produkt + Type") & (fit.Tiefe == 3), "Fehler"].item(), 2)
        self.assertTrue((fit.loc[(fit.Merkmale == "+ Produkt + Type") & (fit.Tiefe < 3), "Fehler"] > 2).all())

    def test_split_is_disjoint_and_test_never_fitted(self):
        from sklearn.tree import DecisionTreeClassifier
        original = DecisionTreeClassifier.fit
        fitted_indices = []
        def record(model, X, y, *args, **kwargs):
            fitted_indices.append(X.index.to_numpy())
            return original(model, X, y, *args, **kwargs)
        with patch.object(DecisionTreeClassifier, "fit", record):
            data, fit, heldout, models, summary = analyze()
        train = fitted_indices[-1]
        test = data.index.difference(train)
        self.assertEqual(len(train), 8000); self.assertEqual(len(test), 2000)
        self.assertEqual(len(np.intersect1d(train,test)), 0)
        for indices in fitted_indices[-3:]:
            np.testing.assert_array_equal(indices, train)
        self.assertEqual(summary["train_osf"] + summary["test_osf"], 98)
        self.assertEqual(summary["test_osf"], 20)

if __name__ == "__main__":
    unittest.main()

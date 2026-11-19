"""Three focused scientific checks for Exercise 14.3."""
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sessions.ch14.engineered_features import prepare, analyze, BASE, FEATURES
from sessions.ch14.tool_wear import load_data

class EngineeredFeatureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fits = []
        original = DecisionTreeClassifier.fit
        def record(model, X, y, *args, **kwargs):
            cls.fits.append((X.index.to_numpy(), list(X.columns), model.get_params()))
            return original(model, X, y, *args, **kwargs)
        with patch.object(DecisionTreeClassifier, "fit", record):
            cls.data, cls.metrics, cls.predictions, cls.splits, cls.counts = analyze()

    def test_physical_features_and_unchanged_source(self):
        data = load_data(); before = data.copy(deep=True); prepared = prepare(data)
        pd.testing.assert_frame_equal(data, before)
        np.testing.assert_allclose(prepared.temp_diff, data["Process temperature [K]"]-data["Air temperature [K]"])
        np.testing.assert_allclose(prepared.power, data["Torque [Nm]"]*data["Rotational speed [rpm]"]*2*np.pi/60)
        self.assertEqual(self.counts.Positive.tolist(), [115,95])
        self.assertEqual(self.counts["TEST positiv"].tolist(), [23,19])

    def test_train_only_and_fair_comparison(self):
        self.assertEqual(len(self.fits), 32)
        for j, (target, feature) in enumerate(FEATURES.items()):
            split = self.splits.loc[self.splits.Ziel == target]
            train = set(split.loc[split.Split == "TRAIN", "UDI"]-1)
            test = set(split.loc[split.Split == "TEST", "UDI"]-1)
            self.assertEqual(len(train),8000); self.assertEqual(len(test),2000)
            self.assertFalse(train & test); self.assertEqual(train|test,set(range(10000)))
            for k, (indices, columns, params) in enumerate(self.fits[j*16:(j+1)*16]):
                self.assertEqual(set(indices),train)
                self.assertEqual(columns,BASE if k<8 else BASE+[feature])
                self.assertEqual(params["random_state"],42)
                self.assertEqual(params["min_samples_leaf"],5)
                self.assertEqual(params["min_samples_split"],5)
                self.assertEqual(params["max_depth"],k%8+1)

    def test_f1_and_exportable_predictions(self):
        m=self.metrics
        self.assertEqual(len(m),64)
        np.testing.assert_allclose(m.F1,2*m.TP/(2*m.TP+m.FP+m.FN))
        self.assertTrue((m.Fehler==m.FP+m.FN).all())
        for target in FEATURES:
            p=self.predictions.loc[self.predictions.Ziel==target]
            self.assertEqual(len(p),2000); self.assertEqual(p.UDI.nunique(),2000)
            np.testing.assert_array_equal(p.Wahr,self.data.set_index("UDI").loc[p.UDI,target])
            for variant in ["Basis","+ Merkmal"]:
                y, pred=p.Wahr.to_numpy(),p[variant].to_numpy()
                tp=((y==1)&(pred==1)).sum();fp=((y==0)&(pred==1)).sum();fn=((y==1)&(pred==0)).sum()
                row=m.loc[(m.Ziel==target)&(m.Variante==variant)&(m.Tiefe==3)&(m.Split=="TEST")].iloc[0]
                self.assertEqual((row.TP,row.FP,row.FN),(tp,fp,fn))
        values=m.loc[(m.Tiefe==3)&(m.Split=="TEST"),"F1"]
        np.testing.assert_allclose(values,[22/36,40/43,30/38,1])

if __name__=="__main__":
    unittest.main()

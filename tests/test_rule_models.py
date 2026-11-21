"""Focused rule boundaries, leakage protection and metric verification."""
import unittest
import numpy as np
from sklearn.metrics import confusion_matrix, f1_score
from sessions.ch15.drilling_data import load_data, SUBGROUPS
from sessions.ch15.rule_models import evaluate, split_data, FEATURES, RULES, predict_bef, predict_fwf, predict_wdf
class RuleModelTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load_data();cls.result=evaluate(cls.data)
    def test_rule_boundaries_without_labels(self):
        d=self.data.iloc[:4][FEATURES].copy()
        d["Cutting speed vc [m/min]"]=[22,22.01,29.70,29.71]
        d["Cooling [%]"]=[25,25,50,50]
        d["Material"]=["P","P","N","N"]
        d["Drill Bit Type"]=["N","H","W","N"]
        d["Feed rate vf [mm/min]"]=[100,100,206,206]
        self.assertEqual(predict_bef(d).tolist(),[1,0,0,0])
        self.assertEqual(predict_fwf(d).tolist(),[0,0,1,0])
        self.assertEqual(predict_wdf(d).tolist(),[0,1,0,1])
        for f in RULES.values():self.assertTrue(f(d).isin([0,1]).all())
    def test_shared_split_and_train_only_fit(self):
        train,test=split_data(self.data)
        self.assertFalse(set(map(tuple,self.data.iloc[train][FEATURES].to_numpy())) & set(map(tuple,self.data.iloc[test][FEATURES].to_numpy())))
        altered=self.data.copy();altered.loc[altered.index[test],SUBGROUPS]=1-altered.loc[altered.index[test],SUBGROUPS]
        changed=evaluate(altered)
        for flag in SUBGROUPS:
            before=self.result[4][flag];after=changed[4][flag]
            self.assertLessEqual(before[-1].get_depth(),3)
            np.testing.assert_array_equal(before.predict(self.data[FEATURES]),after.predict(self.data[FEATURES]))
        self.assertNotIn("ID",FEATURES);self.assertFalse(set(SUBGROUPS)&set(FEATURES))
    def test_all_prediction_metrics(self):
        metrics,predictions,split,counts,models,texts=self.result
        self.assertEqual(len(metrics),8);self.assertEqual(len(predictions),4*split.Split.eq("TEST").sum())
        for row in metrics.to_dict("records"):
            p=predictions.loc[predictions.Fehlertyp.eq(row["Fehlertyp"])]
            np.testing.assert_array_equal([row[k] for k in ["TN","FP","FN","TP"]],confusion_matrix(p.Ist,p[row["Methode"]],labels=[0,1]).ravel())
            self.assertAlmostEqual(row["F1"],f1_score(p.Ist,p[row["Methode"]],zero_division=0))
if __name__=="__main__":unittest.main()

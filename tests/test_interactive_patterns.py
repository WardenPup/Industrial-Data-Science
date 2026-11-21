"""Three focused data/category/selection checks using the existing environment."""
import unittest
import pandas as pd
import numpy as np
from sessions.ch15.interactive_patterns import prepare,figure,notebook_widget,MATERIAL,DRILL
from sessions.ch15.drilling_data import load_data,SUBGROUPS
from sessions.ch15.exploration import NUMERIC
class InteractivePatternTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.data=prepare()
    def test_source_and_complete_dimensions(self):
        raw=load_data()
        for column in raw:np.testing.assert_array_equal(self.data[column].to_numpy(),raw[column].to_numpy())
        for column in ["Material","Drill Bit Type"]+SUBGROUPS:self.assertIsInstance(self.data[column].dtype,pd.CategoricalDtype)
        for flag in SUBGROUPS:
            trace=figure(self.data,flag).data[0]
            self.assertEqual([d.name for d in trace.dimensions],NUMERIC+["Material","Drill Bit Type","failure"])
            for d in trace.dimensions:self.assertEqual(len(d.values),20000)
            np.testing.assert_array_equal(trace.dimensions[-1].values,raw[flag])
            np.testing.assert_array_equal(trace.line.color,raw.Material.map(MATERIAL))
    def test_material_and_multiple_label_selections(self):
        data=self.data;flags=data[SUBGROUPS].astype(int)
        self.assertEqual(flags.sum().tolist(),[215,344,278,300])
        selected=data.loc[flags.FWF.eq(1)&data.Material.eq("N")]
        self.assertEqual(len(selected),270)
        selected=selected.loc[selected["Drill Bit Type"].isin(["N","H"])]
        self.assertEqual(len(selected),9);self.assertTrue(selected.WDF.astype(int).eq(1).all())
        self.assertEqual(int((flags.CCF.eq(1)&flags.WDF.eq(1)).sum()),106)
    def test_actual_jupyter_callback(self):
        view,choice=notebook_widget(self.data);before=view.children[1].value
        choice.value="FWF";self.assertNotEqual(view.children[1].value,before)
        self.assertEqual(list(choice.options),SUBGROUPS)
        self.assertIn("FWF",view.children[1].value)
        choice.close();view.close()
if __name__=="__main__":unittest.main()

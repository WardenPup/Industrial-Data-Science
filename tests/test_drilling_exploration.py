"""Three focused checks for grouped descriptive statistics; no model tests."""
import unittest
import numpy as np
import pandas as pd
from sessions.ch15.drilling_data import load_data,SUBGROUPS
from sessions.ch15.exploration import summarize,NUMERIC,CATEGORICAL

class ExplorationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=load_data();cls.tables=summarize(cls.data)
    def test_all_feature_groups_and_nonmutation(self):
        before=self.data.copy(deep=True);tables=summarize(self.data)
        pd.testing.assert_frame_equal(self.data,before)
        self.assertEqual(len(tables["numeric_summary"]),56)
        self.assertEqual(len(tables["categorical_summary"]),48)
        self.assertEqual(len(tables["positive_bounds"]),28)
        for flag in SUBGROUPS:
            for feature in NUMERIC:
                rows=tables["numeric_summary"].loc[lambda x:(x.Fehlertyp==flag)&(x.Merkmal==feature)]
                self.assertEqual(rows["count"].sum(),20000)
            for value in [0,1]:
                for feature in CATEGORICAL:
                    rows=tables["categorical_summary"].loc[lambda x:(x.Fehlertyp==flag)&(x.Flag==value)&(x.Merkmal==feature)]
                    self.assertAlmostEqual(rows["Anteil [%]"].sum(),100)
    def test_manual_fixture_statistics(self):
        data=pd.DataFrame({"ID":range(1,7),**{c:[1.,2.,3.,4.,5.,6.] for c in NUMERIC},"Material":["P"]*6,"Drill Bit Type":["N"]*6,**{c:[1,1,1,0,0,0] for c in SUBGROUPS}})
        row=summarize(data)["numeric_summary"].iloc[1]
        self.assertEqual(row["count"],3);self.assertEqual(row["mean"],5)
        self.assertEqual(row["std"],1);self.assertEqual(row["25%"],4.5)
        self.assertEqual(row["50%"],5);self.assertEqual(row["75%"],5.5)
    def test_material_context_and_category_pair_totals(self):
        m=self.tables["fwf_material_summary"]
        n=m.loc[(m.Material=="N")&(m.FWF==1)&(m.Merkmal==NUMERIC[0])].iloc[0]
        self.assertEqual(n["n"],270);self.assertAlmostEqual(n["Median"],29.6)
        self.assertAlmostEqual(n["max"],29.7)
        pairs=self.tables["wdf_pairs"]
        self.assertEqual(pairs.Zeilen.sum(),20000);self.assertEqual(pairs.WDF.sum(),300)
        self.assertEqual(len(pairs),9)
        self.assertEqual(set(pairs["WDF-Anteil [%]"]),{0.,100.})
        bef=self.tables["positive_bounds"].loc[lambda x:(x.Fehlertyp=="BEF")&(x.Merkmal==NUMERIC[0])].iloc[0]
        self.assertEqual(bef["Maximum markiert"],22.)

if __name__=="__main__":unittest.main()

"""Three focused source/label-integrity tests, without model training."""
import unittest
from pathlib import Path
import tempfile
import pandas as pd
import numpy as np
from sessions.ch15.drilling_data import load_data,label_tables,verify_file,TARGETS,SUBGROUPS

class DrillingTests(unittest.TestCase):
    def test_pinned_source_and_known_counts(self):
        data=load_data();self.assertEqual(data.shape,(20000,15))
        self.assertFalse(data.isna().any().any());self.assertEqual(data.ID.nunique(),20000)
        counts,cross,multi,conflicts,multiple=label_tables(data)
        self.assertEqual(counts.Markiert.tolist(),[1001,215,344,278,300])
        np.testing.assert_array_equal(cross,[[18999,0],[0,1001]])
        self.assertEqual(multi.Zeilen.tolist(),[18999,887,92,22,0])
        self.assertTrue(conflicts.empty);self.assertEqual(len(multiple),114)
        self.assertEqual(data.drop(columns="ID").duplicated().sum(),2)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/"modified.csv";p.write_bytes(b"not the original")
            with self.assertRaises(ValueError):verify_file(p)

    def test_union_multiple_labels_and_nonmutation(self):
        data=pd.DataFrame({"ID":[1,2,3,4],"Main Failure":[0,1,0,1],"BEF":[0,1,1,0],"CCF":[0,1,0,0],"FWF":[0,0,0,0],"WDF":[0,0,0,0]})
        before=data.copy(deep=True)
        counts,cross,multi,conflicts,multiple=label_tables(data)
        pd.testing.assert_frame_equal(data,before)
        self.assertEqual(conflicts.ID.tolist(),[3,4])
        self.assertEqual(multiple.ID.tolist(),[2])
        self.assertEqual(cross.loc[0,1],1);self.assertEqual(cross.loc[1,0],1)
        self.assertEqual(multi.Zeilen.tolist(),[2,1,1,0,0])

    def test_invalid_labels_are_not_silently_counted(self):
        data=pd.DataFrame({"ID":[1],**{f:[0] for f in TARGETS}})
        for value in [2,np.nan]:
            invalid=data.copy();invalid["BEF"]=value
            with self.assertRaises(ValueError):label_tables(invalid)

if __name__=="__main__":unittest.main()

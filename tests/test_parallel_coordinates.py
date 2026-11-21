"""Focused checks of actual categorical dimensions, data and notebook callback."""
import unittest
import numpy as np
import pandas as pd
from sessions.ch14.parallel_coordinates import prepare,figure,notebook_widget,CONTINUOUS,TYPE_CODES
from sessions.ch14.tool_wear import load_data,FLAGS

class ParallelCoordinateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data=prepare()
    def test_original_data_and_categorical_flags(self):
        raw=load_data()
        for column in raw:
            np.testing.assert_array_equal(self.data[column].to_numpy(),raw[column].to_numpy())
        for column in FLAGS+["Type"]:
            self.assertIsInstance(self.data[column].dtype,pd.CategoricalDtype)
        self.assertEqual(self.data[FLAGS].astype(int).sum().tolist(),[339,46,115,95,98,19])
        np.testing.assert_allclose(self.data.temp_diff,raw["Process temperature [K]"]-raw["Air temperature [K]"])
        np.testing.assert_allclose(self.data.power,raw["Torque [Nm]"]*raw["Rotational speed [rpm]"]*2*np.pi/60)
        np.testing.assert_allclose(self.data.wearadjTorque,raw["Torque [Nm]"]*raw["Tool wear [min]"])
    def test_complete_dimensions_and_discrete_colors(self):
        for target in FLAGS:
            trace=figure(self.data,target).data[0]
            self.assertEqual([d.name for d in trace.dimensions],CONTINUOUS+["Type","failure"])
            for dimension in trace.dimensions:
                self.assertEqual(len(dimension.values),10000)
            np.testing.assert_array_equal(trace.dimensions[-1].values,self.data[target].astype(int))
            self.assertEqual(list(trace.dimensions[-1].tickvals),[0,1])
            np.testing.assert_array_equal(trace.line.color,self.data.Type.map(TYPE_CODES).astype(int))
        with self.assertRaises(ValueError):figure(self.data,"unknown")
    def test_real_jupyter_dropdown_callback(self):
        view,dropdown=notebook_widget(self.data)
        self.assertEqual(dropdown.value,"HDF")
        before=view.children[1].value
        dropdown.value="PWF"
        self.assertNotEqual(view.children[1].value,before)
        self.assertIn('PWF',view.children[1].value)
        self.assertEqual(list(dropdown.options),FLAGS)
        dropdown.close();view.close()

if __name__=="__main__":unittest.main()

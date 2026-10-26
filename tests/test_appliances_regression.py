"""Regression contracts: numerical meaning, leakage boundaries and reproducibility."""
import unittest
from unittest.mock import patch
import numpy as np
import pandas as pd
import torch
from aeon.regression.distance_based import KNeighborsTimeSeriesRegressor
from aeon.regression.interval_based import TimeSeriesForestRegressor
from sessions.ch12 import regression as study


class AppliancesTests(unittest.TestCase):
    def test_raw_shapes_and_targets(self):
        for split, cases in [('TRAIN',95),('TEST',42)]:
            x,y=study.load_appliances(split)
            self.assertEqual(x.shape,(cases,24,144));self.assertEqual(y.shape,(cases,))
            self.assertTrue(np.isfinite(x).all() and np.isfinite(y).all())

    def test_actual_train_only_boundary(self):
        x=np.arange(8*24*20,dtype=float).reshape(8,24,20);y=np.arange(8,dtype=float)
        with patch.object(study,'KNeighborsTimeSeriesRegressor') as knn, patch.object(study,'TimeSeriesForestRegressor') as forest, patch.object(study,'fit_cnn',return_value=(object(),(3.5,1),pd.DataFrame())) as cnn:
            fitted=study.fit_regressors(x,y)
            knn.assert_called_once_with(**study.KNN_CONFIG);forest.assert_called_once_with(**study.FOREST_CONFIG)
            expected=study.transform(x,fitted['scaler'])
            for call in [knn.return_value.fit.call_args,forest.return_value.fit.call_args,cnn.call_args]:
                np.testing.assert_array_equal(call.args[0],expected);np.testing.assert_array_equal(call.args[1],y)
            np.testing.assert_allclose(fitted['scaler'][0],x.mean(axis=(0,2),keepdims=True))
            before=fitted['scaler'][0].copy();study.transform(x+10000,fitted['scaler'])
            np.testing.assert_array_equal(before,fitted['scaler'][0])

    def test_knn_is_neighbor_target_mean(self):
        x=np.repeat(np.array([0.,1.,3.,5.])[:,None,None],12,axis=2)
        y=np.array([10.,20.,40.,80.]);query=np.full((1,1,12),1.2)
        model=KNeighborsTimeSeriesRegressor(n_neighbors=3,distance='dtw',distance_params={'window':.1}).fit(x,y)
        np.testing.assert_allclose(model.predict(query),[70/3])

    def test_forest_is_mean_of_regression_trees(self):
        rng=np.random.default_rng(3);x=rng.normal(size=(10,3,20));y=np.arange(10,dtype=float)
        model=TimeSeriesForestRegressor(n_estimators=3,n_intervals=2,random_state=42).fit(x,y)
        expected=np.mean([tree.predict(interval[0].transform(x)) for tree,interval in zip(model.estimators_,model.intervals_)],axis=0)
        np.testing.assert_allclose(model.predict(x),expected)

    def test_cnn_seed_target_scaler_and_linear_output(self):
        x=np.random.default_rng(3).normal(size=(8,24,20)).astype(np.float32)
        y=np.array([1.,3.,5.,7.,9.,11.,13.,15.])
        torch.manual_seed(42);initial=study.EnergyCNN().state_dict()
        a,scaler,h1=study.fit_cnn(x,y,epochs=2);b,_,h2=study.fit_cnn(x,y,epochs=2)
        np.testing.assert_allclose(scaler,[y.mean(),y.std()])
        np.testing.assert_allclose(((y-scaler[0])/scaler[1])*scaler[1]+scaler[0],y)
        with torch.inference_mode():pa=a(torch.from_numpy(x));pb=b(torch.from_numpy(x))
        np.testing.assert_array_equal(pa,pb);np.testing.assert_array_equal(h1,h2)
        self.assertEqual(tuple(pa.shape),(8,));self.assertEqual(sum(p.numel() for p in a.parameters()),5553)
        self.assertIsInstance(a.layers[-1],torch.nn.Linear)
        self.assertTrue(any(not torch.equal(a.state_dict()[key],initial[key]) for key in initial))

    def test_manual_metrics_in_original_units(self):
        result=study.evaluate_regressors(np.array([1.,4.,7.]),{'manual':np.array([0.,2.,8.])})
        np.testing.assert_allclose(result[['rmse','mae']].to_numpy(),[[np.sqrt(2),4/3]])

    def test_invalid_inputs(self):
        for y in [[1,np.nan],[[1],[2]],[1]]:
            with self.assertRaises(ValueError):study.validate_targets(y,2)
        with self.assertRaises(ValueError):study.fit_regressors(np.full((2,24,20),np.nan),[1,2])
        with self.assertRaises(ValueError):study.evaluate_regressors(np.array([1,2]),{'bad':np.array([1])})


if __name__=='__main__':unittest.main()

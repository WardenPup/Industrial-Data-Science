"""Analytic preprocessing/metric checks and actual multivariate model tests."""
import tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
import torch
from aeon.distances import dtw_distance
from aeon.classification.distance_based import KNeighborsTimeSeriesClassifier
from sessions.ch12 import classification as study

class UWaveTests(unittest.TestCase):
    def test_scaler_is_train_only_and_nonmutating(self):
        train=np.arange(24,dtype=float).reshape(2,3,4);before=train.copy()
        scaler=study.fit_scaler(train)
        np.testing.assert_allclose(scaler[0].ravel(),[7.5,11.5,15.5])
        np.testing.assert_allclose(scaler[1].ravel(),np.sqrt(37.25))
        scaled=study.transform(train,scaler)
        np.testing.assert_allclose(scaled.mean(axis=(0,2)),0,atol=1e-7)
        np.testing.assert_allclose(scaled.std(axis=(0,2)),1,atol=1e-7)
        shifted=study.transform(train+1000,scaler)
        self.assertGreater(float(shifted.mean()),100)
        np.testing.assert_array_equal(train,before)
        np.testing.assert_allclose(scaler[0].ravel(),[7.5,11.5,15.5])
        constant=np.ones((2,3,4));np.testing.assert_array_equal(study.transform(constant,study.fit_scaler(constant)),np.zeros_like(constant))

    def test_invalid_input_and_raw_checksum(self):
        for x in [np.zeros((2,3)),np.empty((0,3,4)),np.full((2,3,4),np.nan),np.full((2,3,4),np.inf)]:
            with self.assertRaises(ValueError):study.fit_scaler(x)
        with self.assertRaises(ValueError):study.transform(np.ones((2,2,4)),study.fit_scaler(np.ones((2,3,4))))
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);p=root/'data/raw/UWaveGestureLibrary';p.mkdir(parents=True)
            (p/'UWaveGestureLibrary_TRAIN.ts').write_bytes(b'changed')
            with patch.object(study,'ROOT',root),self.assertRaises(ValueError):study.load_uwave('TRAIN')

    def test_multivariate_dtw_and_known_neighbours(self):
        x=np.array([[0.,1.],[1.,0.]])
        y=np.array([[0.,2.],[1.,0.]])
        self.assertEqual(dtw_distance(x,y,window=0),1.)
        self.assertEqual(dtw_distance(x,x),0.)
        a=np.tile(np.array([0.,0.,1.,1.]),(3,1));b=a[:,::-1].copy()
        train=np.stack([a,a,a,b,b,b]);labels=np.array(['a']*3+['b']*3)
        model=KNeighborsTimeSeriesClassifier(**study.KNN_PARAMS).fit(train,labels)
        np.testing.assert_array_equal(model.predict(np.stack([a,b])),['a','b'])

    def test_cnn_shape_loss_learning_and_seed(self):
        torch.set_num_threads(1);torch.manual_seed(42)
        network=study.GestureCNN()
        self.assertEqual(sum(p.numel() for p in network.parameters()),5000)
        self.assertEqual(tuple(network(torch.zeros((2,3,315))).shape),(2,8))
        self.assertAlmostEqual(float(torch.nn.CrossEntropyLoss()(torch.zeros((2,8)),torch.tensor([0,7]))),np.log(8),places=6)
        x=np.random.default_rng(42).normal(size=(6,3,32)).astype(np.float32);y=np.array([0,0,0,1,1,1])
        torch.manual_seed(42);initial=study.GestureCNN(3,2)
        first,history=study.fit_cnn(x,y,2,epochs=2)
        second,_=study.fit_cnn(x,y,2,epochs=2)
        self.assertTrue(any(not torch.equal(a,b) for a,b in zip(initial.parameters(),first.parameters())))
        for a,b in zip(first.parameters(),second.parameters()):self.assertTrue(torch.equal(a,b))
        self.assertTrue(np.isfinite(history.train_cross_entropy).all())
        self.assertFalse(first.training)

    def test_fit_predict_boundary_and_frozen_scaler(self):
        x=np.random.default_rng(9).normal(size=(6,3,32)).astype(np.float32);labels=np.array(['a']*3+['b']*3)
        real_fit=study.fit_cnn
        with patch.object(study,'fit_cnn',side_effect=lambda a,b,c:real_fit(a,b,c,epochs=2)),patch.object(study,'fit_scaler',wraps=study.fit_scaler) as scaling:
            fitted=study.fit_classifiers(x,labels)
            self.assertEqual(scaling.call_count,1)
            np.testing.assert_array_equal(scaling.call_args.args[0],x)
        frozen=[v.copy() for v in fitted['scaler']]
        predictions,_,logits=study.predict_classifiers(fitted,x[:2]+100)
        self.assertEqual(logits.shape,(2,2))
        self.assertTrue(all(len(p)==2 for p in predictions.values()))
        for a,b in zip(fitted['scaler'],frozen):np.testing.assert_array_equal(a,b)

    def test_metrics_on_known_confusion(self):
        metrics,matrices,report=study.evaluate(np.array(['a','a','b','b']),{'toy':np.array(['a','b','b','b'])},np.array(['a','b']))
        np.testing.assert_array_equal(matrices['toy'],[[1,1],[0,2]])
        self.assertAlmostEqual(metrics.iloc[0].accuracy,.75)
        self.assertAlmostEqual(metrics.iloc[0].balanced_accuracy,.75)
        self.assertAlmostEqual(metrics.iloc[0].macro_f1,11/15)
        with self.assertRaises(ValueError):study.evaluate(np.array(['c']),{'toy':np.array(['a'])},np.array(['a','b']))

    def test_complete_original_splits(self):
        for split,n in [('TRAIN',120),('TEST',320)]:
            x,y=study.load_uwave(split)
            self.assertEqual(x.shape,(n,3,315));self.assertEqual(len(y),n)
            self.assertTrue(np.isfinite(x).all());self.assertEqual(len(set(y)),8)

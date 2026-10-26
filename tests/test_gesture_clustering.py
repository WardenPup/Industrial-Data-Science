"""Analytic preprocessing/MSM tests and genuine estimator smoke checks."""
import unittest
import numpy as np
from aeon.distances import msm_distance
from aeon.clustering import KASBA,TimeSeriesKMeans
from sklearn.metrics import adjusted_rand_score
from sessions.ch12.clustering import resample_normalize,msm_matrix,load_gestures

class GestureTests(unittest.TestCase):
    def test_linear_resampling_and_constant(self):
        raw=np.array([[2.,5.,8.]])
        before=raw.copy()
        expected=np.array([2.,3.5,5.,6.5,8.]);expected=(expected-expected.mean())/expected.std()
        np.testing.assert_allclose(resample_normalize([raw],5)[0,0],expected)
        np.testing.assert_array_equal(raw,before)
        np.testing.assert_array_equal(resample_normalize([np.ones((1,3))],5),np.zeros((1,1,5)))
        mixed=resample_normalize([raw,np.array([[1.,2.]])],7)
        self.assertEqual(mixed.shape,(2,1,7))
        np.testing.assert_allclose(mixed.mean(axis=2),0,atol=1e-14)
        np.testing.assert_allclose(mixed.std(axis=2),1,atol=1e-14)

    def test_invalid_preprocessing(self):
        for data in [[],[np.array([[1.,np.nan]])],[np.ones((2,3))],[np.ones((1,1))]]:
            with self.assertRaises(ValueError):resample_normalize(data)
        with self.assertRaises(ValueError):resample_normalize([np.ones((1,2))],True)

    def test_msm_hand_calculation_and_reference(self):
        self.assertEqual(msm_matrix([1.,1.,3.],[1.,3.])[-1,-1],1.)
        self.assertEqual(msm_matrix([1.,2.],[1.,3.])[-1,-1],1.)
        self.assertEqual(msm_matrix([2.],[4.])[-1,-1],2.)
        rng=np.random.default_rng(42)
        for n,m in [(2,5),(4,3),(6,6)]:
            x,y=rng.normal(size=n),rng.normal(size=m)
            np.testing.assert_allclose(msm_matrix(x,y)[-1,-1],msm_distance(x,y),atol=1e-12)
            np.testing.assert_allclose(msm_matrix(x,y)[-1,-1],msm_matrix(y,x)[-1,-1],atol=1e-12)
            self.assertEqual(msm_matrix(x,x)[-1,-1],0.)
        with self.assertRaises(ValueError):msm_matrix([], [1.])
        with self.assertRaises(ValueError):msm_matrix([1.], [2.],c=0)

    def test_original_splits_and_format(self):
        for split,count in [("TRAIN",132),("TEST",172)]:
            raw,labels=load_gestures(split)
            self.assertEqual(len(raw),count);self.assertEqual(len(labels),count)
            self.assertGreater(len(set(x.shape[-1] for x in raw)),1)
            self.assertEqual(resample_normalize(raw).shape,(count,1,128))
            self.assertEqual(len(set(labels)),6)

    def test_estimators_seed_and_prediction(self):
        x=np.array([[[0.,0.,1.,1.]],[[0.,.1,.9,1.]],[[1.,1.,0.,0.]],[[1.,.9,.1,0.]]])
        factories=[lambda:TimeSeriesKMeans(n_clusters=2,distance="euclidean",averaging_method="mean",n_init=1,max_iter=5,random_state=42),
                   lambda:KASBA(n_clusters=2,max_iter=5,random_state=42)]
        for factory in factories:
            a,b=factory(),factory()
            self.assertFalse(a.get_tag("capability:unequal_length"))
            a.fit(x);b.fit(x)
            self.assertEqual(adjusted_rand_score(a.labels_,b.labels_),1.)
            self.assertEqual(a.predict(x[:1]).shape,(1,))
            self.assertTrue(np.isfinite(a.cluster_centers_).all())

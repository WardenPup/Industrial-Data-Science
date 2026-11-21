"""Three focused checks for the official 16.1 frame."""
import unittest
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from sklearn.model_selection import train_test_split
from sessions.ch16.multimodal import load_multimodal_data,DATA_PATH,prepare_data,TimeSeriesCNN,train_model,predict_proba
class VibrationCNNTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1)
        cls.arrays=load_multimodal_data(str(DATA_PATH));cls.p=prepare_data(*cls.arrays)
    def test_source_shapes_and_label_definition(self):
        ts,img,y,levels=self.arrays
        self.assertEqual([a.shape for a in self.arrays],[(500,80),(500,32,32),(500,),(500,2)])
        self.assertEqual(np.bincount(y).tolist(),[240,185,75])
        table=np.array([[0,0,1],[1,1,2],[2,2,2]])
        np.testing.assert_array_equal(y,table[levels[:,0],levels[:,1]])
    def test_alignment_and_train_only_scalars(self):
        p=self.p;ts,img,y,levels=self.arrays
        expected=train_test_split(ts,img,y,levels,test_size=.2,random_state=42,stratify=y)
        for key,value in zip(["ts_train","ts_test","img_train","img_test","y_train","y_test","levels_train","levels_test"],expected):np.testing.assert_array_equal(p[key],value)
        changed_ts=ts.copy();changed_img=img.copy()
        changed_ts[p["test_indices"]]+=1000;changed_img[p["test_indices"]]-=1000
        q=prepare_data(changed_ts,changed_img,y,levels)
        for name,shape in [("ts",(1,80)),("img",(1,32,32))]:
            for suffix in ["mean","std"]:self.assertEqual(p[name+"_"+suffix],q[name+"_"+suffix])
            self.assertAlmostEqual(float(p[name+"_train_norm"].mean()),0,places=10)
            self.assertAlmostEqual(float(p[name+"_train_norm"].std()),1,places=10)
            self.assertEqual(tuple(p[name+"_train_tensor"].shape),(400,)+shape)
            self.assertEqual(tuple(p[name+"_test_tensor"].shape),(100,)+shape)
            self.assertEqual(p[name+"_train_tensor"].dtype,torch.float32)
    def test_exact_architecture_and_training_modes(self):
        torch.manual_seed(42);model=TimeSeriesCNN();layers=list(model.features)
        self.assertEqual([type(x) for x in layers],[nn.Conv1d,nn.ReLU,nn.MaxPool1d,nn.Conv1d,nn.ReLU,nn.MaxPool1d,nn.AvgPool1d,nn.Flatten,nn.Linear,nn.ReLU,nn.Dropout])
        self.assertEqual([(layers[i].in_channels,layers[i].out_channels,layers[i].kernel_size,layers[i].padding) for i in [0,3]],[(1,16,(5,),"same"),(16,32,(5,),"same")])
        self.assertEqual((layers[2].kernel_size,layers[5].kernel_size,layers[6].kernel_size),(2,2,(20,)))
        self.assertEqual((layers[8].in_features,layers[8].out_features,layers[-1].p),(32,32,.3))
        self.assertEqual((model.classifier.in_features,model.classifier.out_features),(32,3))
        x=self.p["ts_train_tensor"][:4];self.assertEqual(tuple(model.features(x).shape),(4,32));self.assertEqual(tuple(model(x).shape),(4,3))
        before=[p.detach().clone() for p in model.parameters()]
        loader=DataLoader(TensorDataset(x,self.p["y_train_tensor"][:4]),batch_size=4)
        model=train_model(model,loader,epochs=1)
        self.assertFalse(model.training);self.assertFalse(model.features[-1].training)
        self.assertTrue(any(not torch.equal(a,b) for a,b in zip(before,model.parameters())))
        a=predict_proba(model,x);b=predict_proba(model,x)
        np.testing.assert_array_equal(a,b);np.testing.assert_allclose(a.sum(axis=1),1,atol=1e-6)
if __name__=="__main__":unittest.main()

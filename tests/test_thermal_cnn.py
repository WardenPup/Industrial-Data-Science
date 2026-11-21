"""Two focused checks for the prescribed thermal CNN and shared training."""
import unittest
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from sessions.ch16.multimodal import load_multimodal_data,DATA_PATH,prepare_data,train_model,predict_proba
from sessions.ch16.thermal import ThermalCNN
class ThermalCNNTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1);cls.p=prepare_data(*load_multimodal_data(str(DATA_PATH)))
    def test_exact_layers_and_shapes(self):
        model=ThermalCNN();layers=list(model.features)
        self.assertEqual([type(x) for x in layers],[nn.Conv2d,nn.ReLU,nn.MaxPool2d,nn.Conv2d,nn.ReLU,nn.MaxPool2d,nn.Flatten,nn.Linear,nn.ReLU,nn.Dropout])
        self.assertEqual([(layers[i].in_channels,layers[i].out_channels,layers[i].kernel_size,layers[i].padding) for i in [0,3]],[(1,16,(3,3),"same"),(16,32,(3,3),"same")])
        self.assertEqual((layers[2].kernel_size,layers[5].kernel_size),(2,2))
        self.assertEqual((layers[7].in_features,layers[7].out_features,layers[-1].p),(2048,64,.3))
        self.assertEqual((model.classifier.in_features,model.classifier.out_features),(64,3))
        x=self.p["img_train_tensor"][:4]
        self.assertEqual(tuple(model.features(x).shape),(4,64));self.assertEqual(tuple(model(x).shape),(4,3))
    def test_seeded_training_and_prediction(self):
        x=self.p["img_train_tensor"][:16];y=self.p["y_train_tensor"][:16];results=[]
        for _ in range(2):
            torch.manual_seed(42)
            model=ThermalCNN();before=[p.detach().clone() for p in model.parameters()]
            model=train_model(model,DataLoader(TensorDataset(x,y),batch_size=16,shuffle=True),epochs=1)
            self.assertFalse(model.training);self.assertFalse(model.features[-1].training)
            self.assertTrue(any(not torch.equal(a,b) for a,b in zip(before,model.parameters())))
            result=predict_proba(model,self.p["img_test_tensor"])
            np.testing.assert_allclose(result.sum(axis=1),1,atol=1e-6)
            np.testing.assert_array_equal(result,predict_proba(model,self.p["img_test_tensor"]))
            results.append(result)
        np.testing.assert_array_equal(*results)
if __name__=="__main__":unittest.main()

"""Two focused checks: fresh architecture and joint gradient-based training."""
import unittest
import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader,TensorDataset
from sessions.ch16.intermediate import MultimodalNet
from sessions.ch16.multimodal import TimeSeriesCNN,load_multimodal_data,DATA_PATH,prepare_data,train_model,predict_proba
from sessions.ch16.thermal import ThermalCNN
class IntermediateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        torch.set_num_threads(1);cls.p=prepare_data(*load_multimodal_data(str(DATA_PATH)))
    def test_fresh_branches_exact_head_and_shapes(self):
        torch.manual_seed(42);model=MultimodalNet()
        torch.manual_seed(42);img_reference=ThermalCNN();ts_reference=TimeSeriesCNN()
        for branch,reference in [(model.img_features,img_reference.features),(model.ts_features,ts_reference.features)]:
            for a,b in zip(branch.parameters(),reference.parameters()):
                self.assertTrue(torch.equal(a,b));self.assertNotEqual(a.data_ptr(),b.data_ptr())
        self.assertEqual([type(x) for x in model.classifier],[nn.Linear,nn.ReLU,nn.Dropout,nn.Linear])
        self.assertEqual((model.classifier[0].in_features,model.classifier[0].out_features,model.classifier[2].p,model.classifier[3].in_features,model.classifier[3].out_features),(96,32,.3,32,3))
        img=self.p["img_train_tensor"][:4];ts=self.p["ts_train_tensor"][:4]
        self.assertEqual(tuple(model.img_features(img).shape),(4,64))
        self.assertEqual(tuple(model.ts_features(ts).shape),(4,32))
        self.assertEqual(tuple(torch.cat([model.img_features(img),model.ts_features(ts)],dim=1).shape),(4,96))
        self.assertEqual(tuple(model(img,ts).shape),(4,3))
        self.assertEqual(sum(p.numel() for p in model.parameters()),142883)
    def test_end_to_end_update_in_both_branches(self):
        torch.manual_seed(42);model=MultimodalNet()
        before=[next(block.parameters()).detach().clone() for block in [model.img_features,model.ts_features,model.classifier]]
        img=self.p["img_train_tensor"][:16];ts=self.p["ts_train_tensor"][:16];y=self.p["y_train_tensor"][:16]
        loader=DataLoader(TensorDataset(img,ts,y),batch_size=16,shuffle=True)
        model=train_model(model,loader,epochs=1)
        for old,block in zip(before,[model.img_features,model.ts_features,model.classifier]):
            self.assertFalse(torch.equal(old,next(block.parameters())))
            self.assertTrue(any(p.grad is not None and torch.count_nonzero(p.grad)>0 for p in block.parameters()))
        self.assertFalse(model.training)
        result=predict_proba(model,img,ts)
        np.testing.assert_array_equal(result,predict_proba(model,img,ts))
        np.testing.assert_allclose(result.sum(axis=1),1,atol=1e-6)
if __name__=="__main__":unittest.main()

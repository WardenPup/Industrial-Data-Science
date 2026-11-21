"""Two focused checks for the exact course fusion operations."""
import unittest
import numpy as np
import torch
from sessions.ch16.fusion import as_image_channel,mean_probabilities
from sessions.ch16.thermal import ThermalCNN
class FusionTests(unittest.TestCase):
    def test_padding_channel_order_and_network_input(self):
        torch.set_num_threads(1)
        ts=np.arange(160,dtype=float).reshape(2,80)
        channel=as_image_channel(ts)
        self.assertEqual(tuple(channel.shape),(2,1,32,32))
        flat=channel.numpy().reshape(2,1024)
        np.testing.assert_array_equal(flat[:,:80],ts)
        np.testing.assert_array_equal(flat[:,80:],np.zeros((2,944)))
        images=torch.ones(2,1,32,32)*-7
        early=torch.cat([images,channel],dim=1)
        self.assertTrue(torch.equal(early[:,0:1],images))
        self.assertTrue(torch.equal(early[:,1:2],channel))
        model=ThermalCNN(in_channels=2)
        self.assertEqual(model.features[0].in_channels,2)
        self.assertEqual(tuple(model(early).shape),(2,3))
        self.assertEqual(sum(p.numel() for p in model.parameters()),136275)
    def test_unweighted_probability_mean_and_argmax(self):
        a=np.array([[.8,.1,.1],[.1,.2,.7]],dtype=np.float32)
        b=np.array([[.2,.7,.1],[.6,.3,.1]],dtype=np.float32)
        result=mean_probabilities(a,b)
        np.testing.assert_array_equal(result,(a+b)/2)
        np.testing.assert_array_equal(result.argmax(axis=1),[0,2])
        np.testing.assert_allclose(result.sum(axis=1),1)
        with self.assertRaises(ValueError):mean_probabilities(a,b[:1])
        with self.assertRaises(ValueError):mean_probabilities(a,np.zeros_like(b))
if __name__=="__main__":unittest.main()

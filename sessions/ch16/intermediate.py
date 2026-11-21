"""Exact official intermediate-fusion architecture, with fresh feature branches."""
import torch
from torch import nn
from sessions.ch16.multimodal import TimeSeriesCNN
from sessions.ch16.thermal import ThermalCNN

class MultimodalNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.img_features=ThermalCNN().features
        self.ts_features=TimeSeriesCNN().features
        self.classifier=nn.Sequential(nn.Linear(96,32),nn.ReLU(),nn.Dropout(.3),nn.Linear(32,3))
    def forward(self,img: torch.Tensor,ts: torch.Tensor)->torch.Tensor:
        features=torch.cat([self.img_features(img),self.ts_features(ts)],dim=1)
        return self.classifier(features)

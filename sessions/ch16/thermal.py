"""Exact Exercise 16.2 image architecture; shared training stays unchanged."""
from torch import nn

class ThermalCNN(nn.Module):
    """Table 16.3: 64 image features and three health-status logits."""
    def __init__(self,in_channels: int=1):
        super().__init__()
        self.features=nn.Sequential(
            nn.Conv2d(in_channels,16,kernel_size=3,padding="same"),nn.ReLU(),nn.MaxPool2d(2),
            nn.Conv2d(16,32,kernel_size=3,padding="same"),nn.ReLU(),nn.MaxPool2d(2),
            nn.Flatten(),nn.Linear(2048,64),nn.ReLU(),nn.Dropout(.3))
        self.classifier=nn.Linear(64,3)
    def forward(self,x):return self.classifier(self.features(x))

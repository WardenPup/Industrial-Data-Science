"""Only the two fusion operations prescribed in Exercise 16.3."""
import numpy as np
import torch

def as_image_channel(ts: np.ndarray)->torch.Tensor:
    """Official frame: pad 80 standardized samples to a 32x32 channel."""
    if ts.ndim!=2 or ts.shape[1]!=80:raise ValueError("Expected (samples,80)")
    padded=np.pad(ts,((0,0),(0,32*32-ts.shape[1])))
    return torch.FloatTensor(padded).reshape(-1,1,32,32)

def mean_probabilities(first: np.ndarray,second: np.ndarray)->np.ndarray:
    """Unweighted row-wise mean; rows and class order must already match."""
    if first.shape!=second.shape or first.ndim!=2 or first.shape[1]!=3:
        raise ValueError("Expected two matching (samples,3) probability arrays")
    for values in [first,second]:
        if not np.isfinite(values).all() or (values<0).any() or not np.allclose(values.sum(axis=1),1,atol=1e-6):
            raise ValueError("Expected finite normalized class probabilities")
    return (first+second)/2

"""Course-aligned residual outlier candidates on complete original observations."""
import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL
from sessions.ch11.stl_imputation import STL_CONFIG, FIT_CONFIG


def sigma_flags(residual, multiplier=3.0):
    """Strict two-sided sample-standard-deviation rule; no automatic removal."""
    if len(residual) < 2 or not np.isfinite(residual).all():
        raise ValueError("Need at least two finite residuals")
    if not np.isfinite(multiplier) or multiplier <= 0:
        raise ValueError("multiplier must be finite and positive")
    mean = float(residual.mean())
    std = float(residual.std(ddof=1))
    lower, upper = mean - multiplier * std, mean + multiplier * std
    return (residual < lower) | (residual > upper), lower, upper


def detect_outliers(source):
    """Reestimate STL on raw pieces, without smoothing or filling gaps."""
    if not isinstance(source.index, pd.DatetimeIndex) or not source.index.equals(
        pd.date_range(source.index[0], periods=len(source), freq="7D", name=source.index.name)
    ) or len(source) < 104 or not np.isfinite(source).all():
        raise ValueError("Need at least two complete ordered weekly cycles")
    result = STL(source, **STL_CONFIG).fit(**FIT_CONFIG)
    flags, lower, upper = sigma_flags(result.resid)
    table = pd.DataFrame({"pieces": source, "trend": result.trend,
                          "seasonal": result.seasonal, "residual": result.resid,
                          "outlier_candidate": flags})
    return table, lower, upper

"""Exercise 11.3: two-stage additive seasonal imputation, not forecasting."""

import numpy as np
import pandas as pd
from statsmodels.tsa.seasonal import STL

from sessions.ch11.imputation import impute_series

STL_CONFIG = {"period": 52, "seasonal": 13, "trend": 101, "low_pass": 53, "robust": True}
FIT_CONFIG = {"inner_iter": 2, "outer_iter": 15}


def seasonal_imputation(source, seasonal):
    """Subtract season from gapped source, interpolate, add it back.

    Observed source values are restored exactly after floating-point arithmetic.
    Returns gapped deseasonalized, completed deseasonalized, final series.
    """
    if not source.index.equals(seasonal.index):
        raise ValueError("Source and seasonal indices must match")
    if not np.isfinite(seasonal).all():
        raise ValueError("Seasonal component must be finite")
    deseasonalized = source - seasonal
    completed = impute_series(deseasonalized, "linear")
    final = (completed + seasonal).where(source.isna(), source)
    return deseasonalized, completed, final


def stl_impute(source, config=None):
    """Estimate season from preliminary fill, then use original gaps again."""
    settings = dict(STL_CONFIG if config is None else config)
    if len(source) < 2 * settings["period"]:
        raise ValueError("At least two assumed seasonal cycles are required")
    initial = impute_series(source, "linear")
    if not np.isfinite(initial).all():
        raise ValueError("STL requires a finite preliminary series; boundary gaps remain")
    decomposition = STL(initial, **settings).fit(**FIT_CONFIG)
    seasonal = pd.Series(decomposition.seasonal, index=source.index)
    deseasonalized, completed, final = seasonal_imputation(source, seasonal)
    stages = pd.DataFrame({"smoothed_gaps": source, "preliminary_linear": initial,
                           "trend": decomposition.trend, "seasonal": seasonal,
                           "residual": decomposition.resid,
                           "deseasonalized_gaps": deseasonalized,
                           "deseasonalized_linear": completed, "final_imputed": final})
    return stages, decomposition


def summarize_stages(stages):
    source = stages.smoothed_gaps
    observed = source.notna()
    changed = stages.loc[~observed, "final_imputed"] - stages.loc[~observed, "preliminary_linear"]
    return {
        "rows": len(source), "observed": int(observed.sum()), "missing_input": int((~observed).sum()),
        "missing_preliminary": int(stages.preliminary_linear.isna().sum()),
        "missing_deseasonalized": int(stages.deseasonalized_gaps.isna().sum()),
        "same_deseasonalized_mask": stages.deseasonalized_gaps.isna().equals(source.isna()),
        "missing_final": int(stages.final_imputed.isna().sum()),
        "observed_exactly_preserved": np.array_equal(stages.loc[observed, "final_imputed"], source[observed]),
        "additive_reconstruction_max_abs": float((stages.preliminary_linear - stages.trend - stages.seasonal - stages.residual).abs().max()),
        "difference_from_linear_mean_abs_at_gaps": float(changed.abs().mean()),
        "difference_from_linear_max_abs_at_gaps": float(changed.abs().max()),
        "negative_imputed": int((stages.loc[~observed, "final_imputed"] < 0).sum()),
    }

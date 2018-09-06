"""
Common error stat calculations.

Jamie Taylor
2018-09-04
"""

import numpy as np

def r_squared(predictions, actuals):
    mean_actual = np.mean(actuals)
    ss_tot = np.sum(np.power(actuals - mean_actual, 2))
    ss_res = np.sum(np.power(actuals - predictions, 2))
    return 1 - ss_res / ss_tot

def pearson_coefficient(predictions, actuals):
    return np.corrcoef(predictions, actuals)[0, 1]

def wmape(predictions, actuals, norms):
    mapes = np.abs((predictions - actuals) / norms) * 100.
    return np.sum(actuals * mapes) / np.sum(actuals)
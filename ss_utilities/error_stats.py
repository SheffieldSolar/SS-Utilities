"""
Common error stat calculations.

Jamie Taylor
2018-09-04
"""

import numpy as np

def r_squared(predictions, actuals):
    r"""
    Calculate the coefficient of determination (a.k.a R-Squared) [1]_.
    
    Parameters
    ----------
    `predictions` : numpy array of floats
        Predictions being tested.
    `actuals`: numpy array of floats
        Actual values corresponding to `predictions`. Must be same size as `predictions`.

    Returns
    -------
    float
        Coefficient of determination.

    Notes
    -----
    .. math::
        \begin{align*}
        y=Actuals,\quad f&=Predictions,\quad \bar{y}=\frac{1}{n}\sum_{i=1}^n{y_i}\\
        SS_{tot}&=\sum_i{(y_i-\bar{y})^2}\\
        SS_{res}&=\sum_i{(y_i-f_i)^2}\\
        R^2&=1-\frac{SS_{res}}{SS_{tot}}
        \end{align*}

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Coefficient_of_determination
    """
    mean_actual = np.mean(actuals)
    ss_tot = np.sum(np.power(actuals - mean_actual, 2))
    ss_res = np.sum(np.power(actuals - predictions, 2))
    return 1 - ss_res / ss_tot

def pearson_coefficient(predictions, actuals):
    r"""
    Calculate the Pearson correlation coefficient [1]_.
    
    Parameters
    ----------
    `predictions` : numpy array of floats
        Predictions being tested.
    `actuals`: numpy array of floats
        Actual values corresponding to `predictions`. Must be same size as `predictions`.

    Returns
    -------
    float
        Pearson correlation coefficient.

    Notes
    -----
    .. math::
        \begin{align*}
        \rho_{x,y}=\frac{\mathrm{cov}(x, y)}{\sigma_x\sigma_y}
        \end{align*}

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    """
    return np.corrcoef(predictions, actuals)[0, 1]

def wmape(predictions, actuals, norms=None, weights=None):
    r"""
    Calculate the weighted Mean Absolute Percent Error (MAPE).
    
    Parameters
    ----------
    `predictions` : numpy array of floats
        Predictions being tested.
    `actuals` : numpy array of floats
        Actual values corresponding to `predictions`. Must be same size as `predictions`.
    `norms` : numpy array of floats
        Normalisation values. Must be same size as `predictions`. Default is to use `actuals`.
    `weights` : numpy array of floats
        Weighting values. Must be same size as `predictions`. Default is to use `actuals`.

    Returns
    -------
    float
        wMAPE.

    Notes
    -----
    .. math::
        \begin{gathered}
        y=Actuals,\quad f=Predictions,\quad n=Normalisations,\quad w=Weights\\
        \mathit{wMAPE}=
        \frac{\sum_i{w_i\times\mathrm{abs}\left(\frac{f_i-y_i}{n_i}\right)\times100\%}}{\sum_i{w_i}}
        \end{gathered}
    """
    norms = actuals if norms is None else norms
    weights = actuals if weights is None else weights
    mapes = np.abs((predictions - actuals) / norms) * 100.
    return np.sum(weights * mapes) / np.sum(weights)

def rmse(predictions, actuals):
    r"""
    Calculate the Root Mean Square Error (RMSE).
    
    Parameters
    ----------
    `predictions` : numpy array of floats
        Predictions being tested.
    `actuals` : numpy array of floats
        Actual values corresponding to `predictions`. Must be same size as `predictions`.

    Returns
    -------
    float
        RMSE.

    Notes
    -----
    .. math::
        \begin{gathered}
        y=Actuals,\quad f=Predictions\\
        \mathit{RMSE}=\sqrt{\frac{\sum_i^n{{\left (f_i-y_i \right )}^2}}{n}}
        \end{gathered}
    """
    return np.sqrt(np.mean(np.power(predictions - actuals, 2)))

def mbe(predictions, actuals):
    r"""
    Calculate the Mean Bias Error (MBE).
    
    Parameters
    ----------
    `predictions` : numpy array of floats
        Predictions being tested.
    `actuals` : numpy array of floats
        Actual values corresponding to `predictions`. Must be same size as `predictions`.

    Returns
    -------
    float
        MBE.

    Notes
    -----
    .. math::
        \begin{gathered}
        y=Actuals,\quad f=Predictions\\
        \mathit{MBE}=\frac{\sum_i^n{\left (f_i-y_i \right )}}{n}
        \end{gathered}
    """
    return np.mean(predictions - actuals)

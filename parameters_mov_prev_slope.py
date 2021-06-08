import numpy as np
import pandas as pd

def parameters_mov_prev_slope(counts=None, dataset=None, time_attribute=None, outcome_attribute=None):

    params = counts.join(dataset.groupby(time_attribute)[outcome_attribute].mean())
    params = params.rename(columns={outcome_attribute[0]: 'prev'})

    return params

def parameters_mov_prev_slope_rest(params=None):

    temp_params = params.copy()

    theta = temp_params['prev'].values
    var = (theta * (1 - theta)) / ( temp_params['n'].values - 1 ) # normalized with n-1 see Bethlehem p.71
    ses = np.sqrt(var)
    temp_params['prev_se'] = ses

    temp_params = replace_zero_se(params=temp_params)

    prevs = temp_params['prev'].values
    n = temp_params['n'].values
    window = 2
    sums = n[(window-1):] + n[:-(window-1)]
    w = n / np.append(sums,[np.nan])
    p1 = w[:-(window-1)] * prevs[:-(window-1)]
    p2 = (1-w)[:-(window-1)] * prevs[(window-1):]
    means = p1 + p2

    '''    
    n = temp_params['n'].values
    totals = prevs*n
    means = (totals[1:] + totals[:-1]) / (n[1:] + n[:-1])
    '''
    
    ns = n[(window-1):] + n[:-(window-1)]    
    nans = np.empty(window-1)
    nans[:] = np.nan
    temp_params['mov_prev'] = np.append(means, list(nans))
    temp_params['mov_prev_n'] = np.append(ns, list(nans))

    temp_ses = temp_params['prev_se'].values
    p1 = ((w[:-(window-1)]**2)) * (temp_ses[:-(window-1)]**2)
    p2 = (((1-w)[:-(window-1)]**2)) * (temp_ses[(window-1):]**2)
    vars = p1 + p2
    #vars = (thetas * (1 - thetas)) / temp_params['mov_prev_n'].values
    ses = np.sqrt(vars)

    temp_params['mov_prev_se'] = np.append(ses, list(nans))
    
    # slopes

    thetas = temp_params['mov_prev'].values
    slopes = thetas[1:] - thetas[:-1]
    temp_params['mov_prev_slope'] = np.append(slopes, [np.nan])

    ses = temp_params['mov_prev_se'].values
    var = ses**2
    sum_var = var[1:] + var[:-1]
    slopes_ses = np.sqrt(sum_var)
    temp_params['mov_prev_slope_se'] = np.append(slopes_ses, [np.nan])

    params = temp_params.copy()

    return params

def replace_zero_se(params=None):

    idx_replace = params['prev_se'] == 0.0
    if np.sum(idx_replace) > 0:
        params.loc[idx_replace, 'prev_se'] = np.min(params.loc[~idx_replace, 'prev_se'])

    return params

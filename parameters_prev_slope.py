import numpy as np
import pandas as pd

def parameters_prev_slope(counts=None, dataset=None, time_attribute=None, outcome_attribute=None):

    params = counts.join(dataset.groupby(time_attribute)[outcome_attribute].mean())
    params = params.rename(columns={outcome_attribute[0]: 'prev'})

    return params

def parameters_prev_slope_rest(params=None):

    temp_params = params.copy()

    theta = temp_params['prev'].values
    var = (theta * (1 - theta)) / ( temp_params['n'].values - 1 ) # normalized with n-1 see Bethlehem p.71
    ses = np.sqrt(var)
    temp_params['prev_se'] = ses

    temp_params = replace_zero_se(params=temp_params)

    thetas = temp_params['prev'].values
    slopes = thetas[1:] - thetas[:-1]
    temp_params['prev_slope'] = np.append(slopes, [np.nan])
    
    ses = temp_params['prev_se'].values
    var = ses**2
    sum_var = var[1:] + var[:-1]
    slopes_ses = np.sqrt(sum_var)
    temp_params['prev_slope_se'] = np.append(slopes_ses, [np.nan])

    params = temp_params.copy()

    return params

def replace_zero_se(params=None):

    idx_replace = params['prev_se'] == 0.0
    if np.sum(idx_replace) > 0:
        params.loc[idx_replace, 'prev_se'] = np.min(params.loc[~idx_replace, 'prev_se'])

    return params

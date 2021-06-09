import numpy as np
import pandas as pd

def parameters_prev(counts=None, dataset=None, time_attribute=None, outcome_attribute=None):

    params = counts.join(dataset.groupby(time_attribute)[outcome_attribute].mean())
    params = params.rename(columns={outcome_attribute[0]: 'prev'})

    theta = params['prev'].values
    var = (theta * (1 - theta)) / ( params['n'].values - 1 ) # normalized with n - 1 see Bethlehem p.71
    ses = np.sqrt(var)
    params['prev_se'] = ses

    params = replace_zero_se(params=params)

    return params

def parameters_prev_rest(params=None):

    return params

def replace_zero_se(params=None):

    idx_replace = params['prev_se'] == 0.0
    if np.sum(idx_replace) > 0:
        params.loc[idx_replace, 'prev_se'] = np.min(params.loc[~idx_replace, 'prev_se'])
        #print('yes')

    return params


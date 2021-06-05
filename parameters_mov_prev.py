import numpy as np
import pandas as pd

def parameters_mov_prev(counts=None, dataset=None, time_attribute=None, outcome_attribute=None):

    params = counts.join(dataset.groupby(time_attribute)[outcome_attribute].mean())
    params = params.rename(columns={outcome_attribute[0]: 'prev'})  
    
    return params

def parameters_mov_prev_rest(params=None):

    temp_params = params.copy()

    theta = temp_params['prev'].values
    var = (theta * (1 - theta)) / ( temp_params['n'].values - 1 ) # normalized with n-1 see Bethlehem p.71
    ses = np.sqrt(var)
    temp_params['prev_se'] = ses

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
    params = temp_params.copy()

    return params
import numpy as np
import pandas as pd

def parameters_prev(counts=None, dataset=None, time_attribute=None, outcome_attribute=None):

    params = counts.join(dataset.groupby(time_attribute)[outcome_attribute].mean())
    params = params.rename(columns={outcome_attribute[0]: 'prev'})

    theta = params['prev'].values
    var = (theta * (1 - theta)) / ( params['n'].values - 1 ) # normalized with n - 1 see Bethlehem p.71
    ses = np.sqrt(var)
    params['prev_se'] = ses

    return params

def parameters_prev_rest(params=None):

    return params


import numpy as np
import pandas as pd

def parameters_mean(counts=None, dataset=None, time_attribute=None, outcome_attribute=None):

    params = counts.join(dataset.groupby(time_attribute)[outcome_attribute].mean())
    params = params.rename(columns={outcome_attribute[0]: 'mean'})

    theta = dataset.groupby(time_attribute)[outcome_attribute].std() # normalized with n-1
    ns = params['n'].pow(0.5)
    ses = theta.iloc[:,0] / ns
    params['mean_se'] = ses.values

    return params

def parameters_mean_rest(params=None):   

    return params
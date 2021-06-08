import numpy as np
import pandas as pd

def parameters_ratio(counts=None, dataset=None, time_attribute=None, outcome_attribute=None):

    var1 = 'Remainer'
    var2 = 'Leaver'
    
    mean_var1 = dataset.groupby(time_attribute)[var1].mean()
    mean_var2 = dataset.groupby(time_attribute)[var2].mean()
    
    params = counts
    params['mean_remainer'] = mean_var1
    params['mean_leaver'] = mean_var2

    params['ratio'] = np.nan
    all_occasions = params.index.values
    for occ in all_occasions:
        if params.loc[occ, 'mean_remainer'] > 0.0:
            if params.loc[occ, 'mean_leaver'] > 0.0:
                params.loc[occ, 'ratio'] = params.loc[occ, 'mean_remainer'] / params.loc[occ, 'mean_leaver']

    #params['ratio'] = params['mean_remainer'].values / params['mean_leaver'].values

    return params

def parameters_ratio_rest(params=None, dataset=None, time_attribute=None):

    var1 = 'Remainer'
    var2 = 'Leaver'

    # variance
    all_occasions = params.index.values
    params['ratio_se'] = np.nan

    for occ in all_occasions:
        if not np.isnan(params.loc[occ, 'ratio']):
            vals1 = dataset.loc[dataset[time_attribute[0]] == occ, var1]
            vals2 = dataset.loc[dataset[time_attribute[0]] == occ, var2]
            m1 = params.loc[occ, 'ratio']
            n = params.loc[occ, 'n']
            var = (1/n) * (1/(n-1)) * np.sum((vals1 - (vals2*m1))**2)
            params.loc[occ, 'ratio_se'] = np.sqrt(var)

    return params


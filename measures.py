import numpy as np
import pandas as pd

def calculate_z_values(general_params=None, subgroup_params=None, model_params=None):

    trend_var = model_params['trend_var']

    if model_params['hypothesis'] == 'data':
        dif = subgroup_params['params'][trend_var] - general_params['params'][trend_var]
        z = dif / subgroup_params['params'][trend_var + '_se']
        #print('z', z)

    elif model_params['hypothesis'] == 'value':
        if model_params['use_se']:
            dif = subgroup_params['params'][trend_var] - model_params['value']
            z = dif / subgroup_params['params'][trend_var + '_se']
        elif not model_params['use_se']:
            z = subgroup_params['params'][trend_var] - model_params['value']

    subgroup_params['z'] = z 

    return subgroup_params

def apply_qm_function(subgroup_params=None, model_params=None):

    if model_params['qm'] == 'max':
        qm_value = np.round(subgroup_params['z'].abs().max(), 2)

    elif model_params['qm'] == 'count':
        qm_value = np.sum(subgroup_params['z'].abs() < model_params['threshold'])
        sum_qm_value = np.round(np.sum(subgroup_params['z'][subgroup_params['z'].abs() < model_params['threshold']].abs()),3)
        subgroup_params['sum_qm_value'] = sum_qm_value
        
    elif model_params['qm'] == 'average':
        qm_value = np.round(subgroup_params['z'].abs().mean(), 2)

    subgroup_params['qm_value'] = qm_value    

    return subgroup_params
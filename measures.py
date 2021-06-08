import numpy as np
import pandas as pd

def calculate_z_values(general_params=None, subgroup_params=None, model_params=None):

    trend_var = model_params['trend_var']

    # for standard errors of 0, that is, when the prev is 0, z is np.nan if dif is 0, z is inf if dif is pos and z is -inf if dif is neg.

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
        elif model_params['use_se'] == 'multiply':
            dif = subgroup_params['params'][trend_var] - model_params['value']
            z = dif * subgroup_params['params'][trend_var + '_se']
        else:
            print('no choice made for how to use standard error')

    subgroup_params['z'] = z 

    return subgroup_params

def apply_qm_function(subgroup_params=None, model_params=None):

    if model_params['qm'] == 'max':
        qm_value = np.round(subgroup_params['z'].abs().max(), 2)

    elif model_params['qm'] == 'min':
        qm_value = np.round(subgroup_params['z'].abs().min(), 2)

    elif model_params['qm'] == 'count':
        qm_value = np.sum(subgroup_params['z'].abs() < model_params['threshold'])
        sum_qm_value = np.round(np.sum(subgroup_params['z'][subgroup_params['z'].abs() < model_params['threshold']].abs()),3)
        subgroup_params['sum_qm_value'] = sum_qm_value
        
    elif model_params['qm'] == 'average':
        qm_value = np.round(subgroup_params['z'].abs().mean(), 2)

    elif model_params['qm'] == 'sum':
        qm_value = np.round(subgroup_params['z'].abs().sum(), 2)

    subgroup_params['qm_value'] = qm_value    

    if np.isinf(qm_value):
        print(subgroup_params['z'])
        print(subgroup_params['params'])

    return subgroup_params
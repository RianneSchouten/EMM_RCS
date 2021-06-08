import numpy as np
import pandas as pd

import parameters_prev as pp
import parameters_prev_slope as pps
import parameters_mov_prev as pmp
import parameters_mov_prev_slope as pmps
import parameters_mean as pm
import parameters_ratio as pmr

def calculate_general_params(dataset=None, attributes=None, model_params=None):  

    params = calculate_first_part_params(dataset=dataset, attributes=attributes, model_params=model_params, general_params=None)
    params = calculate_second_part_params(params=params, dataset=dataset, attributes=attributes, model_params=model_params)

    return params

def calculate_first_part_params(dataset=None, attributes=None, model_params=None, general_params=None):

    id_attribute = attributes['id_attribute']
    time_attribute = attributes['time_attribute']
    outcome_attribute = attributes['outcome_attribute']

    # calculate counts
    # make sure that the subgroup params dataframe has the same size as the dataset one
    # this is necessary to check later whether slopes etc. can be calculated or not
    if not general_params is None:
        initial_params = pd.DataFrame(index=general_params['params'].index.values)
        initial_counts = dataset.groupby(time_attribute)[id_attribute].nunique()
        initial_counts = initial_counts.rename(columns={id_attribute[0]:'n'})
        counts = initial_params.join(initial_counts)
    else: 
        initial_counts = dataset.groupby(time_attribute)[id_attribute].nunique()
        counts = initial_counts.rename(columns={id_attribute[0]:'n'})

    if model_params['trend_var'] == 'prev':
        params = pp.parameters_prev(counts=counts, dataset=dataset, time_attribute=time_attribute, outcome_attribute=outcome_attribute)
    elif model_params['trend_var'] == 'prev_slope':
        params = pps.parameters_prev_slope(counts=counts, dataset=dataset, time_attribute=time_attribute, outcome_attribute=outcome_attribute)
    elif model_params['trend_var'] == 'mov_prev':
        params = pmp.parameters_mov_prev(counts=counts, dataset=dataset, time_attribute=time_attribute, outcome_attribute=outcome_attribute)
    elif model_params['trend_var'] == 'mov_prev_slope':
        params = pmps.parameters_mov_prev_slope(counts=counts, dataset=dataset, time_attribute=time_attribute, outcome_attribute=outcome_attribute)
    elif model_params['trend_var'] == 'mean':
        params = pm.parameters_mean(counts=counts, dataset=dataset, time_attribute=time_attribute, outcome_attribute=outcome_attribute)
    elif model_params['trend_var'] == 'ratio':
        params = pmr.parameters_ratio(counts=counts, dataset=dataset, time_attribute=time_attribute, outcome_attribute=None)
    else: 
        print('trend variable not available')

    return params

def calculate_second_part_params(params=None, model_params=None, dataset=None, attributes=None):

    if model_params['trend_var'] == 'prev':
        params = pp.parameters_prev_rest(params=params)
    elif model_params['trend_var'] == 'prev_slope':
        params = pps.parameters_prev_slope_rest(params=params)
    elif model_params['trend_var'] == 'mov_prev':
        params = pmp.parameters_mov_prev_rest(params=params)
    elif model_params['trend_var'] == 'mov_prev_slope':
        params = pmps.parameters_mov_prev_slope_rest(params=params)
    elif model_params['trend_var'] == 'mean':
        params = pm.parameters_mean_rest(params=params)
    elif model_params['trend_var'] == 'ratio':
        params = pmr.parameters_ratio_rest(params=params, dataset=dataset, time_attribute=attributes['time_attribute'])

    return params

def calculate_minimum_size(params=None, min_size=None):

    params['min_size'] = params['n']*min_size

    return params




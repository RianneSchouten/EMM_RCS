import numpy as np

import parameters as pa
import measures as me

def calculate_general_parameters(dataset=None, attributes=None, model_params=None, constraints=None):

    params = pa.calculate_general_params(dataset=dataset, attributes=attributes, model_params=model_params)
    params_with_min = pa.calculate_minimum_size(params=params, min_size=constraints['min_size'])
    general_params = {'data_size': len(dataset), 'params': params_with_min, 'T': len(params)}

    return general_params

def calculate_first_part_subgroup_parameters(subgroup=None, attributes=None, model_params=None, general_params=None):

    params = pa.calculate_first_part_params(dataset=subgroup, attributes=attributes, model_params=model_params, general_params=general_params)
    subgroup_params = {'sg_size': np.sum(params['n']), 'params': params}    

    occassion_selector = params.index.values
    subgroup_params['occassion_selector'] = occassion_selector

    return subgroup_params

def calculate_second_part_subgroup_parameters(subgroup_params=None, subgroup=None, attributes=None, model_params=None):

    added_params = pa.calculate_second_part_params(params=subgroup_params['params'], dataset=subgroup, attributes=attributes, model_params=model_params)
    subgroup_params['params'] = added_params    

    return subgroup_params

def add_qm(desc=None, general_params=None, subgroup_params=None, model_params=None, beam_search_params=None):

    # calculate z, gives a vector of T values, add in dictionary
    subgroup_params = me.calculate_z_values(general_params=general_params, subgroup_params=subgroup_params, model_params=model_params)
    
    # apply qm function, gives one value per subgroup, add in dictionary
    subgroup_params = me.apply_qm_function(subgroup_params=subgroup_params, model_params=model_params)

    # add new measures to the qualities part
    # we add sg_size here so that it will become part of the output
    desc_qm = desc.copy()
    subgroup_params['sg_size'] = np.round(subgroup_params['sg_size'] / general_params['data_size'],2)
    #subgroup_params['sg_idx'] = subgroup_params['sg_idx']
    desc_qm['qualities'] = subgroup_params.copy()

    return desc_qm




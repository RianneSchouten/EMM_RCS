import numpy as np
import pandas as pd
import itertools as it

import select_subgroup as ss
import collect_qualities as qu
import constraints as cs

def apply_dominance_pruning(result_set=None, dataset=None, descriptives=None, attributes=None, general_params=None, model_params=None, beam_search_params=None, constraints=None):

    print('start pruning')
    pruned_descriptions = get_new_descriptions(result_set=result_set)
    pruned_subgroups, n_small_groups, n_type_small_subgroup, n_type_small_occassions, n_type_no_subgroup, n_connected_occassions = get_new_qualities(pruned_descriptions=pruned_descriptions, \
        dataset=dataset, descriptives=descriptives, attributes=attributes, general_params=general_params, model_params=model_params, beam_search_params=beam_search_params, constraints=constraints)

    # append with result_set, to keep the original subgroups as well
    all_subgroups = [result_set.copy()]
    all_subgroups.append(pruned_subgroups)
    all_subgroups = [item for sublist in all_subgroups for item in sublist]

    return all_subgroups, len(pruned_descriptions), n_small_groups, n_type_small_subgroup, n_type_small_occassions, n_type_no_subgroup, n_connected_occassions

def get_new_descriptions(result_set=None):

    pruned_descriptions = []
    for existing_subgroup in result_set:

        old_desc = existing_subgroup['description']
        items_old_desc = old_desc.items()

        for r in np.arange(1, len(list(items_old_desc))):
            combs = list(it.combinations(items_old_desc, r=r))
            combs_r = [{'description': dict(desc)} for desc in combs]
            pruned_descriptions.append(combs_r)

    pruned_descriptions = [item for sublist in pruned_descriptions for item in sublist]

    return pruned_descriptions

def get_new_qualities(pruned_descriptions=None, dataset=None, descriptives=None, attributes=None, general_params=None, model_params=None, beam_search_params=None, constraints=None):

    pruned_subgroups = []
    n_small_groups = 0
    n_type_small_subgroup = 0
    n_type_small_occassions = 0
    n_type_no_subgroup = 0
    n_connected_occassions = 0
    
    for desc in pruned_descriptions:

        #print(desc)

        subgroup, idx_sg, subgroup_compl, idx_compl = ss.select_subgroup(description=desc['description'], df=dataset, descriptives=descriptives)
        
        if len(idx_sg) == 0:
            n_small_groups += 1
            n_type_no_subgroup += 1
                    
        else: 
            subgroup_params = qu.calculate_first_part_subgroup_parameters(subgroup=subgroup, attributes=attributes, model_params=model_params, general_params=general_params)
            subgroup_params['sg_idx'] = idx_sg # necessary for weighting when selecting beam, see below
                            
            # a check on subgroup size
            check_size, constraint_type, subgroup_params = cs.constraint_subgroup_size(general_params=general_params, subgroup_params=subgroup_params, 
                                                                                   constraints=constraints, model_params=model_params)
            if not check_size:
                n_small_groups += 1
                if constraint_type == 'small_subgroup': n_type_small_subgroup += 1
                elif constraint_type == 'small_occassions': n_type_small_occassions += 1
                print('subgroup too small')
            else: 

                subgroup_params = qu.calculate_second_part_subgroup_parameters(subgroup_params=subgroup_params, model_params=model_params, subgroup=subgroup, attributes=attributes)
                check_connected_occassions = cs.constraint_connected_occassions(general_params=general_params, subgroup_params=subgroup_params, 
                                                                            constraints=constraints, model_params=model_params)

                if not check_connected_occassions:
                    n_connected_occassions += 1
                    print('nr of measurement occassions not met')
            
                else:                
                
                    desc_qm = qu.add_qm(desc=desc, general_params=general_params, subgroup_params=subgroup_params, 
                                model_params=model_params, beam_search_params=beam_search_params) 
                    pruned_subgroups.append(desc_qm) 

    return pruned_subgroups, n_small_groups, n_type_small_subgroup, n_type_small_occassions, n_type_no_subgroup, n_connected_occassions
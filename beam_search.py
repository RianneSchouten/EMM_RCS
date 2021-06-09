import numpy as np
import pandas as pd

import collect_qualities as qu
import refinements as rf
import select_subgroup as ss
import constraints as cs
import prepare_beam as pb
import prepare_result as pr
import dominance_pruning as dp

def beam_search(dataset=None, attributes=None, descriptives=None, model_params=None, beam_search_params=None, wcs_params=None, constraints=None):

    general_params = qu.calculate_general_parameters(dataset=dataset, attributes=attributes, model_params=model_params, constraints=constraints)
    print(len(general_params['params']))
    print(general_params['params'])
    candidate_queue = rf.create_starting_descriptions(dataset=dataset, descriptives=descriptives, b=beam_search_params['b'])
    #print(candidate_queue)

    candidate_result_set = []
    considered_subgroups = {}
    for d_i in range(1, beam_search_params['d']+1):

        print('d_i', d_i)

        n_consd = 0
        n_small_groups = 0
        n_type_small_subgroup = 0
        n_type_small_occassions = 0
        n_type_no_subgroup = 0
        n_sim_descs = 0
        n_connected_occassions = 0

        cq_satisfied = []
        for seed in candidate_queue:

            #print('seed', seed)

            if d_i == 1:
                seed_set = []
                seed_set.append(seed)
            else:                
                subgroup, idx_sg, subgroup_compl, idx_compl = ss.select_subgroup(description=seed['description'], df=dataset, descriptives=descriptives)
                seed_set = rf.refine_seed(seed=seed, subgroup=subgroup, descriptives=descriptives, b=beam_search_params['b'])

            for desc in seed_set:

                #print('desc', desc)
                n_consd += 1

                # a check for similar descriptions
                check_similar_description = cs.similar_description(desc=desc, cq_satisfied=cq_satisfied)    

                if not check_similar_description:
                    n_sim_descs += 1
                    #print('redundancy_check_description false for ', desc)
                else:

                    subgroup, idx_sg, subgroup_compl, idx_compl = ss.select_subgroup(description=desc['description'], df=dataset, descriptives=descriptives)
                    
                    if len(idx_sg) == 0:
                        n_small_groups += 1
                        n_type_no_subgroup += 1
                    
                    else: 
                        subgroup_params = qu.calculate_first_part_subgroup_parameters(subgroup=subgroup, attributes=attributes, model_params=model_params, general_params=general_params)
                        
                        #if list(desc['description'].keys())[0] in ['Hindsight','EURef2016']:
                        #    print(subgroup_params['params'])
                        
                        subgroup_params['sg_idx'] = idx_sg # necessary for weighting when selecting beam, see below
                            
                        # a check on subgroup size
                        check_size, constraint_type, subgroup_params = cs.constraint_subgroup_size(general_params=general_params, subgroup_params=subgroup_params, 
                                                                                                   constraints=constraints, model_params=model_params)
                        if not check_size:
                            n_small_groups += 1
                            if constraint_type == 'small_subgroup': n_type_small_subgroup += 1
                            elif constraint_type == 'small_occassions': n_type_small_occassions += 1
                            #print('subgroup too small')
                        else: 

                            subgroup_params = qu.calculate_second_part_subgroup_parameters(subgroup_params=subgroup_params, model_params=model_params, subgroup=subgroup, attributes=attributes)
                            check_connected_occassions = cs.constraint_connected_occassions(general_params=general_params, subgroup_params=subgroup_params, 
                                                                                            constraints=constraints, model_params=model_params)

                            if not check_connected_occassions:
                                n_connected_occassions += 1
                                #print('nr of measurement occassions not met')
                            else:                             

                                desc_qm = qu.add_qm(desc=desc, general_params=general_params, subgroup_params=subgroup_params, 
                                                model_params=model_params, beam_search_params=beam_search_params) 
                                cq_satisfied.append(desc_qm)                                                               
                    
        considered_subgroups['level_' + str(d_i)] = {'n_consd': n_consd, 'n_sim_descs': n_sim_descs, 
                                                     'n_small_groups': n_small_groups, 
                                                     'n_type_small_subgroup': n_type_small_subgroup,
                                                     'n_type_small_occassions': n_type_small_occassions, 
                                                     'n_type_no_subgroup': n_type_no_subgroup,
                                                     'n_connected_occassions': n_connected_occassions}

        # below we prepare the result set and beam (candidate_queue) for the next level
        # here, we apply description based selection and cover based selection to prevent issues with redundancy
        beam_search_params.update({'d_i': d_i})
        candidate_result_set, candidate_queue, n_redun_descs = pb.collect_beam_and_candidate_result_set(candidate_result_set=candidate_result_set, cq_satisfied=cq_satisfied, 
                                                                                                        model_params=model_params, beam_search_params=beam_search_params, 
                                                                                                        data_size=general_params['data_size'], wcs_params=wcs_params)
        considered_subgroups['level_' + str(d_i)]['n_redun_decs'] = n_redun_descs

    result_set, rs_n_redun_descs = pr.select_result_set(candidate_result_set=candidate_result_set[0], model_params=model_params, beam_search_params=beam_search_params, 
                                                        data_size=general_params['data_size'], wcs_params=wcs_params)

    # apply dominance pruning
    result_set_pruned, n_consd, n_small_groups, n_type_small_subgroup, n_type_small_occassions, n_type_no_subgroup, n_connected_occassions = dp.apply_dominance_pruning(result_set=result_set, \
        dataset=dataset, descriptives=descriptives, attributes=attributes, general_params=general_params, model_params=model_params, beam_search_params=beam_search_params, constraints=constraints)
    # again apply description and cover based selection
    final_result_set, rs_n_redun_descs = pr.select_result_set(candidate_result_set=result_set_pruned, model_params=model_params, beam_search_params=beam_search_params, 
                                                              data_size=general_params['data_size'], wcs_params=wcs_params)
        
    considered_subgroups['dominance_pruning'] = {'n_consd': n_consd, 'n_sim_descs': None, 
                                                 'n_small_groups': n_small_groups, 'n_type_small_subgroup': n_type_small_subgroup, 
                                                 'n_type_small_occassions': n_type_small_occassions, 'n_connected_occassions': n_connected_occassions,
                                                 'n_type_no_subgroup': n_type_no_subgroup, 'n_redun_decs': rs_n_redun_descs}

    # result_set is a dictionary
    # result_emm is a dataframe with the descriptive attributes on the columns, and q*2 rows
    result_emm = pr.prepare_result_list(result_set=final_result_set)

    return result_emm, general_params, considered_subgroups
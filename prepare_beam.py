import numpy as np
import pandas as pd

import desc_based_selection as dbs
import cover_based_selection as cbs

def collect_beam_and_candidate_result_set(candidate_result_set=None, cq_satisfied=None, model_params=None, beam_search_params=None, data_size=None, wcs_params=None):

    n_redun_descs = None
    if len(cq_satisfied) > 0:

        # follow procedure using 1 quality measure
        # we apply description based selection and cover based selection to prevent issues with redundancy
        print('arrives here')
        candidate_result_set, candidate_queue, n_redun_descs = prepare_beam_and_candidate_result_set(candidate_result_set=candidate_result_set, 
                                                                                                         cq_satisfied=cq_satisfied, 
                                                                                                         model_params=model_params, beam_search_params=beam_search_params,
                                                                                                         data_size=data_size, wcs_params=wcs_params)
    
    else:

        candidate_queue = []

    return candidate_result_set, candidate_queue, n_redun_descs

def prepare_beam_and_candidate_result_set(candidate_result_set=None, cq_satisfied=None, model_params=None, beam_search_params=None, data_size=None, wcs_params=None):

    if model_params['order'] == 'max':
        reverse = True
    elif model_params['order'] == 'min':
        reverse = False

    # sort cq_satisfied on quality value
    if model_params['qm'] == 'count': cq_sorted = sorted(cq_satisfied, key=lambda i: (i['qualities']['qm_value'],i['qualities']['sum_qm_value']), reverse=reverse)       
    else: cq_sorted = sorted(cq_satisfied, key = lambda i: i['qualities']['qm_value'], reverse=reverse)     
    
    # apply description-based selection
    # difficult to know when to stop
    # only from 2nd level and onwards
    print('description-based selection')
    candidates, n_redun_descs = dbs.remove_redundant_descriptions(descs=cq_sorted, stop_number=wcs_params['stop_desc_sel'], 
                                                                  model_params=model_params, beam_search_params=beam_search_params)

    # apply cover-based selection
    # len(candidates) should always be larger than 0, at least 1 description will be maintained
    print('cover-based selection')
    candidate_queue = cbs.select_using_weighted_coverage(candidates=candidates, stop_number=beam_search_params['w'], 
                                                         data_size=data_size, wcs_params=wcs_params, model_params=model_params)

    # we have the same procedure for the result set
    # but we only do it at the end of the entire beam search
    # in every level of the beam search we only select the first q of the beam
    selected_for_result_list = candidate_queue[0:beam_search_params['q']]
    candidate_result_set.append(selected_for_result_list) # creates a nested list
    rs_candidates = [item for sublist in candidate_result_set for item in sublist] # unlist alle elements

    return [rs_candidates], candidate_queue, n_redun_descs
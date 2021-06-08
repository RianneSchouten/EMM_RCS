import numpy as np
import pandas as pd

def select_using_weighted_coverage(candidates=None, stop_number=None, data_size=None, wcs_params=None, model_params=None):

    # if the number of candidates is smaller than the desired number, we can just select all candidates
    if len(candidates) > stop_number:

        all_idx = pd.DataFrame(pd.Series(np.zeros(data_size)), columns=[['count']])

        # list has to be sorted
        # already sorted during description-based selection    
        # first pop sg_idx from first candidate, leftover is the candidate without sg_idx

        #sel_idx = candidates[0]['qualities'].pop('sg_idx')
        sel_idx = candidates[0]['qualities']['sg_idx']
        sel = [candidates[0]]
        left_over_candidates = candidates.copy()
        left_over_candidates.remove(left_over_candidates[0])

        i = 1
    
        while i < stop_number:
       
            # update weight of cases coverd by already selected descriptions    
            all_idx.loc[sel_idx,['count']] = all_idx.loc[sel_idx,['count']] + 1        
            candidates_with_updated_qms = []

            for candidate in left_over_candidates:
                
                # select rows in current candidate and calculate weight for candidate
                sg_idx = candidate['qualities']['sg_idx']
                all_weights = np.power(wcs_params['gamma'], all_idx.loc[sg_idx, ['count']].values)
                weight = np.sum(all_weights) / len(sg_idx)

                # calculate new quality value with weight for subgroup
                candidate['qualities']['temp_qm_value'] = candidate['qualities']['qm_value'] * weight
                candidates_with_updated_qms.append(candidate)

            # re-sort candidates
            if model_params['order'] == 'max':
                reverse = True
            elif model_params['order'] == 'min':
                reverse = False
            candidates_sorted = sorted(candidates_with_updated_qms, key = lambda i: i['qualities']['temp_qm_value'], reverse=reverse)
            # select first candidate and update other lists
            #sel_idx = candidates_sorted[0]['qualities'].pop('sg_idx')
            sel_idx = candidates_sorted[0]['qualities']['sg_idx']
            sel.append(candidates_sorted[0])
            left_over_candidates.remove(candidates_sorted[0])
            i += 1

    else:

        sel = candidates

    return sel
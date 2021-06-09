import numpy as np
import pandas as pd

def remove_redundant_descriptions(descs=None, stop_number=None, model_params=None, beam_search_params=None):

    all_descs = descs.copy()

    if beam_search_params['d_i'] > 1:

        # even if the length of descs is small, we still want to remove redundant descriptions
        if len(all_descs) > stop_number:
            stop_at = stop_number
        else: 
            stop_at = len(all_descs)

        i = 1
        candidates = [all_descs[0]]
        n_redun_descs = 0
        while i < stop_at:
            #print(i)
            new_desc = all_descs[i]
            #print('new_desc', new_desc['description'])
            for old_desc in candidates:

                if model_params['qm'] == 'count':
                    if (new_desc['qualities']['qm_value'] == old_desc['qualities']['qm_value']) & (new_desc['qualities']['sum_qm_value'] == old_desc['qualities']['sum_qm_value']):
                        remove = compare_two_descs(old_desc=old_desc['description'], new_desc=new_desc['description'])
                        if remove == 'old_desc':
                            #print('remove old desc')
                            candidates.remove(eval(remove))
                            n_redun_descs += 1
                        elif remove == 'new_desc':
                            #print('remove new desc')
                            n_redun_descs += 1
                            break # return to while loop, break the for loop
                    else:
                        remove = None

                else:
                                 
                    if new_desc['qualities']['qm_value'] == old_desc['qualities']['qm_value']:
                        #print('old_desc', old_desc['description'])
                        remove = compare_two_descs(old_desc=old_desc['description'], new_desc=new_desc['description'])
                        if remove == 'old_desc':
                            #print('remove old desc')
                            candidates.remove(eval(remove))
                            n_redun_descs += 1
                        elif remove == 'new_desc':
                            #print('remove new desc')
                            n_redun_descs += 1
                            break # return to while loop, break the for loop
                    else:
                        remove = None
            if not remove == 'new_desc':                    
                candidates.append(new_desc)
            i += 1

    else:

        n_redun_descs = None
        candidates = all_descs

    return candidates, n_redun_descs

def compare_two_descs(old_desc=None, new_desc=None):

    length_dif = len(new_desc) - len(old_desc)

    remove = None
    if np.abs(length_dif) > 1:
        remove = None

    # new_desc is smaller than old_desc
    # check if all items exist in old_desc
    # if so, the new_desc is a general description/subset of old_desc
    elif length_dif == -1:
        items_exist_in_old_desc = [item in list(old_desc.items()) for item in list(new_desc.items())]
        #print('items_exist_in_old_desc', items_exist_in_old_desc)
        if np.all(items_exist_in_old_desc):
            remove = 'old_desc'

    # old_desc is smaller than new_desc
    # same procedure
    elif length_dif == 1:
        items_exist_in_new_desc = [item in list(new_desc.items()) for item in list(old_desc.items())]
        #print('items_exist_in_new_desc', items_exist_in_new_desc)
        if np.all(items_exist_in_new_desc):
            remove = 'new_desc'

    # check difference
    # if two or more keys are different, both can be kept
    # if two or more literals are different, both can be kept
    # otherwise, take the more general description
    elif length_dif == 0:
        same_keys = [key not in list(old_desc.keys()) for key in list(new_desc.keys())]
        #print('same_keys', same_keys)
        if np.sum(same_keys) < 2:
            same_descs = [item not in list(old_desc.items()) for item in list(new_desc.items())]
            #print('same_descs', same_descs)
            if np.sum(same_descs) == 1:
                # we know the difference is in the key difference, we remove the latest one
                remove = 'new_desc'
            elif np.sum(same_descs) == 0:
                # remove the more general description
                # bit complex to write, for convenience we remove the latest one
                remove = 'new_desc'
            else: 
                remove = None

    else:
        print('some mistake, new subgroup is larger than old subgroup')
        remove = None

    #print('remove', remove)

    return remove
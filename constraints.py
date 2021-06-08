import numpy as np

# because the descriptions are saved in a dictionary
# it is possible to compare them without reordering them
# the binary, nominal (tuple), ordinal (Index) and numerical (tuple) can be handled
def similar_description(desc=None, cq_satisfied=None):

    check_similar_description = True

    # check for redundant descriptions (the exact same description but in another order)
    # the comparison has to be done with the candidate queue of the current iteration only
    # this queue is saved in cq_satisfied
    # in theory, a refinement at the current level can be similar to a desc from an earlier level
    # this can happen for numerical and ordinal attributes
    # changes are low that those descriptions will end up in the result list together
    for seed in cq_satisfied:
        if desc['description'] == seed['description']:
            check_similar_description = False
            break

    return check_similar_description

# per year/meting, the size should be at least min_size 
# the min_size values are saved in general_params
def constraint_subgroup_size(general_params=None, subgroup_params=None, constraints=None, model_params=None):

    T = general_params['T']    
    threshold = np.floor(constraints['min_occassions'] * T)

    occassion_selector = subgroup_params['occassion_selector']
    subgroup_values = subgroup_params['params']['n'].values
    general_values = general_params['params'].loc[occassion_selector, 'min_size'].values

    if len(occassion_selector) < threshold:
        #print('len < threshold')
        return False, 'small_subgroup', None
    
    else:     
        difs = subgroup_values - general_values
        t = np.sum(difs >= 0)

        if t == T:
            return True, np.nan, subgroup_params

        # subgroup can continue because the minimum number of observed occassion is met
        # we should check however if for a trend_var that includes slope or mean, there are still enough occassions
        # and then we change the occassion selector
        elif t >= threshold:

            #print(subgroup_params['params'])
            # adapt subgroup params
            new_subgroup_params = adapt_subgroup_params(difs=difs, subgroup_params=subgroup_params, model_params=model_params)     
            #print(new_subgroup_params['params'])

            return True, np.nan, new_subgroup_params

        # if too many occassions have a small sample size, we cannot continue with this subgroup
        elif t < threshold:
            #print('t < threshold')
            return False, 'small_occassions', None

        else: 
            print('ends up here')

def constraint_connected_occassions(general_params=None, subgroup_params=None, constraints=None, model_params=None):

    trend_var = model_params['trend_var']

    if trend_var in ['prev', 'mean']:
        return True
    else:
        temp_params = subgroup_params['params'].copy()
        temp_params = temp_params.reset_index()
        idx_subgroup = temp_params[temp_params[trend_var].notnull()].index.values
        T = general_params['T']    
        threshold = np.floor(constraints['min_occassions'] * T)
        
        if len(idx_subgroup) < threshold:
            return False
        else:
            return True

            # for slope, mov or other summary point estimates, if there are no two values in a row
            # during parameter calculation, it will end in a np.nan in params
            # therefore, we just have to count the number of available values in the right column in params
            # and check if there are at least threshold number of measurement occassions with a value

            '''
            # check whether there are enough connected measurement occassions
            idx = np.array(idx_subgroup)            
            if trend_var in ['prev_slope', 'mov_prev']:
                idx_dif = idx[1:] - idx[:-1]
                t = len(idx_dif[idx_dif == 1])
                if t < threshold:
                    return False
                else: 
                    # select those measurement occassions for calculating qm
                    return True
            if trend_var in ['mov_prev_slope']:
                print(idx)
                idx_dif = idx[2:] - idx[:-2]
                print(idx_dif)
                t = len(idx_dif[idx_dif == 2])
                print(t)
                if t < threshold:
                    return False
                else:
                    return True
            '''

def adapt_subgroup_params(difs=None, subgroup_params=None, model_params=None):

    new_subgroup_params = subgroup_params.copy()

    sel = difs > 0
    all_idx = new_subgroup_params['params'].index.values
    sel_idx = [all_idx[i] for i in np.arange(len(all_idx)) if not sel[i]]

    #print(new_subgroup_params['params'])
    
    #np.where(difs < 0)
    #print(idx)
    #all_idx = np.arange(len(subgroup_params['occassion_selector']))
    #sel_idx = np.setdiff1d(all_idx, idx)
    #new_sel = [new_subgroup_params['occassion_selector'][i] for i in sel_idx]
    new_sel = [i for i in all_idx if i not in sel_idx]
    new_subgroup_params['occassion_selector'] = new_sel
    
    new_params = new_subgroup_params['params']
    if model_params['trend_var'] in ['prev', 'prev_slope', 'mov_prev', 'mov_prev_slope']:
        new_params.loc[sel_idx, 'prev'] = np.nan
    elif model_params['trend_var'] == 'mean':
        new_params.loc[sel_idx, 'mean'] = np.nan
    elif model_params['trend_var'] == 'ratio':
        new_params.loc[sel_idx, 'ratio'] = np.nan

    new_subgroup_params['params'] = new_params

    #print(new_subgroup_params['params'])

    return new_subgroup_params
import numpy as np
import pandas as pd
import random as r
from joblib import Parallel, delayed

import beam_search as bs

def distribution_false_discoveries_params(m=None, model_params=None, beam_search_params=None, dataset=None, attributes=None, descriptives=None, 
                                          wcs_params=None, constraints=None):

    beam_search_params_temp = beam_search_params.copy()
    beam_search_params_temp['q'] = 1
    distribution = make_distribution_false_discoveries(m=m, model_params=model_params, 
                                                       dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                                       beam_search_params_temp=beam_search_params_temp, 
                                                       wcs_params=wcs_params, constraints=constraints)

    #distribution = [1,2,3]
    mu = np.mean(distribution)
    std = np.std(distribution)

    cutoff90 = mu + 1.645*std
    cutoff95 = mu + 1.96*std
    cutoff99 = mu + 2.58*std

    distribution_params = {'m': m, 'distribution': distribution, 
                           'mu': mu, 'std': std, 
                           'cutoff90': cutoff90, 'cutoff95': cutoff95, 'cutoff99': cutoff99}

    return distribution_params

def make_distribution_false_discoveries(m=None, model_params=None, 
                                        dataset=None, attributes=None, descriptives=None, 
                                        beam_search_params_temp=None, wcs_params=None, constraints=None):

    inputs = range(m)
    print('building distribution of false discoveries...')

    qm_values = Parallel(n_jobs=-2)(delayed(make_false_discovery)(i, model_params, dataset, attributes, descriptives, 
                                                                  beam_search_params_temp, wcs_params,
                                                                  constraints) for i in inputs)

    return qm_values

def make_false_discovery(i=None, model_params=None, 
                         dataset=None, attributes=None, descriptives=None, 
                         beam_search_params_temp=None, wcs_params=None, constraints=None):

    print(i)

    shuffled_dataset = shuffle_dataset(dataset=dataset, attributes=attributes, descriptives=descriptives)

    # perform beam search    
    result_emm, general_params, considered_subgroups = bs.beam_search(dataset=shuffled_dataset, attributes=attributes, descriptives=descriptives, 
                                                                      model_params=model_params, beam_search_params=beam_search_params_temp, wcs_params=wcs_params,
                                                                      constraints=constraints)

    # save qm of the first subgroup
    qm_value = result_emm.loc[result_emm.sg == 0, 'qm_value'].values[1] # 1 is qualities

    return qm_value

def shuffle_dataset(dataset=None, attributes=None, descriptives=None):

    id_attribute = attributes['id_attribute'][0]
    time_attribute = attributes['time_attribute'][0]
    outcome_attribute = attributes['outcome_attribute'][0]

    keep_cols = [time_attribute, outcome_attribute]
    cols = dataset.columns
    cols_descs = cols.drop(keep_cols)

    cnts = dataset[id_attribute].value_counts().sort_index()
    idx = cnts.index.values
    
    new_idx = idx.copy()
    r.shuffle(new_idx)

    #print('make new dataset')
    #print(dataset.shape)
    #print(dataset.tail())
    out = list(map(lambda x: dataset.loc[new_idx[x], cols_descs], np.arange(0, len(new_idx))))
    new = pd.DataFrame(out)
    #print(new.head())
    new.reset_index(drop=True,inplace=True)

    old = dataset[keep_cols]
    shuffled_dataset = new.join(old)

    shuffled_dataset[descriptives['num_atts']] = shuffled_dataset[descriptives['num_atts']].astype('float')
    shuffled_dataset[descriptives['nom_atts']] = shuffled_dataset[descriptives['nom_atts']].astype('object')
    shuffled_dataset[descriptives['bin_atts']] = shuffled_dataset[descriptives['bin_atts']].astype('object')
    shuffled_dataset[descriptives['ord_atts']] = shuffled_dataset[descriptives['ord_atts']].astype('category')

    #categories are not ordered anymore
    #print(shuffled_dataset['schnivo'].cat.categories)

    return shuffled_dataset
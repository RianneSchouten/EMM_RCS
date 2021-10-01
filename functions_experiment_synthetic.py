import numpy as np
import pandas as pd
import random as r
import itertools as it

def generate_dataset(params=None, simulation_params=None):

    covs, cov_names = sample_covs(N=simulation_params['N'], ncovs=simulation_params['ncovs'], p=simulation_params['p'])

    df = covs.copy()
    df[simulation_params['trend_name']] = np.random.normal(loc=10.0, scale=1.0, size=simulation_params['N'])

    #print(df.head(20))
    true_description = find_true_description(nlits=params[2], ncovs=simulation_params['ncovs'])
    #print(true_description)

    # generate subgroup
    dataset = generate_subgroup(df=df, true_description=true_description, dist=params[0], sd=params[1], simulation_params=simulation_params)    
    dataset_ordered, attributes, descriptives = define_attributes(dataset=dataset, cov_names=cov_names, simulation_params=simulation_params)

    #print(dataset_ordered)

    return dataset_ordered, attributes, descriptives, true_description

def define_attributes(dataset=None, cov_names=None, simulation_params=None):

    dataset['tp'] = r.choices(list(np.arange(1,simulation_params['tp']+1)),k=simulation_params['N'])
    data_sorted = dataset.sort_values(['tp'], ascending=[True])
    data_sorted['id'] = np.arange(len(data_sorted))

    #print(data_sorted.head(20))

    descriptives = {'num_atts': [], 'bin_atts': cov_names, 
                    'nom_atts': [], 'ord_atts': []}
    attributes = {'time_attribute': ['tp'], 'skip_attributes': [],
                  'id_attribute': ['id'], 'outcome_attribute': [simulation_params['trend_name']]}

    return data_sorted, attributes, descriptives

def generate_subgroup(df=None, true_description=None, dist=None, sd=None, simulation_params=None):

    dataset = df.copy()
    desc = true_description

    # select cov_names based on desc
    mask = (dataset[list(desc.keys())] == pd.Series(desc)).all(axis=1)
    #print(np.sum(mask))

    n = np.sum(mask)
    trend_values = np.random.normal(loc=10.0+dist, scale=sd, size=n)
    dataset.loc[mask, simulation_params['trend_name']] = trend_values 

    return dataset

def sample_covs(N=None, ncovs=None, p=None):

    # sample covariates
    covs = pd.DataFrame()
    for cov in np.arange(1,ncovs+1):
        covs['x' + str(cov)] = np.random.binomial(n=1, p=p, size=N)

    cov_names = ['x' + str(k) for k in np.arange(1,ncovs+1)]

    return covs, cov_names

def find_true_description(nlits=None, ncovs=None):
   
    true_description = {}
    # randomly choose covs from entire list
    # number of lits is determined by params[2]
    lits = r.sample(list(np.arange(1,ncovs+1)),nlits) # returns list
    for l in lits:
        true_description['x' + str(l)] = 1

    return true_description

def process_result(result_emm=None, true_description=None):

    #print(true_description)
    vars = list(true_description.keys())
    for var in vars:
        if var not in result_emm:
            result_emm[var] = np.nan

    cols = result_emm.dtypes.index
    covs = cols[cols.str.startswith('x')]
    descriptions = result_emm.loc['description', covs]
    descriptions.reset_index(drop=True,inplace=True)
    descriptions.fillna(value=999,inplace=True)
    #stack = descriptions.stack()
    #stack[pd.isnull(stack)] = 999
    #descriptions = stack.unstack()
    #descriptions[pd.isnull(descriptions)] = 999
    #print(descriptions)

    all_covs = {k: 999 for k in covs}
    for lit in vars:
        all_covs[lit] = [1]
    
    
    equal = descriptions.apply(lambda row: row == pd.Series(all_covs), axis=1)

    quals = result_emm.loc['qualities', :] 
    quals.reset_index(drop=True,inplace=True)
    sel_qual = quals.loc[equal.all(axis=1)]

    result = {}
    if len(sel_qual) > 0:    
        result['quality_value'] = sel_qual['qm_value'].values[0]
        result['rank'] = sel_qual['sg'].values[0] + 1
        result['size'] = sel_qual['sg_size'].values[0]
    else:
        result['quality_value'] = 0
        result['rank'] = 51
        result['size'] = 0

    return result
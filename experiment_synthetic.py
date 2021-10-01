import numpy as np
import pandas as pd
import random as r
import itertools as it
from joblib import Parallel, delayed

import preprocess as pp
import beam_search as bs
import functions_experiment_synthetic as fes

def experiment(simulation_params=None, beam_search_params=None, model_params=None, constraints=None, wcs_params=None,
               nreps=None):
               
    parameter_set = list(it.product(simulation_params['distances'], simulation_params['sds'], simulation_params['ds']))
    nexp = len(parameter_set)

    for exp in np.arange(nexp):   
        print('experiment', exp+1, 'of', nexp)

        params = parameter_set[exp]
        print('parameters:', params)

        ranks_one_parameter_run = parallelization(nreps=nreps, params=params, simulation_params=simulation_params, 
                                                  beam_search_params=beam_search_params, 
                                                  model_params=model_params, constraints=constraints, wcs_params=wcs_params)
        
        # concatenate all results per parameter combination
        params_pd = pd.DataFrame(np.tile(params, nreps).reshape(nreps, len(params)), 
                                 columns = ['distance', 'sd', 'd'])
        ranks_pd = pd.DataFrame(ranks_one_parameter_run)
        results_one_parameter_pd = pd.concat((params_pd, ranks_pd), axis=1)
        results_one_parameter_pd.insert(len(params), 'nreps', pd.DataFrame(np.arange(1, nreps+1)))   

        # save with the parameter combination
        if exp == 0:
            result_experiment = results_one_parameter_pd
        else:
            result_experiment = result_experiment.append(results_one_parameter_pd)
        result_experiment.reset_index(drop=True)

    # saving
    data_output_location = './data_output/Synthetic/' + 'Experiment' + '_' + \
        str(list(simulation_params.values())) + '.xlsx'

    beam_search_params.update(constraints)
    beam_search_params.update(wcs_params)
    beam_search_params.update(model_params)
    analysis_info = pd.DataFrame(beam_search_params, index=[0])

    dfs = {'result_experiment': result_experiment, 'analysis_info': analysis_info}
    
    writer = pd.ExcelWriter(data_output_location, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.save()    

def parallelization(nreps=None, params=None, simulation_params=None, beam_search_params=None, model_params=None, constraints=None, wcs_params=None):

    inputs = range(nreps)
    #num_cores = multiprocessing.cpu_count() - 2

    print('iterations...')

    ranks_one_parameter_run = Parallel(n_jobs=-2)(delayed(one_parameter_run)(i,
                                                                             params,
                                                                             simulation_params,
                                                                             beam_search_params, 
                                                                             model_params, 
                                                                             constraints,
                                                                             wcs_params) for i in inputs)

    return ranks_one_parameter_run

def one_parameter_run(i=None, params=None, simulation_params=None, beam_search_params=None, model_params=None, constraints=None, wcs_params=None):

    print(i)
    
    result_ranks_one_rep = one_repetition(params=params, 
                                          simulation_params=simulation_params,
                                          beam_search_params=beam_search_params, 
                                          model_params=model_params,      
                                          constraints=constraints, wcs_params=wcs_params)
  
    return result_ranks_one_rep

def one_repetition(params=None, simulation_params=None, beam_search_params=None, model_params=None, constraints=None, wcs_params=None):

    # generate dataset
    dataset_ordered, attributes, descriptives, true_description = fes.generate_dataset(params=params, simulation_params=simulation_params)
    
    # analyze dataset
    result_emm, general_params, considered_subgroups = bs.beam_search(dataset=dataset_ordered, attributes=attributes, descriptives=descriptives, 
                                                                      model_params=model_params, beam_search_params=beam_search_params, 
                                                                      wcs_params=wcs_params, constraints=constraints)

    #print(result_emm)
    #print(general_params)
    #print(considered_subgroups)
    #print(result_emm.shape)

    # process result
    result = fes.process_result(result_emm=result_emm, true_description=true_description)
    result['gen'] = general_params['params'].loc[1,model_params['trend_var']]    
    #print(result)

    return result

# run experiment
'''
experiment(simulation_params = {'trend_name': 'y', 'distances': [1,2,3], 'sds': [1,2,3],
                                'N': 10000, 'ncovs': 10, 'p': 0.5, 'ds': [1,2,3,4], 'tp': 10},
           beam_search_params = {'b': 8, 'w': 20, 'd': 5, 'q': 20},
           model_params = {'trend_var': 'mean', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
           constraints = {'min_size': 0.05, 'min_occassions': 1.0},
           wcs_params = {'gamma': 0.9, 'stop_desc_sel': 40},
           nreps=50)
''' 
experiment(simulation_params = {'trend_name': 'y', 'distances': [1,2,3], 'sds': [1,2,3],
                                'N': 10000, 'ncovs': 10, 'p': 0.5, 'ds': [1, 2,3,4], 'tp': 10},
           beam_search_params = {'b': 8, 'w': 20, 'd': 5, 'q': 20},
           model_params = {'trend_var': 'mean', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
           constraints = {'min_size': 0.05, 'min_occassions': 1.0},
           wcs_params = {'gamma': 0.9, 'stop_desc_sel': 40},
           nreps=50)


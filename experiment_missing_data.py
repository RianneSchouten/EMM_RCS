import numpy as np
import pandas as pd

import preprocess as pp
import beam_search as bs

def experiment(data_name=None, trend_name=None):

    dataset, attributes, descriptives = pp.preprocess(data_name=data_name, trend_name=trend_name)
    print(descriptives)
    print(attributes)
    print(dataset.dtypes)

    print(dataset.tail())


    beam_search_params = {'b': 8, 'w': 20, 'd': 3, 'q': 20} # 20 descriptive attributes
    model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'}
    constraints = {'min_size': 0.1, 'min_occassions': 0.7}
    wcs_params = {'gamma': 0.9, 'stop_desc_sel': 40} # two times the beam width

    result_emm, general_params, considered_subgroups = bs.beam_search(dataset=dataset, attributes=attributes, descriptives=descriptives, 
                                                                      model_params=model_params, beam_search_params=beam_search_params, 
                                                                      wcs_params=wcs_params, constraints=constraints)

    print(result_emm)
    print(general_params)
    print(considered_subgroups)

    # saving

    data_output_location = './data_output/MissingDataExperiments/' + trend_name + '_' + \
        str(list(beam_search_params.values())) + '_' + str(list(constraints.values())) + '_' + \
            str(list(wcs_params.values())) + '_' + \
                str(list(model_params.values())) + '.xlsx'

    beam_search_params.update(constraints)
    beam_search_params.update(wcs_params)
    beam_search_params.update(model_params)
    analysis_info = pd.DataFrame(beam_search_params, index=[0])
    general_params_pd = general_params['params']
    dfs = {'result_emm': result_emm, 'analysis_info': analysis_info, 
           'considered_subgroups': pd.DataFrame(considered_subgroups), 
           'general_params_pd': general_params_pd}
    
    writer = pd.ExcelWriter(data_output_location, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.save()    

    return 10

#experiment(data_name='MissingDataExperiments', trend_name='Brexit_short.sav')

experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.9_MNAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.7_MNAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.5_MNAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.3_MNAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.1_MNAR.sav')

experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.9_MAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.7_MAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.5_MAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.3_MAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.1_MAR.sav')

experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.9_MCAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.7_MCAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.5_MCAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.3_MCAR.sav')
experiment(data_name='MissingDataExperiments', trend_name='Brexit_0.1_MCAR.sav')
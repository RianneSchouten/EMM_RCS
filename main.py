import numpy as np
import pandas as pd

import analysis as an

def main(data_name=None, trend_name=None, qm=None, 
         beam_search_params=None, model_params=None,
         constraints=None, wcs_params=None,
         dfd_params=None, date=None,
         save_location=None):

    # location of dfd
    data_output_location = save_location + data_name + '/' + trend_name + '/' + str(date) + '_' + str(qm) + '_' + \
        str(list(beam_search_params.values())) + '_' + str(list(constraints.values())) + '_' + \
            str(list(dfd_params.values())) + '_' + str(list(wcs_params.values())) + '_' + \
                str(list(model_params.values())) + '.xlsx'

    # result_analysis is a df
    print(beam_search_params)
    result_emm, general_params, considered_subgroups, distribution_params = an.analysis(data_name=data_name,
                                                                                        trend_name=trend_name,
                                                                                        model_params=model_params,
                                                                                        beam_search_params=beam_search_params, 
                                                                                        constraints=constraints,
                                                                                        dfd_params=dfd_params, 
                                                                                        wcs_params=wcs_params)

    print(result_emm)
    print(general_params)
    print(considered_subgroups)

    # save        
    beam_search_params.update(dfd_params)
    beam_search_params.update(constraints)
    beam_search_params.update(wcs_params)
    beam_search_params.update(model_params)
    beam_search_params.update({'date': date})
    analysis_info = pd.DataFrame(beam_search_params, index=[0])
    general_params_pd = general_params['params']
    dfs = {'result_emm': result_emm, 'analysis_info': analysis_info, 
           'considered_subgroups': pd.DataFrame(considered_subgroups), 
           'general_params_pd': general_params_pd, 
           'distribution_params': pd.DataFrame(distribution_params)}
    
    writer = pd.ExcelWriter(data_output_location, engine='xlsxwriter')
    for sheet_name in dfs.keys():
        dfs[sheet_name].to_excel(writer, sheet_name=sheet_name, index=True)
    writer.save()    

if __name__ == '__main__':

    # current options for trend_var: prev, prev_slope, mov_prev, mov_prev_slope, mean, ratio
    # current options for hypothesis: data, value
    # current options for value: any value in combination with hypothesis: value
    # current options for use_se (if hypothesis = value): True, False, 'multiply'
    # current options for qm: max, count, average, sum, min
    # current options for threshold: any value (<) in combination with qm: count

    '''
    #### HBSC and DNSSSU
    # results not presented in manuscript
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, # 20 descriptive attributes
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 1.0},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210605, 
         save_location='./data_output/')

    # Fig 1
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20},
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210605, 
         save_location='./data_output/')

    # Fig 2
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': False, 'qm': 'count', 'threshold': 0.01, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210605, 
         save_location='./data_output/')

    # higher threshold
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': False, 'qm': 'count', 'threshold': 0.05, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210605, 
         save_location='./data_output/')

    # Fig 3 (not shown in paper)
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': 'multiply', 'qm': 'count', 'threshold': 1, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210606, 
         save_location='./data_output/')

    # higher threshold
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': 'multiply', 'qm': 'count', 'threshold': 0.5, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210606, 
         save_location='./data_output/')

    # Other runs
    # qm sum gives only trends that are overall close to 0 (girls)
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': 'multiply', 'qm': 'sum', 'threshold': None, 'order': 'min'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'make': False, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210606, 
         save_location='./data_output/')

    # qm min gives trends with at least one horizontal slope, is not exceptional 
    main(data_name='HBSC_DNSSSU', 
         trend_name='MPALC', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 20}, 
         model_params = {'trend_var': 'mov_prev_slope', 'hypothesis': 'value', 'value': 0.0, 'use_se': 'multiply', 'qm': 'min', 'threshold': None, 'order': 'min'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.78},
         dfd_params = {'False': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210606, 
         save_location='./data_output/')   
    ''' 
    '''
    #### Eurobarometer
    # Fig 1
    main(data_name='Eurobarometer', 
         trend_name='euspeed1num', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 25}, # 40 descriptive attributes
         model_params = {'trend_var': 'mean', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.5},
         dfd_params = {'make': True, 'm': 20},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210608, 
         save_location='./data_output/')
    
    # Fig 2
    main(data_name='Eurobarometer', 
         trend_name='euspeed1num', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 25}, # 40 descriptive attributes
         model_params = {'trend_var': 'mean', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'average', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.5},
         dfd_params = {'make': True, 'm': 20},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210608, 
         save_location='./data_output/')

    # another trend variable, not shown in manuscript
    main(data_name='Eurobarometer', 
         trend_name='lrsnum',
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 25}, # 40 descriptive attributes
         model_params = {'trend_var': 'mean', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.5},
         dfd_params = {'make': True, 'm': 20},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210608, 
         save_location='./data_output/')
  
    # another trend variable, not shown in manuscript
    main(data_name='Eurobarometer', 
         trend_name='lrsnum', 
         beam_search_params = {'b': 8, 'w': 40, 'd': 3, 'q': 25}, # 40 descriptive attributes
         model_params = {'trend_var': 'mean', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'average', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.05, 'min_occassions': 0.5},
         dfd_params = {'make': True, 'm': 20},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 80}, # two times the beam width
         date=20210608, 
         save_location='./data_output/')
    '''
    '''
    #### Brexit
    # Fig 1
    main(data_name='Brexit', 
         trend_name='Leaver_with', 
         beam_search_params = {'b': 8, 'w': 20, 'd': 3, 'q': 20}, # 20 descriptive attributes
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.1, 'min_occassions': 0.7},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 40}, # two times the beam width
         date=20210606, 
         save_location='./data_output/')

    # Fig 2
    main(data_name='Brexit', 
         trend_name='Leaver_with', 
         beam_search_params = {'b': 8, 'w': 20, 'd': 3, 'q': 20}, # 20 descriptive attributes
         model_params = {'trend_var': 'prev_slope', 'hypothesis': 'value', 'value': 0, 'use_se': True, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.1, 'min_occassions': 0.7},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 40}, # two times the beam width
         date=20210606, 
         save_location='./data_output/')

    # data without 3 variables
    # prev, not shown in manuscript
    main(data_name='Brexit', 
         trend_name='Leaver_without', 
         beam_search_params = {'b': 8, 'w': 20, 'd': 3, 'q': 20}, # 20 descriptive attributes
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.1, 'min_occassions': 0.7},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 40}, # two times the beam width
         date=20210607, 
         save_location='./data_output/')

    # prev_slope, not shown in manuscript
    main(data_name='Brexit', 
         trend_name='Leaver_without', 
         beam_search_params = {'b': 8, 'w': 20, 'd': 3, 'q': 20}, # 20 descriptive attributes
         model_params = {'trend_var': 'prev_slope', 'hypothesis': 'value', 'value': 0, 'use_se': True, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.1, 'min_occassions': 0.7},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 40}, # two times the beam width
         date=20210607, 
         save_location='./data_output/')
    '''
    '''
    # method can be repeated for trend variable 'remainer'
    # not shown in manuscript
    main(data_name='Brexit', 
         trend_name='Remainer', 
         beam_search_params = {'b': 8, 'w': 20, 'd': 3, 'q': 20}, # 20 descriptive attributes
         model_params = {'trend_var': 'prev', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.1, 'min_occassions': 0.7},
         dfd_params = {'make': True, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 40}, # two times the beam width
         date=20210605, 
         save_location='./data_output/')

    # ratio estimator needs non-correlated attributes
    # these attributes are too correlated
    # results not shown in manuscript
    main(data_name='Brexit', 
         trend_name='Remainer_plus_Leaver', 
         beam_search_params = {'b': 8, 'w': 20, 'd': 3, 'q': 20}, # 20 descriptive attributes
         model_params = {'trend_var': 'ratio', 'hypothesis': 'data', 'value': None, 'use_se': None, 'qm': 'max', 'threshold': None, 'order': 'max'},
         constraints = {'min_size': 0.1, 'min_occassions': 0.7},
         dfd_params = {'make': False, 'm': 100},
         wcs_params = {'gamma': 0.9, 'stop_desc_sel': 40}, # two times the beam width
         date=20210606, 
         save_location='./data_output/')
    '''
import numpy as np
import pandas as pd

import preprocess as pp
import collect_qualities as qu
import select_subgroup as ss

def import_subgroup_from_resultlist(data_name=None, trend_name=None, file_name=None, subgroup_numbers=None):

    dataset, attributes, descriptives = pp.preprocess(data_name=data_name, trend_name=trend_name)
    result_emm, analysis_info, considered_subgroups, general_params_pd, distribution_params = \
        load_result_emm(file_name=data_name + '/' + trend_name + '/' + file_name + '.xlsx')
    data_size = np.sum(general_params_pd['n'].values) 

    result_emm = result_emm.iloc[:,1:]
    general_params_params = general_params_pd.set_index(attributes['time_attribute'])

    sgn = subgroup_numbers[0]        
    sg = result_emm.loc[result_emm.sg == sgn, ]
    desc_series = sg.iloc[0,].dropna().drop(['sg'])
    desc_dict = desc_series.apply(eval).to_dict()

    subgroup, idx, subgroup_compl, idx2 = ss.select_subgroup(description=desc_dict, df=dataset, descriptives=descriptives)

    model_params = {'trend_var': analysis_info.loc[0, 'trend_var']} 
    general_params = {'params': general_params_params}

    #subgroup_params, is_replaced = qu.calculate_subgroup_parameters(subgroup=subgroup, attributes=attributes)
    subgroup_params = qu.calculate_first_part_subgroup_parameters(subgroup=subgroup, attributes=attributes, 
                                                                  model_params=model_params, general_params=general_params)
    subgroup_params = qu.calculate_second_part_subgroup_parameters(subgroup_params=subgroup_params, subgroup=subgroup, attributes=attributes, model_params=model_params)                                    
    
    params = subgroup_params['params']
    params['size'] = np.repeat(subgroup_params['sg_size'] / data_size, len(general_params_params))
    all_params = params

    if len(subgroup_numbers) > 1:        
        for sgn in subgroup_numbers[1:]:

            #print(sgn)

            sg = result_emm.loc[result_emm.sg == sgn, ]
            desc_series = sg.iloc[0, ].dropna().drop(['sg'])
            desc_dict = desc_series.apply(eval).to_dict()

            subgroup, idx, subgroup_compl, idx2 = ss.select_subgroup(description=desc_dict, df=dataset, descriptives=descriptives)
            subgroup_params_more = qu.calculate_first_part_subgroup_parameters(subgroup=subgroup, attributes=attributes, 
                                                                               model_params=model_params, general_params=general_params)
            subgroup_params_more = qu.calculate_second_part_subgroup_parameters(subgroup_params=subgroup_params_more, subgroup=subgroup, attributes=attributes, model_params=model_params)   

            params = subgroup_params_more['params']
            params['size'] = np.repeat(subgroup_params_more['sg_size'] / data_size, len(general_params_params))
            all_params = all_params.append(params)

    all_params['subgroup'] = np.repeat(subgroup_numbers, len(general_params_params))
    all_params[attributes['time_attribute'][0]] = all_params.index

    return general_params_pd, all_params

def load_result_emm(file_name=None):

    location = 'C:/Users/20200059/Documents/Github/EMM_RCS/data_output/' + file_name
    sheets = pd.read_excel(location, sheet_name=['result_emm', 'analysis_info', 'considered_subgroups', 'general_params_pd', 'distribution_params'])

    result_emm = sheets['result_emm']
    analysis_info = sheets['analysis_info']
    considered_subgroups = sheets['considered_subgroups']
    general_params_pd = sheets['general_params_pd']
    distribution_params = sheets['distribution_params']

    return result_emm, analysis_info, considered_subgroups, general_params_pd, distribution_params 

'''
general_params_pd, all_params = import_subgroup_from_resultlist(data_name="HBSC_DNSSSU",
                                                                trend_name="MPALC",
                                                                file_name="20210602_None_[8, 20, 2, 20]_[0.05, 0.78]_[False, 2]_[0.9, 40]_['mov_prev_slope', 'data', None, None, 'max', None]", 
                                                                subgroup_numbers=np.arange(14))

general_params, all_params = import_subgroup_from_resultlist(data_name="Eurobarometer",
                                                                trend_name="euspeed1num",
                                                                file_name="20210602_None_[8, 10, 2, 20]_[0.05, 0.5]_[False, 2]_[0.9, 20]_['mean', 'data', None, None, 'max', None]", 
                                                                subgroup_numbers=np.arange(10))

print(general_params)
print(all_params)
'''

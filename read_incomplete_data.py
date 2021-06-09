import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype

def load_and_preprocess(trend_name=None):

    data = load(trend_name=trend_name)
    dataset, attributes, descriptives = define_attributes(data=data, trend_name='MissingDataExperiments', skip_attributes=['Remainer'], outcome_attribute=['Leaver'])
    #dataset, descriptives = missing_data_method(dataset=dataset, descriptives=descriptives)
    finished_dataset = reset_attribute_type(dataset=dataset, descriptives=descriptives)

    return finished_dataset, attributes, descriptives

def load(trend_name=None):

    location = 'data_input/Brexit/MissingDataExperiments/' + trend_name
    dataset = pd.read_csv(location)

    print(dataset.head())
    print(dataset.dtypes)
    print(dataset.shape)
    print(dataset.isnull().sum())

    return dataset

def define_attributes(data=None, trend_name=None, skip_attributes=None, outcome_attribute=None):

    time_attribute = ['Wave']
    #outcome_attribute = ['euspeed1num']

    data_sorted = data.sort_values(['Wave'], ascending=[True]).reset_index(drop=True)
    data_sorted['id'] = np.arange(len(data_sorted))

    id_attribute = ['id']      
    #print(data_sorted.dtypes)

    num_atts = ['age', 'Tradeimmig']
    bin_atts = ['sex']

    if trend_name in ['Leaver_with', 'Remainer', 'Remainer_plus_Leaver', 'MissingDataExperiments']:
        nom_atts = ['Hindsight', 'work_stat', 'work_organisation', 'work_type', 'region', 'EURef2016']
        ord_atts = ['Poscountry', 'Posind', 'Govthand', 'profile_gross_personal', 'education_age', 'socialgradeCIE2']
    elif trend_name in ['Leaver_without']:
        nom_atts = ['work_stat', 'work_organisation', 'work_type', 'region', 'EURef2016']
        ord_atts = ['Govthand', 'profile_gross_personal', 'education_age', 'socialgradeCIE2']

    skip_attributes_temp = []
    if not skip_attributes is None:
       for var in skip_attributes:
            skip_attributes_temp.append(var)
            if var in ord_atts:
                ord_atts.remove(var)
    skip_attributes = skip_attributes_temp

    #print(ord_atts)
    #print(skip_attributes)

    dataset = data_sorted.drop(skip_attributes, axis=1)   

    descriptives = {'num_atts': num_atts, 'bin_atts': bin_atts, 'nom_atts': nom_atts, 'ord_atts': ord_atts}
    attributes = {'time_attribute': time_attribute, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'outcome_attribute': outcome_attribute}

    return dataset, attributes, descriptives

def missing_data_method(dataset=None, descriptives=None):

    print(dataset.shape)
    #print(dataset.head(20))
    print(dataset.isnull().sum())      

    # drop variables with more than 50% missing values
    #perc_missing = dataset.isnull().sum() / len(dataset)
    #drop_vars = perc_missing[perc_missing > 0.5].index.values
    #print(drop_vars)  
    #print(len(drop_vars))
    #smaller_dataset = dataset.drop(columns=drop_vars)
    smaller_dataset = dataset.copy()
    print(smaller_dataset.shape)

    # drop those variables from attributes
    bin_atts = descriptives['bin_atts']
    nom_atts = descriptives['nom_atts']
    ord_atts = descriptives['ord_atts']
    for var in drop_vars:
        if var in bin_atts:
            bin_atts.remove(var)
        elif var in nom_atts:
            nom_atts.remove(var)
        elif var in ord_atts:
            ord_atts.remove(var)     
    descriptives['bin_atts'] = bin_atts
    descriptives['nom_atts'] = nom_atts
    descriptives['ord_atts'] = ord_atts
    print(descriptives)

    new_dataset = smaller_dataset.copy()
    data_sorted = new_dataset.sort_values(['Wave'], ascending=[True]).reset_index(drop=True)
    #print(data_sorted.tail())

    return data_sorted, descriptives

def reset_attribute_type(dataset=None, descriptives=None):

    finished_dataset = dataset.copy()
    print(finished_dataset.dtypes)

    for var in descriptives['num_atts']:
        finished_dataset[var] = finished_dataset[var].astype(float)
    for var in descriptives['bin_atts']:
        finished_dataset[var] = finished_dataset[var].astype(object)
    for var in descriptives['nom_atts']:
        finished_dataset[var] = finished_dataset[var].astype(object)
    
    # process ordinal attributes one by one
    for var in descriptives['ord_atts']:

        print(var)
        finished_dataset[var]= finished_dataset[var].astype('category')

        if var == 'Govthand':
            #print(finished_dataset[var].cat.categories)
            new_order = [0,3,1,2,4]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)
        
        elif var == 'Posind':
            #print(finished_dataset[var].cat.categories)
            new_order = [0,4,2,1,3,5]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'Poscountry':
            #print(finished_dataset[var].cat.categories)
            new_order = [0,4,2,1,3,5]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)
        
        elif var == 'profile_gross_personal':
            #print(finished_dataset[var].cat.categories)
            new_order = [0,10,1,3,4,5,6,7,8,9,11,12,13,2]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'education_age':
            #print(finished_dataset[var].cat.categories)
            new_order = [6,7,0,1,2,5,4,3]#[2,3,4,5,6,7,0,1]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'socialgradeCIE2':
            #print(finished_dataset[var].cat.categories)
            new_order = [0,1,2,3,4,5]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

    print(finished_dataset.dtypes)
    for var in descriptives['ord_atts']:
        print(finished_dataset[var].cat.categories)
    for var in descriptives['nom_atts']:
        print(finished_dataset[var].unique())
    for var in descriptives['bin_atts']:
        print(finished_dataset[var].unique())

    data_sorted = finished_dataset.sort_values(['Wave'], ascending=[True]).reset_index(drop=True)
    data_sorted['id'] = np.arange(len(data_sorted))

    return data_sorted
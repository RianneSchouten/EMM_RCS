import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype

def load_and_preprocess(trend_name=None):

    data = load(trend_name=trend_name)
    dataset, attributes, descriptives = define_attributes(data=data, skip_attributes=['euspeed1', 'lrsnum'], outcome_attribute=['euspeed1num'])
    dataset, descriptives = missing_data_method(dataset=dataset, descriptives=descriptives)
    finished_dataset = reset_attribute_type(dataset=dataset, descriptives=descriptives)

    return finished_dataset, attributes, descriptives

def missing_data_method(dataset=None, descriptives=None):

    print(dataset.shape)
    #print(dataset.head(20))
    #print(dataset.isnull().sum())      

    # drop variables with more than 50% missing values
    perc_missing = dataset.isnull().sum() / len(dataset)
    drop_vars = perc_missing[perc_missing > 0.5].index.values
    #print(drop_vars) #71 
    print(len(drop_vars))
    smaller_dataset = dataset.drop(columns=drop_vars)
    #print(smaller_dataset.shape)

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
    #print(descriptives)

    # drop incomplete cases for age and sex, do not drop other cases
    new_dataset = smaller_dataset.copy()
    #print(new_dataset.isnull().sum())  
    new_dataset = new_dataset.dropna(how='any', axis=0, subset=['sex', 'age'])
    print(new_dataset.shape) 
    #print(new_dataset.isnull().sum())  

    data_sorted = new_dataset.sort_values(['eb'], ascending=[True]).reset_index(drop=True)
    #print(data_sorted.tail())

    return data_sorted, descriptives

def define_attributes(data=None, skip_attributes=None, outcome_attribute=None):

    time_attribute = ['eb']
    #outcome_attribute = ['euspeed1num']

    data_sorted = data.sort_values(['eb'], ascending=[True]).reset_index(drop=True)
    data_sorted['id'] = np.arange(len(data_sorted))

    id_attribute = ['id']      

    num_atts = ['age']
    bin_atts = ['benefit', 'comm', 'ecpres', 'epinfo', 'epimp2', 'epelfut', 'mepatt', 'eurogov', 'semmedia', 'trustep', 'trustec', 'trustcm', \
        'trustcj', 'trusteo', 'trustecb', 'trusteca', 'trustcr', 'trustsec', 'cpcultur', 'cpcurr', 'cpdatap', 'cpdrugs', 'cpeduc', 'cpenvir', \
        'cpforpol', 'cpimmigr', 'cpindust' , 'cppasyl', 'cppress', 'cpscien', 'cpsecur', 'cpthird', 'cpunemp', 'cpvatax', 'cpwelfar', 'cpworker', \
        'cpworsec', 'worldwar', 'efficacy', 'party', 'unionr', 'unionhh', 'hh', 'mhw', 'sex', 'mie']
    nom_atts = ['nation1', 'epimpf', 'feel', 'sochange', 'valpri1', 'valpri2', 'closepty', 'married', 'typecmty', 'religf1', 'religf2', 'tea']
    ord_atts = ['unifictn', 'membrshp', 'regret', 'commf', 'ecpresf', 'epinfof', 'epimp1', 'semhope', 'ecfinfo', 'ecint4', 'ecimp', 'citizen', 'satislfe', 'econpast', 'finapast', \
        'persuade', 'polint', 'newstv', 'newspap', 'newsrad', 'relimp', 'natpride', 'satisdmo', 'satisdeu', 'mvanm', 'mvanw', 'mvecol', 'mvnatur', \
        'poldisc', 'conflict', 'peaceful', 'better', 'happinss', 'underst', 'semgood', 'ecint3', 'particip', 'educ', 'educrec', 'sizehh', 'children', 'childold', 'childyng', \
        'churchat', 'mediause', 'oli', 'scmi', 'lrs', 'euspeed1']

    skip_attributes_temp = ['year']
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

def load(trend_name=None):

    name_dataset = 'ZA3521_v2-0-1_' + trend_name
    location = 'data_input/Eurobarometer/' + name_dataset + '.sav'

    dataset = pd.read_spss(location)

    return dataset

def reset_attribute_type(dataset=None, descriptives=None):

    finished_dataset = dataset.copy()
    #print(finished_dataset.dtypes)

    finished_dataset['age'] = finished_dataset['age'].astype(float)
    for var in descriptives['bin_atts']:
        finished_dataset[var] = finished_dataset[var].astype(object)
    for var in descriptives['nom_atts']:
        finished_dataset[var] = finished_dataset[var].astype(object)

    print(descriptives['ord_atts'])
    
    # process ordinal attributes one by one
    for var in descriptives['ord_atts']:

        if var == 'membrshp':
            #print(finished_dataset[var].cat.categories)
            new_order = [0,2,1]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'epimp1':
            #print(finished_dataset[var].cat.categories)
            new_order = [1,2,0,3]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'satislfe':
            #print(finished_dataset[var].cat.categories)
            new_order = [1,2,0,3]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'persuade':
            #print(finished_dataset[var].cat.categories)
            new_order = [1,3,0,2]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'newstv':
            #print(finished_dataset[var].cat.categories)
            new_order = [3,2,0,4,1]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'newspap':
            #print(finished_dataset[var].cat.categories)
            new_order = [3,2,0,4,1]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'newsrad':
            #print(finished_dataset[var].cat.categories)
            new_order = [3,2,0,4,1]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'satisdmo':
            #print(finished_dataset[var].cat.categories)
            new_order = [1,2,0,3]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'poldisc':
            #print(finished_dataset[var].cat.categories)
            new_order = [1,2,0]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'educ':
            #print(finished_dataset[var].cat.categories)
            new_order = [9,0,1,2,3,4,5,6,7,8]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'sizehh':
            #print(finished_dataset[var].cat.categories)
            new_order = [4,8,7,2,1,6,5,0,3]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'children':
            #print(finished_dataset[var].cat.categories)
            new_order = [4,5,9,8,2,1,7,6,0,3]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'mediause':
            #print(finished_dataset[var].cat.categories)
            new_order = [3,1,0,2]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'oli':
            #print(finished_dataset[var].cat.categories)
            new_order = [1,3,2,0]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'lrs':
            #print(finished_dataset[var].cat.categories)
            new_order = [8,0,1,2,3,4,5,6,7,9]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)
            #print(finished_dataset[var].cat.categories)

        elif var == 'euspeed1':
            #print(finished_dataset[var].cat.categories)
            new_order = [6,0,1,2,3,4,5]
            cat_type = CategoricalDtype(categories=[list(finished_dataset[var].cat.categories)[i] for i in new_order], ordered=True)
            finished_dataset[var] = finished_dataset[var].astype(cat_type)

    #print(finished_dataset.dtypes)

    '''
    print(finished_dataset.dtypes)
    for var in descriptives['ord_atts']:
        print(finished_dataset[var].cat.categories)
    for var in descriptives['nom_atts']:
        print(finished_dataset[var].unique())
    for var in descriptives['bin_atts']:
        print(finished_dataset[var].unique())
    '''

    return finished_dataset
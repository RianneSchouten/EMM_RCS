import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype

def load_and_preprocess(trend_name=None):

    data = load(trend_name=trend_name)
    dataset, attributes, descriptives = define_attributes(data=data)

    return dataset, attributes, descriptives

def define_attributes(data=None):

    time_attribute = ['meting']
    outcome_attribute = ['mpalc']

    data_sorted = data.sort_values(['meting'], ascending=[True]).reset_index(drop=True)
    data_sorted['id'] = np.arange(len(data_sorted))

    id_attribute = ['id']
    skip_attributes = []

    dataset = data_sorted.drop(skip_attributes, axis=1)         

    num_atts = ['lft', 'cijferleven']
    bin_atts = ['sekse', 'vollgezin']
    nom_atts = ['etngroep3', 'vaderbaan', 'moederbaan']
    ord_atts = ['schnivo', 'leerjaar', 'stedgem', 'spijbel']

    descriptives = {'num_atts': num_atts, 'bin_atts': bin_atts, 'nom_atts': nom_atts, 'ord_atts': ord_atts}

    attributes = {'time_attribute': time_attribute, 'skip_attributes': skip_attributes,
                  'id_attribute': id_attribute, 'outcome_attribute': outcome_attribute}

    return dataset, attributes, descriptives

def load(trend_name=None):

    name_dataset = 'PeilHBSC20032019_' + trend_name + '_70'
    location = 'C:/Users/20200059/Documents/Projects/ContextSpecificEffectsHBSC/Analysis/Data/' + name_dataset + '.sav'

    dataset = pd.read_spss(location)
    #print(dataset.shape)
    #print(data.head(20))
    #print(data.isnull().sum())     
    #print(dataset.dtypes) 

    # prepare right type per variable
    new_order_schnivo = [1,2,0,3]
    cat_type_schnivo = CategoricalDtype(categories=[list(dataset['schnivo'].cat.categories)[i] for i in new_order_schnivo], ordered=True)
    dataset['schnivo'] = dataset['schnivo'].astype(cat_type_schnivo)

    cat_type_leerjaar = CategoricalDtype(categories=[1.0, 2.0, 3.0, 4.0], ordered=True)
    dataset['leerjaar'] = dataset['leerjaar'].astype(cat_type_leerjaar)

    new_order_stedgem = [1,3,0,2,4]
    cat_type_stedgem = CategoricalDtype(categories=[list(dataset['stedgem'].cat.categories)[i] for i in new_order_stedgem], ordered=True)
    dataset['stedgem'] = dataset['stedgem'].astype(cat_type_stedgem)

    new_order_spijbel = []
    cat_type_spijbel = CategoricalDtype(categories=list(dataset['spijbel'].cat.categories), ordered=True)
    dataset['spijbel'] = dataset['spijbel'].astype(cat_type_spijbel)

    dataset['sekse'] = dataset['sekse'].astype(object)
    dataset['vollgezin'] = dataset['vollgezin'].astype(object)
    dataset['etngroep3'] = dataset['etngroep3'].astype(object)
    dataset['vaderbaan'] = dataset['vaderbaan'].astype(object)
    dataset['moederbaan'] = dataset['moederbaan'].astype(object)   

    return dataset
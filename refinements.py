import numpy as np
import itertools as it

def create_starting_descriptions(dataset=None, descriptives=None, b=None):

    cq_bin = refine_binary_attributes(seed=None, dataset=dataset, subgroup=None, binary_attributes=descriptives['bin_atts'])    
    
    cq_bin_nom = refine_nominal_attributes(cq=cq_bin, seed=None, dataset=dataset, subgroup=None, 
                                            nominal_attributes=descriptives['nom_atts'])
    
    cq_bin_nom_num = refine_numerical_attributes(cq=cq_bin_nom, seed=None, dataset=dataset, subgroup=None, 
                                                 numerical_attributes=descriptives['num_atts'], b=b)

    cq_bin_nom_num_ord = refine_ordinal_attributes(cq=cq_bin_nom_num, seed=None, dataset=dataset, subgroup=None, 
                                                   ordinal_attributes=descriptives['ord_atts'])

    return cq_bin_nom_num_ord

def refine_seed(seed=None, subgroup=None, descriptives=None, b=None):

    cq_bin = refine_binary_attributes(seed=seed, dataset=None, subgroup=subgroup, binary_attributes=descriptives['bin_atts'])

    cq_bin_nom = refine_nominal_attributes(cq=cq_bin, seed=seed, dataset=None, subgroup=subgroup, 
                                           nominal_attributes=descriptives['nom_atts'])
    
    cq_bin_nom_num = refine_numerical_attributes(cq=cq_bin_nom, seed=seed, dataset=None, subgroup=subgroup, 
                                                 numerical_attributes=descriptives['num_atts'], b=b)

    cq_bin_nom_num_ord = refine_ordinal_attributes(cq=cq_bin_nom_num, seed=seed, dataset=None, subgroup=subgroup, 
                                                   ordinal_attributes=descriptives['ord_atts'])
 
    return cq_bin_nom_num_ord

def refine_numerical_attributes(cq=None, seed=None, dataset=None, subgroup=None, numerical_attributes=None, b=None):

    refined_cq = cq

    quantiles = np.linspace(0, 1, b+1)[1:-1] # for 4 quantiles, this results in 0.25, 0.5, 0.75
    
    # first candidate queue
    if seed is None:
        for attribute in numerical_attributes:

            if any(dataset[attribute].isnull()):
                refined_cq.append({'description' : {attribute : ['NaN']}})
            
            values = dataset.loc[dataset[attribute].notnull(),attribute]
            #values = dataset[attribute]

            # continue with quantile split
            min_value = values.quantile(0.0) 
            max_value = values.quantile(1.0)
              
            for i in range(b-1):
                value = values.quantile(quantiles[i], interpolation='linear')

                refined_cq.append({'description' : {attribute : (min_value, value)}})
                refined_cq.append({'description' : {attribute : (value, max_value)}})       

    # refinements for existing candidate queue
    else:    
        description = seed['description']        
        for attribute in numerical_attributes:

            if any(subgroup[attribute].isnull()):
                temp_desc = description.copy()
                temp_desc[attribute] = ['NaN']
                refined_cq.append({'description' : temp_desc})
            
            values = subgroup.loc[subgroup[attribute].notnull(),attribute]
            
            # continue with quantile split
            # only if there are real numbers left in the subgroup
            min_value = values.quantile(0.0) 
            max_value = values.quantile(1.0)
                
            for i in range(b-1):

                value = values.quantile(quantiles[i], interpolation='linear')

                temp_desc = description.copy()
                temp_desc[attribute] = (min_value, value) # this replaces the original boundaries for this attribute
                refined_cq.append({'description' : temp_desc})

                temp_desc_2 = description.copy()
                temp_desc_2[attribute] = (value, max_value) # this replaces the original boundaries for this attribute
                refined_cq.append({'description' : temp_desc_2})     

    return  refined_cq

def refine_nominal_attributes(cq=None, seed=None, dataset=None, subgroup=None, nominal_attributes=None):

    refined_cq = cq

    # first candidate queue
    if seed is None:

        for attribute in nominal_attributes:
            
            if any(dataset[attribute].isnull()):                
                refined_cq.append({'description' : {attribute : ['NaN']}})

            values = dataset.loc[dataset[attribute].notnull(),attribute].unique() 
            for i in range(len(values)):

                value = values[i]
                refined_cq.append({'description' : {attribute : (1.0, value)}}) # 1.0 indicates == this nominal value
                
                if attribute != 'nation1':
                    refined_cq.append({'description' : {attribute : (0.0, value)}}) # 0.0 indicates != this nominal value

        return refined_cq

    # refinements for existing candidate queue
    else:
        
        description = seed['description']

        for attribute in nominal_attributes:
            if not attribute in list(description.keys()):

                if any(subgroup[attribute].isnull()):                
                    temp_desc = description.copy()
                    temp_desc[attribute] = ['NaN']
                    refined_cq.append({'description' : temp_desc})

                values = subgroup.loc[subgroup[attribute].notnull(),attribute].unique() 
                for i in range(len(values)):

                    value = values[i]
                    tup1 = (1.0, value)
                    tup0 = (0.0, value)

                    temp_desc = description.copy()
                    temp_desc[attribute] = tup1
                    refined_cq.append({'description' : temp_desc})

                    if attribute != 'nation1':
                        temp_desc_2 = description.copy()
                        temp_desc_2[attribute] = tup0
                        refined_cq.append({'description' : temp_desc_2})
        
        return refined_cq

def refine_binary_attributes(seed=None, dataset=None, subgroup=None, binary_attributes=None):

    refined_cq = []

    # first candidate queue
    if seed is None:

        for attribute in binary_attributes:

            if any(dataset[attribute].isnull()):
                refined_cq.append({'description' : {attribute : ['NaN']}})
            
            values = dataset.loc[dataset[attribute].notnull(),attribute].unique() 
            refined_cq.append({'description' : {attribute : [values[0]]}})
            refined_cq.append({'description' : {attribute : [values[1]]}})

    # refinements for a seed
    else:
        
        description = seed['description']

        for attribute in binary_attributes:
            if not attribute in list(description.keys()):

                if any(subgroup[attribute].isnull()):
                    temp_desc = description.copy()
                    temp_desc[attribute] = ['NaN']
                    refined_cq.append({'description' : temp_desc})

                values = subgroup.loc[subgroup[attribute].notnull(),attribute].unique() 
                for i in range(len(values)):

                    value = values[i]
                    temp_desc = description.copy()
                    temp_desc[attribute] = [value]
                    refined_cq.append({'description' : temp_desc})

    return  refined_cq     

def refine_ordinal_attributes(cq=None, seed=None, dataset=None, subgroup=None, ordinal_attributes=None):

    refined_cq = cq

    # first candidate queue
    if seed is None:
        for attribute in ordinal_attributes:
           
            cat_values = dataset[attribute].cat.categories
            for i in range(len(cat_values)-1):
                
                refined_cq.append({'description' : {attribute : list(cat_values[0:i+1].values)}})
                refined_cq.append({'description' : {attribute : list(cat_values[i+1:].values)}})

            if any(dataset[attribute].isnull()):
                refined_cq.append({'description' : {attribute : ['NaN']}})               

    # refinements for existing candidate queue
    else:    
        description = seed['description']        
        for attribute in ordinal_attributes:

            if not attribute in list(description.keys()):

                if any(subgroup[attribute].isnull()):
                    temp_desc = description.copy()
                    temp_desc[attribute] = ['NaN']
                    refined_cq.append({'description' : temp_desc})  

                #unique_values = subgroup.loc[subgroup[attribute].notnull(),attribute].unique() 
                #cat_values = subgroup[attribute].cat.categories
                #values_to_use = [value for value in unique_values if value in cat_values]

                values_to_use = subgroup[attribute].cat.categories

                for i in range(len(values_to_use)-1):

                    temp_desc = description.copy()
                    temp_desc[attribute] = list(values_to_use[0:i+1]) # this replaces the original boundaries for this attribute
                    refined_cq.append({'description' : temp_desc})

                    temp_desc_2 = description.copy()
                    temp_desc_2[attribute] = list(values_to_use[i+1:]) # this replaces the original boundaries for this attribute
                    refined_cq.append({'description' : temp_desc_2})                  

    return  refined_cq
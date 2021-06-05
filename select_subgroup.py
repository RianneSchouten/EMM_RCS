import numpy as np
import pandas as pd

def select_subgroup(description=None, df=None, descriptives=None):

    pairs = list(description.items())

    num_atts = descriptives['num_atts']
    bin_atts = descriptives['bin_atts']
    nom_atts = descriptives['nom_atts']
    ord_atts = descriptives['ord_atts']

    if len(pairs) == 0:
        idx = []
    else: 
        # select all indices as a starting point
        idx = df.index.values

        for pair in pairs:

            att = pair[0]
            sel = pair[1]

            if att in bin_atts:
            
                idx = select_bin_att(idx=idx, att=att, sel=sel, df=df)
        
            elif att in num_atts:

                idx = select_num_att(idx=idx, att=att, sel=sel, df=df)

            elif att in nom_atts:

                idx = select_nom_att(idx=idx, att=att, sel=sel, df=df)

            elif att in ord_atts:

                idx = select_ord_att(idx=idx, att=att, sel=sel, df=df)
     
    all_idx = df.index.values
    idx_compl = np.setdiff1d(all_idx, idx)
    
    # this should be loc!!
    # make sure the dataset is sorted at the beginning of the algorithm
    subgroup = df.loc[idx]
    subgroup_compl = df.loc[idx_compl]

    #print(list(idx_sg))
    #print(list(idx_compl))

    return subgroup, list(idx), subgroup_compl, list(idx_compl)

def select_bin_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()

    if 'NaN' == sel[0]:
        sel_idx = df[df[att].isnull()].index.values
    else:
        sel_idx = df[df[att] == sel[0]].index.values

    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out

def select_num_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()

    if 'NaN' == sel[0]:
        sel_idx = df[df[att].isnull()].index.values
    else:
        low_idx =  df[df[att] >= sel[0]].index.values # value can be equal to the lower bound
        up_idx = df[df[att] <= sel[1]].index.values # value can be equal to the upper bound            
        sel_idx = np.intersect1d(low_idx, up_idx)
    
    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out

def select_nom_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()
    tup = sel

    if 'NaN' == sel[0]:
        sel_idx = df[df[att].isnull()].index.values
        idx_in = np.intersect1d(idx_in, sel_idx)
  
    # when the first value is a 1, then take all datapoints with the value in position two
    if tup[0] == 1.0:
        df_drop = df[df[att].notnull()]
        sel_idx = df_drop[df_drop[att] == tup[1]].index.values
        idx_in = np.intersect1d(idx_in, sel_idx)
        
    # when the first value is a 0, then take all datapoints that do not have the value in position two
    elif tup[0] == 0.0:
        df_drop = df[df[att].notnull()]
        sel_idx = df_drop[df_drop[att] != tup[1]].index.values
        idx_in = np.intersect1d(idx_in, sel_idx)

    idx_out = idx_in.copy()

    return idx_out    

def select_ord_att(idx=None, att=None, sel=None, df=None):

    idx_in = idx.copy()        

    if 'NaN' == sel[0]:
        sel_idx = df[df[att].isnull()].index.values
    else:
        # a loop over all categories in the description
        # cases that equal either of the categories should be selected
        sel_idx = df[df[att].isin(sel)].index.values

    idx_out = np.intersect1d(idx_in, sel_idx)

    return idx_out   
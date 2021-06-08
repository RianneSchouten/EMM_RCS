import numpy as np
import pandas as pd

import preprocess as pp
import beam_search as bs

def experiment(data_name=None, trend_name=None):

    dataset, attributes, descriptives = pp.preprocess(data_name=data_name, trend_name=trend_name)
    print(descriptives)
    print(attributes)
    print(dataset.dtypes)

    return 10

experiment(data_name='MissingDataExperiments', trend_name='Brexit_1_ha.sav')
#experiment(data_name='MissingDataExperiments', trend_name='Brexit_1_emp.sav')
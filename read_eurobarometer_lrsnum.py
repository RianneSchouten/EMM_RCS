import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype

import read_eurobarometer_euspeed1num as rebme

def load_and_preprocess(trend_name=None):

    data = rebme.load(trend_name=trend_name)
    dataset, attributes, descriptives = rebme.define_attributes(data=data, skip_attributes=['euspeed1num', 'lrs'], outcome_attribute=['lrsnum'])
    dataset, descriptives = rebme.missing_data_method(dataset=dataset, descriptives=descriptives)
    finished_dataset = rebme.reset_attribute_type(dataset=dataset, descriptives=descriptives)

    return finished_dataset, attributes, descriptives


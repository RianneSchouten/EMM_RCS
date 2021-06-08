import pandas as pd
import numpy as np
from pandas.api.types import CategoricalDtype
import read_brexit_remainer as rbr

def load_and_preprocess(trend_name=None):

    data = rbr.load(trend_name=trend_name)
    dataset, attributes, descriptives = rbr.define_attributes(data=data, trend_name=trend_name, skip_attributes=['Remainer'], outcome_attribute=['Leaver'])
    dataset, descriptives = rbr.missing_data_method(dataset=dataset, descriptives=descriptives)
    finished_dataset = rbr.reset_attribute_type(dataset=dataset, descriptives=descriptives)

    return finished_dataset, attributes, descriptives


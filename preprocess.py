import numpy as np
import pandas as pd

import read_hbsc_dnsssu_mpalc as rhdm
import read_eurobarometer_lrsnum as rebml
import read_eurobarometer_euspeed1num as rebme
import read_brexit_remainer as rbr
import read_brexit_remainer_plus_leaver as rbrpl
import read_brexit_leaver as rbl
import read_incomplete_data as rid

def preprocess(data_name=None, trend_name=None):

    if data_name == 'HBSC_DNSSSU':
        if trend_name == 'MPALC':
            dataset, attributes, descriptives = rhdm.load_and_preprocess(trend_name=trend_name)

    if data_name == 'Eurobarometer':
        if trend_name == 'lrsnum':
            dataset, attributes, descriptives = rebml.load_and_preprocess(trend_name=trend_name)
        if trend_name == 'euspeed1num':
            dataset, attributes, descriptives = rebme.load_and_preprocess(trend_name=trend_name)

    if data_name == 'Brexit':
        if trend_name == 'Remainer':
            dataset, attributes, descriptives = rbr.load_and_preprocess(trend_name=trend_name)
        if trend_name in ['Leaver_with', 'Leaver_without']:
            dataset, attributes, descriptives = rbl.load_and_preprocess(trend_name=trend_name)
        if trend_name == 'Remainer_plus_Leaver':
            dataset, attributes, descriptives = rbrpl.load_and_preprocess(trend_name=trend_name)

    if data_name == 'MissingDataExperiments':
        dataset, attributes, descriptives = rid.load_and_preprocess(trend_name=trend_name)

    return dataset, attributes, descriptives



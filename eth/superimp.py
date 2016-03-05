import warnings
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd

import pandas.io.data as web
import matplotlib.pyplot as plt
def superImpose():
    serdate='2015-1-1'
    sdate='2015-01-02'
    l=['^VIX', 'SPLK', 'SPY', 'DATA']
    for i in l:
        DT = web.DataReader(name=i, data_source='yahoo',
                     start=serdate)


        DT['CloseN'] = DT['Close']/DT['Close'][sdate]

        #DT['CloseN'].plot(figsize=(8, 5), grid=True)
        print DT['CloseN'].tail()

superImpose()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 16:46:49 2021

@author: seomara
"""

import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold

def delete_constants_variables(df,thrh,y):
    df2=df.drop([y],axis=1)
    constant_filter = VarianceThreshold(threshold=thrh)
    constant_filter.fit(df2)
    col=df2.columns[constant_filter.get_support()]
    col=np.delete(col, (0), axis=0).tolist()
    col.extend([y])
    return(df[col])
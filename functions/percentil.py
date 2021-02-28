#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:34:47 2021

@author: seomara
"""

def percentil(df,per):
    names=list(df)
    p=[]
    for i in names:
        p.append(np.percentile(df[i],per))
    return p
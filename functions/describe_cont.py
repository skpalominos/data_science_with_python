#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:35:07 2021

@author: seomara
"""

def describe_cont(df):
    df=df.select_dtypes(include='number')
    names=list(df)
    descript = pd.DataFrame({'Media': df.mean(),
                             'Mediana': df.median(),
                             'Q1': percentil(df,25),
                             'Q3': percentil(df,75),
                             'Minimo': df.min(),
                             'Maximo': df.max(),
                             'Kurtosis':scipy.stats.kurtosis(df),
                             'Skewness':scipy.stats.skew(df)},
                              index = names,
               columns=['Media','Mediana','Q1','Q3','Minimo','Maximo','Skewness','Kurtosis'])
    return descript
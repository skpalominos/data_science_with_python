#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:35:28 2021

@author: seomara
"""

def describe_categorica(df):
    df=df.select_dtypes(include='object')
    names=list(df)
    for i in names:
        tabla=pd.DataFrame(df.groupby(df[i])[i].count())
        tabla.columns=['N']
        tabla.reset_index(inplace=True)
        tabla=tabla.assign(Porcentaje = lambda x: x.N/(sum(x.N)))
        print(tabla)
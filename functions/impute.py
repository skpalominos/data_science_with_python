#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 15:33:44 2021

@author: seomara
"""

def impute(df):
    df = df.fillna(df.select_dtypes(include='number').median().iloc[0]) 
    df = df.fillna(df.select_dtypes(include='object').mode().iloc[0])
    return df
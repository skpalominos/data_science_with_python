#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 10:07:57 2021

@author: seomara
"""
import pandas as pd

def leer_csv(path,file_name):
    df = pd.read_csv(path+file_name)
    df.columns = df.columns.str.lower()
    return(df)
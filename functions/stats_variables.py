#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 14:19:01 2021

@author: seomara
"""

def stats_variables(df,vars,stat,group):
    for i in range(0,len(vars)):
        new_col = vars[i]+'_'+stat
        df[new_col] =  df[vars[i]].groupby(df[group]).transform(stat)
    return(df) 
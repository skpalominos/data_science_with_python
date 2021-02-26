#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 23:20:46 2021

@author: seomara
"""

def elevate_variables(df,vars,x):
    for i in range(0,len(vars)):
        quadratic_col = vars[i]+'_elevate_'+str(x)
        df[quadratic_col] = df[vars[i]]**x
    return(df) 
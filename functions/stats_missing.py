#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 21:26:02 2021

@author: seomara
"""

class stats_missing:
    def __init__(self,df,x):
        self.df = df
        self.x = x

    def n_null(self):
        return(self.df[[self.x]].isnull().sum())

    def per_null(self):
        return(self.df[[self.x]].isnull().sum() / self.df.shape[0] * 100)
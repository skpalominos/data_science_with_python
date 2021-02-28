#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 16:49:13 2021

@author: seomara
"""

def df_train_test(df,Y_name,downsampling=0.5,p_test=0.2):
    # test 
    nrow=df.shape[0]
    df['target'] = df[Y_name]
    test_index = random.sample(list(range(0,nrow+1)),math.floor(p_test*nrow))
    df_test = df.iloc[test_index,:]

    #train
    df_train = df.drop(test_index, axis=0)
    n1 = df_train['target'].sum()
    n0 = math.floor((n1*downsampling)/(1-downsampling))
    index0 = np.where(df_train['target']==0)[0]
    index1 = np.where(df_train['target']==1)[0]

    if (len(index0)>n0):
       index0 = random.sample(index0.tolist(),n0) 
    else:
         index0 = random.choices(index0.tolist(), k=n0)
    index0.extend(index1)
    df_train = df_train.iloc[index0,:]
    return(df_train,df_test)
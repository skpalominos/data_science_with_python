#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 14:24:30 2021

@author: seomara
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.metrics import roc_auc_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import roc_curve

def clasif_medida(value):
    if (value<=0.6):
        return('baja')
    if ((value>0.6)&(value<=0.7)):
        return('media')
    if (value>0.7):
        return('alta')

def KS(ytest,prob1):
    unos = ytest
    cant_unos = np.sum(unos)
    index_unos = np.argsort(prob1)[::-1]
    sort_unos = unos[index_unos]
    cum_unos = np.cumsum(sort_unos)
    cum_rate_unos = cum_unos/cant_unos
    n = ytest.shape[0]
    recta_lineal = np.arange(start = 1, stop = n+1, step = 1)/n
    recta_lineal
    prob0=1-prob1
    ceros = 1-ytest
    cant_ceros = np.sum(ceros)
    index_ceros = np.argsort(prob1)[::-1]
    sort_ceros = ceros[index_ceros]
    cum_ceros = np.cumsum(sort_ceros)
    cum_rate_ceros = cum_ceros/cant_ceros
    return(max(cum_rate_unos-cum_rate_ceros))

def fit_metrics(ytest,p_corte,prob,interpretacion):
    pred = ((prob  >= p_corte) * 1)
    fpr, tpr, umbral = roc_curve(ytest,prob)
    M = metrics.confusion_matrix(ytest,pred)
    tn, fp, fn, tp = M.ravel()
    accuracy = (tp+tn)/(tp+fp+fn+tn)
    precision = tp/(tp + fp)
    recall=tp/(tp + fn)
    met = pd.DataFrame({'Accuracy': [accuracy], 'Precision': [precision],'Recall': recall,'AUC': metrics.auc(fpr, tpr),'KS' :KS(ytest,prob)},index=['Estimacion'])
    if (interpretacion=='si'):
        print('Interpretacion:')
        print('- Considerando area bajo la curva de ROC, la probabilidad de clasificar correctamente a una observacion seleccionada al azar es igual a', np.around(metrics.auc(fpr, tpr),4),
         'lo que indica que el modelo tiene una capacidad discriminatoria',clasif_medida(metrics.auc(fpr, tpr)))
        print('- El modelo alcanza un valor del indice KS de',round(KS(ytest,prob),4),'lo que indica que el modelo tiene una capacidad predictiva',clasif_medida(KS(ytest,prob)),'respecto a la variable target class')
        print('- La proporcion predicha correctamente por el modelo o Accuracy toma el valor de',round(accuracy,4)) 
        print('- La proporcion de casos predichos por el modelo correctamente clasificados o Precision, es de',round(precision,4))
        print('- La proporcion de casos de interes correctamente clasificados por el modelo  o Recall es de',round(recall,4))
    return (met)

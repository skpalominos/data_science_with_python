#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 14:11:49 2021

@author: seomara
"""

from sklearn.metrics import precision_recall_curve
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import metrics


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

def Grafica_KS_PR(ytest,prob1):
    unos = ytest
    cant_unos = np.sum(unos)
    index_unos = np.argsort(prob1)[::-1]
    sort_unos = unos[index_unos]
    cum_unos = np.cumsum(sort_unos)
    cum_rate_unos = cum_unos/cant_unos
    n = ytest.shape[0]
    recta_lineal = np.arange(start = 1, stop = n+1, step = 1)/n
    prob0=1-prob1
    ceros = 1-ytest
    cant_ceros = np.sum(ceros)
    index_ceros = np.argsort(prob1)[::-1]
    sort_ceros = ceros[index_ceros]
    cum_ceros = np.cumsum(sort_ceros)
    cum_rate_ceros = cum_ceros/cant_ceros
    plt.style.use('ggplot')
    f = plt.figure(figsize=(7,3.5))
    ax = f.add_subplot(121)
    plt.title('Curva KS')
    plt.ylim([-0.05, 1.05])
    plt.xlim([-0.05, 1.05])
    plt.plot(recta_lineal,cum_rate_unos,'r--',color='blue')
    plt.plot(recta_lineal,cum_rate_ceros,'r--',color='green')
    plt.title('Curva KS')
    plt.legend(('Dist Acumulada Exitos','Dist Acumulada Fracasos'), loc = 'lower left')
    ax2 = f.add_subplot(122)
    precision, recall, _ = precision_recall_curve(ytest, prob1)
    plt.plot(recall, precision,'r--',color='rebeccapurple')
    plt.ylim([-0.05, 1.05])
    plt.xlim([-0.05, 1.05])
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    pres, rec, _ = metrics.precision_recall_curve(ytest, prob1)
    plt.legend(('Curva PR','Curva PR'), loc = 'lower left')
    plt.title('Curva PR ')
    plt.show()
    met = pd.DataFrame({'AUC PR': metrics.average_precision_score(ytest, prob1),'KS':KS(ytest,prob1)},index=['Estimacion'])
    return(met)
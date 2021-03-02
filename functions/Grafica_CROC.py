#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 13:55:47 2021

@author: seomara
"""

from sklearn.metrics import roc_curve

def Grafica_CROC(ytest,prob,p_corte,alpha):
    fpr, tpr, umbral = roc_curve(ytest,prob)
    f_fpr1= (1 - np.exp(-7*fpr))/(1-np.exp(-7))
    f_fpr2= (1 - np.exp(-alpha[0]*fpr))/(1-np.exp(-alpha[0]))
    f_fpr3= (1 - np.exp(-alpha[1]*fpr))/(1-np.exp(-alpha[1]))
    plt.style.use('ggplot')
    plt.plot(fpr, tpr,color='blue') 
    plt.plot(f_fpr1, tpr,'r--',color='red')
    plt.plot(f_fpr2, tpr,'r--',color='green') 
    plt.plot(f_fpr3, tpr,'r--',color='orange') 
    plt.plot([0, 1], [0, 1],'r--',color='rebeccapurple')
    plt.xlim([-0.05, 1.0])
    plt.ylim([0.0, 1.05])
    plt.title('Curva CROC')
    plt.legend(('Curva de ROC','Curva CROC alpha = 7','Curva CROC alpha = '+str(alpha[0]),'Curva CROC alpha = '+str(alpha[1])), loc = 'lower right')
    plt.show()

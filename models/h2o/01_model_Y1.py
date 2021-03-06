#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 15:28:33 2021

@author: seomara
"""
# Librerias ---------------------------------------------------------------

import pandas as pd
import csv
import numpy as np
import math as my
import matplotlib.pyplot as plt
import random
import math
from IPython.display import Image
from scipy import stats
from sklearn.feature_selection import VarianceThreshold
import h2o
from h2o.estimators.glm import H2OGeneralizedLinearEstimator
%matplotlib inline

# Leer funciones

import sys
sys.path.append('/Users/seomara/Documents/work/python/data_science_with_python/')
from functions.leer_csv import *
from functions.impute import *
from functions.delete_constant_variables import *
from functions.df_train_test import *
from functions.Grafica_CROC import *
from functions.Grafica_KS_PR import *
from functions.fit_metrics import *

# parametros

class param(): 
    path = '/Users/seomara/Documents/work/test/spike/files/'

p = param()

# Leer dataset  -----------------------------------------------------------

df_pred_M1 = leer_csv(p.path,"df_model1.csv")
df_pred_M1 = df_pred_M1.drop(['y12', 'camada_y12','date_y12', 'fecha','anno','flag'], axis=1)

# Def parametros modelamiento ---------------------------------------------

class param_fit(): 
      p_test = 0.2
      downsampling = 0.5  
      importancia = 0.95
    
param = param_fit()

# Downsampling ------------------------------------------------------------

df_train,df_test = df_train_test(df_pred_M1,'y1',param.downsampling,param.p_test)

# Sanity Check ------------------------------------------------------------

df_train['target'].mean()
df_test['target'].mean()

# -------------------------------------------------------------------------
# Modelo regularizado -----------------------------------------------------
# -------------------------------------------------------------------------

df_train = df_train.drop(['y1', 'camada_y1','nemotecnico_se','date_y1','date_x'], axis=1)
df_train=df_train.replace([np.inf, -np.inf], np.nan).dropna(axis=1)
df_train=delete_constants_variables(df_train,5,'target')
predictors=df_train.drop(['target'], axis=1).columns.tolist()

# importar h2o 

# Bases tran y test 
h2o.init(ip = "localhost",nthreads = -1,max_mem_size = "3g")
train = h2o.H2OFrame(df_train)
train['target'] = train['target'].asfactor()

df_test = df_test.drop(['y1', 'camada_y1','nemotecnico_se','date_y1','date_x'], axis=1)
df_test=df_test.replace([np.inf, -np.inf], np.nan).dropna(axis=1)
test = h2o.H2OFrame(df_test)
test['target'] = test['target'].asfactor()

# Regression Lasso

glm_reg = H2OGeneralizedLinearEstimator(
                     family = "binomial",
                     link   = "logit",
                     ignore_const_cols = True,
                     missing_values_handling = "Skip",
                     lambda_search = True,
                     solver = "AUTO",
                     alpha  = 1,
                     seed   = 123,
                     nfolds = 5,
                     fold_assignment = "Stratified",
                     keep_cross_validation_predictions = False,
                     model_id = "glm_reg")

glm_reg.train(y = 'target',
              x = predictors,
              training_frame = train)


# Filtrar variables que entran en el modelo 
variables = glm_reg.varimp(use_pandas=True)
variables['imp_cum'] = variables['percentage'].cumsum()
variables=variables.query('imp_cum<=@param.importancia')
variables=variables['variable'].tolist()

# -------------------------------------------------------------------------
# Modelo real  ------------------------------------------------------------
# -------------------------------------------------------------------------

# Modelo Real

model_glm = H2OGeneralizedLinearEstimator(family = 'binomial',link = "logit", model_id = 'reg_log')
model_glm.train(x = variables, y = 'target', training_frame = train, validation_frame=test)

#importancia predictores

importancia_predictores = model_glm.varimp(use_pandas=True)
importancia_predictores.head(10)

fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(6, 3.8))
importancia_predictores.head(10).plot.barh(x='variable', y='scaled_importance', ax=ax)
ax.invert_yaxis()
fig.suptitle('Importancia de los predictores (Top 10)', fontsize='large');

# -------------------------------------------------------------------------
# Metricas performance ----------------------------------------------------
# -------------------------------------------------------------------------

# Metricas h2o

performance_test = model_glm.model_performance(test_data = test)

print(f"auc: {performance_test.auc()}")
print(f"MSE: {performance_test.mse()}")
print(f"R2: {performance_test.r2()}")
print(f"Gini: {performance_test.gini()}")
print(f"AIC: {performance_test.aic()}")
print(f"LogLoss: {performance_test.logloss()}")

performance_test.plot(type='roc')

# Coeficientes 

coeficientes = model_glm._model_json['output']['coefficients_table'].as_data_frame()

# Otras metricas de perfomance

predicciones = model_glm.predict(test).as_data_frame()
df_test=test.as_data_frame()

# Grafica CROC
Grafica_CROC(df_test['target'],df_test['pred'],0.5,[10,5])

# Grafica Presicion Recall
Grafica_KS_PR(df_test['target'],df_test['pred'])

# Interpretacion de metricas
fit_metrics(df_test['target'],0.5,df_test['pred'],'si')












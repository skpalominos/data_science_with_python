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
import scipy
from datetime import date
from datetime import datetime, timedelta
import itertools
import matplotlib.pyplot as plt
from dateutil import rrule, parser
import random
import math
import pandas as pd
import numpy as np
import math as mt
import datetime as dt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import datasets
from IPython.display import Image
from sklearn import metrics
from scipy import stats
from sklearn.feature_selection import VarianceThreshold
%matplotlib inline

# Leer funciones

import sys
sys.path.append('/Users/seomara/Documents/work/python/data_science_with_python/')
from functions.leer_csv import *
from functions.impute import *
from functions.delete_constant_variables import *
from functions.df_train_test import *

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
import h2o
from h2o.estimators.glm import H2OGeneralizedLinearEstimator

# Regression Lasso
train = h2o.H2OFrame(df_train)
train['target'] = train['target'].asfactor()
glm_reg = H2OGeneralizedLinearEstimator(alpha=1,lambda_search=True,family = 'binomial', model_id = 'reg_lasso')
glm_reg.train(x = predictors, y = 'target', training_frame = train)

# Filtrar variables que entran en el modelo 
variables = glm_reg.varimp(use_pandas=True)
variables['imp_cum'] = variables['percentage'].cumsum()
variables=variables.query('imp_cum<=@param.importancia')
variables=variables['variable'].tolist()

# -------------------------------------------------------------------------
# Modelo real  ------------------------------------------------------------
# -------------------------------------------------------------------------

# Modelo Real
glm = H2OGeneralizedLinearEstimator(family = 'binomial', model_id = 'reg_log')
glm.train(x = variables, y = 'target', training_frame = train)

# -------------------------------------------------------------------------
# Metricas performance ----------------------------------------------------
# -------------------------------------------------------------------------











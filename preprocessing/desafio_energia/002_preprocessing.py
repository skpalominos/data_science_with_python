#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 09:39:43 2021

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
%matplotlib inline

# Leer funciones

import sys
sys.path.append('/Users/seomara/Documents/work/python/data_science_with_python/')
from functions.leer_csv import *

# parametros

class param(): 
    path = '/Users/seomara/Documents/work/test/spike/files/'

p = param()

# -------------------------------------------------------------------------
# P4 ----------------------------------------------------------------------
# -------------------------------------------------------------------------

# Leer dataset  -----------------------------------------------------------

df_pred = leer_csv(p.path,'base_para_prediccion.csv')

# Contruccion variables ---------------------------------------------------


df_pred['date_ymdh'] = df_pred['fecha'].apply(lambda x: x[:-13])
df_pred['date_ymdh'] = df_pred['date_ymdh'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
df_pred['date_ymdh']=[df_pred['date_ymdh'][i]+np.timedelta64(df_pred['hora'][i],'h') for i in range(0,df_pred.shape[0])]
df_pred['anno'] = df_pred['date_ymdh'].apply(lambda x: x.year)
df_pred['mes'] = df_pred['date_ymdh'].apply(lambda x: x.month)
df_pred['dia'] = df_pred['date_ymdh'].apply(lambda x: x.day)
df_pred['dia_semana'] = df_pred['date_ymdh'].apply(lambda x: x.weekday())
df_pred['weekend'] = df_pred['dia_semana'].apply(lambda x : 1 if (x in [6,7]) else 0)

# Creacion funcion grafica subestaciones  --------------------------------------------------------


def plot_time_series_sub_estation(dates,subestacion,variables,df=df_pred):
    df = df.query('fecha==@date & nemotecnico_se==@subestacion')
    df = df[['date_ymdh']+[variables]]
    df = df.set_index('date_ymdh')
    ax = df.plot(linewidth=2, fontsize=12)
    ax.set_xlabel('Date')
    ax.legend(fontsize=12)
    plt.xticks(rotation=90)

#  Grafica curva de generación solar --------------------------------------

list(map(plot_time_series_sub_estation,
         ["2019-01-10","2019-02-10","2019-02-10""2019-01-14"],
         itertools.repeat('SE005T002'),
         itertools.repeat('gen_solar_total_mwh')))

list(map(plot_time_series_sub_estation,
         ["2019-01-10","2019-02-10","2019-02-10""2019-01-14"],
         itertools.repeat('SE127T005'),
         itertools.repeat('gen_solar_total_mwh')))

# Grafica curva de generación térmica, ------------------------------------

list(map(plot_time_series_sub_estation,
         ["2019-05-14","2019-05-16","2019-05-17""2019-05-18"],
         itertools.repeat('SE020G213'),
         itertools.repeat('gen_termica_total_mwh')))

list(map(plot_time_series_sub_estation,
         ["2019-05-14","2019-05-16","2019-05-17""2019-05-18"],
         itertools.repeat('SE106G216'),
         itertools.repeat('gen_termica_total_mwh')))

# -------------------------------------------------------------------------
# P5 ----------------------------------------------------------------------
# -------------------------------------------------------------------------

# Crear flag --------------------------------------------------------------

df_pred['flag'] = df_pred['cmg_desv_pct'].apply(lambda x : 1 if (abs(x)>15) else 0)
#df_pred = df_pred.assign(flag = lambda x: np.nan if (np.isnan(x.cmg_real) or
#                                                     x.cmg_real==0 or
#                                                     np.isnan(x.cmg_prog) or 
#                                                     x.cmg_prog==0) else x.flag)
                         
# Completar fechas faltantes ----------------------------------------------

df_pred = df_pred.assign(original = lambda x: (1))
datesx = list(rrule.rrule(rrule.HOURLY, dtstart=parser.parse(min(df_pred.fecha)),
                          until=parser.parse(max(df_pred.fecha))))
datesx = list(itertools.product(datesx,df_pred['nemotecnico_se'].unique()))
datesx = pd.DataFrame(datesx, columns =['date_ymdh','nemotecnico_se'])
datesx['date_ymdh'] = pd.to_datetime(datesx['date_ymdh'], utc = True)
df_pred['date_ymdh'] = pd.to_datetime(df_pred['date_ymdh'], utc = True)

df_pred = datesx.merge(df_pred, on=['nemotecnico_se','date_ymdh'], how='left')

# Generar otras covariables -----------------------------------------------

# agregar variables cuadraticas y cubicas

def elevate_variables(df,vars,x):
    for i in range(0,len(vars)):
        quadratic_col = vars[i]+'_elevate_'+str(x)
        df[quadratic_col] = df[vars[i]]**x
    return(df)  

vars_num = [df_pred.columns[df_pred.columns.str.startswith("gen")],
           df_pred.columns[df_pred.columns.str.startswith("cmg")],
           'demanda_mwh','cap_inst_mw']

df_pred = elevate_variables(df_pred,vars_num,2)
df_pred = elevate_variables(df_pred,vars_num,3)

# agregar estadisticos

vars_num = [df_pred.columns[df_pred.columns.str.startswith("gen")],
           df_pred.columns[df_pred.columns.str.startswith("cmg")],
           df_pred.columns[df_pred.columns.str.startswith('demanda_mwh')],
           df_pred.columns[df_pred.columns.str.startswith('cap_inst_mw')]]

def stats_variables(df,vars,stat,group):
    for i in range(0,len(vars)):
        new_col = vars[i]+'_'+stat
        df[new_col] =  df[vars[i]].groupby(df[group]).transform(stat)
    return(df) 

df_pred = stats_variables(df_pred,vars_num,'mean','date_ymdh')
df_pred = stats_variables(df_pred,vars_num,'sum','date_ymdh')
df_pred = stats_variables(df_pred,vars_num,'median','date_ymdh')
df_pred = stats_variables(df_pred,vars_num,'std','date_ymdh')


# Generar la Y  -----------------------------------------------------------

df_pred = df_pred.sort_values(["nemotecnico_se","date_ymdh"], ascending=[True, False])
df_pred.rename({'date_ymdh': 'date_x'}, axis=1, inplace=True)

df_pred['Y1'] = df_pred.groupby(['nemotecnico_se'])['flag'].shift(1)
df_pred['Y12'] = df_pred.groupby(['nemotecnico_se'])['flag'].shift(12)
df_pred['date_y1']=df_pred['date_x'].apply(lambda x: x+np.timedelta64(1,'h'))
df_pred['date_y12']=df_pred['date_x'].apply(lambda x: x+np.timedelta64(12,'h'))
df_pred['camada_y1']=df_pred['date_y1'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))
df_pred['camada_y12']=df_pred['date_y12'].apply(lambda x: datetime.strftime(x, '%Y-%m-%d'))

# sanity check
df_pred['Y1'].mean()
df_pred['Y12'].mean()
df_pred.shape

# Entrenar el modelo  -----------------------------------------------------

# Separar datas modelos 1 y 2


df_pred_M1 = df_pred.query('Y1!="NaN" & cmg_prog!="NaN" & cmg_real!="NaN" & cmg_prog!=0 & cmg_real!=0 & original==1')
df_pred_M12 = df_pred.query('Y12!="NaN" & cmg_prog!="NaN" & cmg_real!="NaN" & cmg_prog!=0 & cmg_real!=0 & original==1')

# Exportar datas ----------------------------------------------------------

df_pred_M1.to_csv(p.path+"df_model1.csv")
df_pred_M12.to_csv(p.path+"df_model12.csv")


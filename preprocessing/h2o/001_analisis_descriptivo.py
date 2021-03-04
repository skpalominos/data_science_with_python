#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 16:40:44 2021

@author: seomara
"""

# - -----------------------------------------------------------------------
# librerias 
# - -----------------------------------------------------------------------

import pandas as pd
import csv
import numpy as np
import math as my
import scipy
import xverse
from xverse.transformer import MonotonicBinning
import matplotlib.pyplot as plt
from datetime import date
from datetime import datetime, timedelta
import itertools
%matplotlib inline

# parametros

class param(): 
    path = '/Users/seomara/Documents/work/test/spike/files/'

p = param()

# - -----------------------------------------------------------------------
# P1 - Costos Marginales --------------------------------------------------
# - -----------------------------------------------------------------------

def leer_csv(path,file_name):
    df = pd.read_csv(path+file_name)
    df.columns = df.columns.str.lower()
    return(df)

# Leer dataset  -----------------------------------------------------------

cm_real = leer_csv(p.path,'costo_marginal_real.csv')
cm_prog = leer_csv(p.path,'costo_marginal_programado.csv')

# Eliminar datos con id duplicado -----------------------------------------

def delete_dup_id(df,ids):
    return(df.groupby(ids).first().reset_index())
    
cm_real = delete_dup_id(cm_real,['barra_mnemotecnico','fecha','hora']) 
cm_prog = delete_dup_id(cm_prog,['mnemotecnico_barra','fecha','hora']) 

# Join --------------------------------------------------------------------

costo_marginal = cm_real.merge(cm_prog,how='left',left_on=['barra_mnemotecnico','fecha','hora'], right_on=['mnemotecnico_barra','fecha','hora'])
costo_marginal = costo_marginal.drop('mnemotecnico_barra', axis=1)

# Sanity Check ------------------------------------------------------------

cm_real.shape[0]
cm_prog.shape[0]
costo_marginal.shape[0]

costo_marginal.columns

# Analisis descriptivo ----------------------------------------------------

# histogramas 


def histograma(x,text): 
    plt.hist(x, density=True, bins=30)  
    plt.ylabel('Probability')
    plt.xlabel(text)
    
histograma(costo_marginal['costo_en_pesos'],"CM real en pesos")
histograma(costo_marginal['costo'],"CM programado en pesos")

# summary 

costo_marginal[['costo','costo_en_dolares','costo_en_pesos']].agg(['sum','mean','median','max','min'])


#En particular analiza las barras (barra_mnemotecnico)

dist_barra = costo_marginal.groupby(['barra_mnemotecnico']).size().reset_index(name='counts')

#sumary 
dist_barra.agg(['min','max','mean','median']) 


class stats_missing:
    def __init__(self,df,x):
        self.df = df
        self.x = x

    def n_null(self):
        return(self.df[[self.x]].isnull().sum())

    def per_null(self):
        return(self.df[[self.x]].isnull().sum() / self.df.shape[0] * 100)

miss_stats = stats_missing(costo_marginal,'costo')

#¿Para cuántas barras se programa el costo?

miss_stats.n_null()

#¿Qué porcentaje es del total de barras que puedes observar en la base?

miss_stats.per_null()

# - -----------------------------------------------------------------------
# P2 - Construccion de variables ------------------------------------------
# - -----------------------------------------------------------------------

# Construccion de variables  ----------------------------------------------

costo_marginal = costo_marginal.assign(desviacion = lambda x: (x.costo_en_pesos-x.costo),
                                       desviacion_pct = lambda x: ((x.desviacion/x.costo_en_pesos)))

costo_marginal = costo_marginal.dropna(subset=['desviacion_pct'])
costo_marginal['desviacion_cat'] = costo_marginal['desviacion_pct'].apply(lambda x: 1 if x > 0.15 else 0)


# Analisis descriptivo desviacion_cat -------------------------------------

costo_marginal.groupby(['desviacion_cat']).size().reset_index(name='counts')

# construccion variables de utilidad

costo_marginal['hora'] = costo_marginal['hora'].apply(lambda x: str(x).zfill(2))
costo_marginal = costo_marginal.assign(date_ymdh = lambda x: (x.fecha+' '+x.hora+':00:00'))
costo_marginal['camada'] = costo_marginal['fecha'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d').replace(day=1))                                  

#plot 1

df_plot = costo_marginal.groupby(['camada','desviacion_cat']).size().reset_index(name='counts')
df_plot1 = df_plot.query('desviacion_cat==1') 

plt.bar(np.arange(len(df_plot1['camada'])), df_plot1['counts'])
plt.xticks(np.arange(len(df_plot1['camada'])),df_plot1['camada'], color='black',rotation=90)
plt.yticks(color='black')
plt.show()

#plot 2
df_plot1['counts']=df_plot1['counts']/df_plot2['counts sum']
df_plot2 = df_plot.groupby(['camada']).agg({'counts':['sum']})
df_plot2.columns=df_plot2.columns.droplevel()
df_plot2.columns = ['camada','sum']
df_plot2['prop'] = df_plot1['counts']/df_plot2['sum']
df_plot2 = df_plot2.fillna(0)

plt.plot( 'camada', 'prop', data=df_plot2, linestyle='-', marker='o')
plt.show()

# - -----------------------------------------------------------------------
# Visualiazacion ----------------------------------------------------------
# - -----------------------------------------------------------------------

def time_plot_costo_barra(codigo_barra,fecha_inicial,fecha_final,df):
    df = df.query('barra_mnemotecnico==@codigo_barra & date_ymdh>=@fecha_inicial & date_ymdh<=@fecha_final') 
    df = df[['date_ymdh','costo','costo_en_pesos']]
    df = df.set_index('date_ymdh')
    ax = df.plot(linewidth=2, fontsize=12)
    ax.set_xlabel('Date')
    ax.legend(fontsize=12)

codigos = ["BA01T002SE036T002","BA02T003SE004T003","BA83L131SE134L131","BA01G004SE008G004"]
fecha_inicial="2019-01-24"
fecha_final="2019-07-01"

plots = list(map(time_plot_costo_barra,
                 codigos,
                 itertools.repeat(fecha_inicial),
                 itertools.repeat(fecha_final),
                 itertools.repeat(costo_marginal)))










#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  1 13:05:20 2021

@author: seomara
"""

# importar h20 

import h2o
from h2o.estimators.glm import H2OGeneralizedLinearEstimator

# generar cluster

h2o.init()
h2o.cluster_info()


# importar dataset 

fr = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/prostate/prostate.csv.zip")
fr[1] = fr[1].asfactor()

# especificar modelo
m = H2OGeneralizedLinearEstimator(family="binomial")


# train the model
m.train(x=fr.names[2:], y="CAPSULE", training_frame=fr)
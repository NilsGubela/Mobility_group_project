#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gesine steudle
"""


# ========== run simulation  ==========
from world import World
import numpy as np
import warnings
warnings.filterwarnings("ignore")

parameters ={'timeSteps': 25,
             'density': 2, # choose between population mpas 1,2,3,4
             'initialChoice': 2, # choose between initial choice sets 1,2,3,4
             'nFriends': 15,
             'friendsLocally': True,
             'loadNetwork': False,
             'weightFriends': True,
             'convenienceBonus': True, 
             'convenienceMalus': True}

parameters['simulationName'] = ('d'+ str(parameters['density']) + '-f' + str(parameters['nFriends']) +
          '-loc' + str(parameters['friendsLocally']) +'-bon' + 
          str(parameters['convenienceBonus']) +'-mal' + str(parameters['convenienceMalus']) +'-')


world= World(parameters, 1, 1)
np.save('initMatrix',world.network)

parameters["loadNetwork"] = True

#cm_grid = np.linspace(1,10,10)
#umax_grid = np.linspace(2,10,9)

cm_grid = np.linspace(1,100,101)
#cm_grid = [25]
umax_grid = np.linspace(1,5,5)
#umax_grid = [4]

#bonus_grid = [0.1, 0.5, 1, 5, 10]

#cm_grid = [5,6,7,8,9,10]
#umax_grid = [3,5,10]

res = np.zeros((len(cm_grid)*len(umax_grid),3))

k = 0
for cm in cm_grid:
    for u_max in umax_grid:
        world= World(parameters, cm, u_max)
        world.runSimulation()
        res[k,0] = world.cm
        res[k,1] = world.u_max
        res[k,2] = world.av_ratio
        k += 1

np.save("result", res)



# ========== plot functions ==========
plotting = False

plotSelection = {'population':1,
         'conveniencesStart': 1,
         'conveniencesEnd': 1,
         'usageMaps': True,
         'usagePerCell': [],# [[0,0],[1,5],[4,0],[5,5]], # add a list of cells by coordinates, e.g. [[1,1],[3,4]],
         'utilityOverTime': 1,
         'carUsageOverTime': 1,
         'similarityOverTime': 0
        }


from plotResults import plotResults, loadResults
from inputs import Inputs
from tools import Tools

if plotting:
    endTime, nCells, cellProperties, cellRecord, nPersons, personProperties, personRecord, globalRecord, simParas = loadResults(parameters['simulationName'])
    
    plotResults(plotSelection, directory = 'pics/', endTime=endTime, nCells=nCells, cellProperties=cellProperties, cellRecord=cellRecord, 
                nPersons=nPersons, personProperties=personProperties, personRecord=personRecord, globalRecord=globalRecord, simParas=simParas)
        
    densities = Inputs.density.flatten()
    utilmax = [max(Tools.gaussian((max(densities)-min(densities))/2, min(densities), d)*100 +1,
                   Tools.gaussian((max(densities)-min(densities))/2, max(densities), d)*100+1) for d in densities]
    utilmean = sum(utilmax)/len(utilmax)
    print('mean utility is ' + str(utilmean))


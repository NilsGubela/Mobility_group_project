#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gesine steudle
"""


# ========== run simulation  ==========
from world import World

parameters ={'timeSteps': 50,
             'density': "Phoenix", # choose between population mpas 1,2,3,4
             'initialChoice': "Phoenix", # choose between initial choice sets 1,2,3,4
             'nFriends': 15,
             'friendsLocally': True,
             'loadNetwork': False,
             'weightFriends': True,
             'convenienceBonus': True, 
             'convenienceMalus': True}

parameters['simulationName'] = ('d'+ str(parameters['density']) + '-f' + str(parameters['nFriends']) +
          '-loc' + str(parameters['friendsLocally']) +'-bon' + 
          str(parameters['convenienceBonus']) +'-mal' + str(parameters['convenienceMalus']) +'-')


world= World(parameters)
world.runSimulation()




# ========== plot functions ==========
plotting = True

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


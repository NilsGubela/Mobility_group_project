#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gsteudle
"""

import os
import numpy as np
from world import World
from inputs import Inputs
from tools import Tools
import matplotlib.pyplot as plt

# ========== run simulation  ==========

parameters ={'runs': 100,
             'timeSteps': 71,
             'density': 2, # choose between population mpas 1,2,3,4
             'initialChoice': 2, # choose between initial choice sets 1,2,3,4
             'nFriends': 15,
             'friendsLocally': True,
             'loadNetwork': False,
             'weightFriends': True,
             'convenienceBonus': False, 
             'convenienceMalus': False,
             'sameNetwork': False}

deleteFiles = True

world = World(parameters)
np.save('initMatrix',world.network)
names = list()
for j in range(parameters['runs']):       
    parameters['simulationName'] = ('run-'+ str(j) + '_d'+ str(parameters['density']) + '-f' + str(parameters['nFriends']) +
              '-loc' + str(parameters['friendsLocally']) +'-bon' + 
              str(parameters['convenienceBonus']) +'-mal' + str(parameters['convenienceMalus']) +'-')
    names.append(parameters['simulationName'])
    if parameters['sameNetwork']:
        parameters['loadNetwork'] = True
    world = World(parameters)
    world.runSimulation()



# ========== mean cell record  ==========
cellRecords = list()
overallUsage = list()
overallUtility = list()
endTime = parameters['timeSteps']-1
n = len(names)

for name in names:
    cellRecord = np.load(name+'cellRecord.npy') 
    cellRecords.append(cellRecord[endTime])
    globalRecord = np.load(name+'globalRecord.npy')
    overallUsage.append(globalRecord[endTime][0])
    overallUtility.append(globalRecord[endTime][1])
    
    
cellProperties = np.load(name+'cellProperties.npy')
nCells = len(cellProperties)

entries = len(cellRecord[0][0])
meanCellRecordEnd = np.zeros((nCells,entries))
varCellRecordEnd = np.zeros((nCells,entries))
     
for cellId in range(nCells):
    for i in range(entries):
        meanCellRecordEnd[cellId][i] = sum([cr[cellId][i] for cr in cellRecords])/n
        varCellRecordEnd[cellId][i] = np.var([cr[cellId][i] for cr in cellRecords])


xMap = Inputs.density.shape[0]
yMap = Inputs.density.shape[1]

carUsage = np.zeros((xMap,yMap))
carUsageVar = np.zeros((xMap,yMap))
utilitiesCar = np.zeros((xMap,yMap))
utilitiesPublic = np.zeros((xMap,yMap))
utilities = np.zeros((xMap,yMap))
for cellId in range(nCells):
    carUsage[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = meanCellRecordEnd[cellId][2]/cellProperties[cellId][2]
    utilitiesCar[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = meanCellRecordEnd[cellId][0]
    utilitiesPublic[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = meanCellRecordEnd[cellId][1]
    utilities[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = meanCellRecordEnd[cellId][4]
Tools.densityPlot(carUsage, title = "Car usage end, mean", name="carUsageMean", cmap="Greys", minmax = True, vmin = 0, vmax = 1)  
Tools.densityPlot(utilitiesCar, title = "Car utility end, mean", name="carUtilityMean", cmap="Blues", minmax = True, vmin = 0, vmax = 4)
Tools.densityPlot(utilitiesPublic, title = "Public transport utility end, mean", name="publicUtilityMean", cmap="Greens", minmax = True, vmin = 0, vmax = 4)
Tools.densityPlot(utilities, title = "mean utility end, mean", name="utilityMean", cmap="Wistia", minmax = True, vmin = 2, vmax = 3.5)

carUsageVar = np.zeros((xMap,yMap))
for cellId in range(nCells):
    carUsageVar[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = varCellRecordEnd[cellId][2]#/cellProperties[cellId][2]
Tools.densityPlot(carUsageVar, title = "Car usage end, variance", name="carUsageVar", cmap="Reds", minmax = True, vmin = 0, vmax = 3)  

plt.hist(overallUsage, bins=5, range=(0,1) )
plt.savefig('carUsageHist.png', bbox_inches = 'tight')

#plt.hist(overallUtility, bins=5)
#plt.savefig('utilityHist.png', bbox_inches = 'tight')

print('Mean utility is ' + str(np.mean(overallUtility)))


if deleteFiles:
    for name in names:
        appendices = ['cellProperties.npy','cellRecord.npy','globalRecord.npy','personProperties.npy','personRecord.npy','network.npy', 'mobilityTypes.json', 'personsInCell.json','worldParameters.json']
        for appendix in appendices:
            os.remove(name + appendix)
        
    

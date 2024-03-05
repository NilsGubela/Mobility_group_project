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

# ========== run simulation  ==========

parameters ={'runs': 100,
             'timeSteps': 50,
             'density': 1, # choose between population mpas 1,2,3,4
             'initialChoice': 1, # choose between initial choice sets 1,2,3,4
             'nFriends': 15}


parameters['friendsLocally'] = True 
parameters['weightFriends'] = True
parameters['convenienceBonus'] = False 
parameters['convenienceMalus'] = False
deleteFiles = True

names = list()
for j in range(parameters['runs']):       
    parameters['simulationName'] = ('run-'+ str(j) + '_d'+ str(parameters['density']) + '-f' + str(parameters['nFriends']) +
              '-loc' + str(parameters['friendsLocally']) +'-bon' + 
              str(parameters['convenienceBonus']) +'-mal' + str(parameters['convenienceMalus']) +'-')
    names.append(parameters['simulationName'])
    world= World(parameters)
    world.runSimulation()




# ========== mean cell record  ==========
cellRecords = list()
endTime = parameters['timeSteps']-1
n = len(names)

for name in names:
    cellRecord = np.load(name+'cellRecord.npy') 
    cellRecords.append(cellRecord[endTime])
    
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
for cellId in range(nCells):
    carUsage[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = meanCellRecordEnd[cellId][2]/cellProperties[cellId][2]
Tools.densityPlot(carUsage, title = "Car usage end, mean", name="meanUsageEnd", cmap="Greys")  

carUsageVar = np.zeros((xMap,yMap))
for cellId in range(nCells):
    carUsageVar[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = varCellRecordEnd[cellId][2]#/cellProperties[cellId][2]
Tools.densityPlot(carUsageVar, title = "Car usage end, variance", name="meanUsageEnd", cmap="Reds")  



if deleteFiles:
    for name in names:
        appendices = ['cellProperties.npy','cellRecord.npy','globalRecord.npy','personProperties.npy','personRecord.npy','mobilityTypes.json', 'personsInCell.json','worldParameters.json']
        for appendix in appendices:
            os.remove(name + appendix)
        
    

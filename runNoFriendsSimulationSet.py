#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gsteudle
"""

import os
import numpy as np
import matplotlib.pyplot as plt

from world import World
from inputs import Inputs
from tools import Tools
from plotResults import plotUsage, loadResults

# ========== run simulation  ==========

nFriends = [1,10,50,100]

parameters ={'runs': 100,
             'timeSteps': 71,
             'density': 3, # choose between population mpas 1,2,3,4
             'initialChoice': 1, # choose between initial choice sets 1,2,3,4
             'loadNetwork': False,
             'weightFriends': True,
             'convenienceBonus': True, 
             'convenienceMalus': True,
             'sameNetwork': True}

deleteFiles = True

for nF in nFriends:
    for loc in [True]:#, False]:
        parameters['nFriends'] = nF
        parameters['friendsLocally'] = loc
        name0 = 'd' + str(parameters['density']) + '_' + str(nF) + '-friends_' + str(loc) +'_'
        
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
            
        # ========== plot last run ==========
        endTime, nCells, cellProperties, cellRecord, nPersons, personProperties, personRecord, globalRecord, simParas = loadResults(parameters['simulationName'])
        plotUsage(endTime, nCells, cellProperties, cellRecord, "localitySet/"+name0)
        
        # ========== plot means  ==========
        cellRecords = list()
        overallUsage = list()
        overallUtilityOverTime = list()
        endTime = parameters['timeSteps']-1
        n = len(names)
        
        for name in names:
            cellRecord = np.load(name+'cellRecord.npy') 
            cellRecords.append(cellRecord[endTime])
            globalRecord = np.load(name+'globalRecord.npy')
            overallUsage.append(globalRecord[endTime][0])
            overallUtilityOverTime.append(globalRecord[:][1])
        
        print(overallUtilityOverTime)
        cellProperties = np.load(name+'cellProperties.npy')
        nCells = len(cellProperties)
        
        entries = len(cellRecord[0][0])
        meanCellRecordEnd = np.zeros((nCells,entries))
        varCellRecordEnd = np.zeros((nCells,entries))
        meanUtilityOverTime = list()
        for t in range(len(overallUtilityOverTime[0])):
            meanUtilityOverTime.append(np.mean([overallUtilityOverTime[t][r] for r in range(parameters['runs'])]))
            
             
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
        Tools.densityPlot(carUsage, title = "Car usage end, mean", name="localitySet/"+name0+"carUsageMean", cmap="Greys", minmax = True, vmin = 0, vmax = 1)  
        Tools.densityPlot(utilitiesCar, title = "Car utility end, mean", name="localitySet/"+name0+"carUtilityMean", cmap="Blues", minmax = True, vmin = 0, vmax = 4)
        Tools.densityPlot(utilitiesPublic, title = "Public transport utility end, mean", name="localitySet/"+name0+"publicUtilityMean", cmap="Greens", minmax = True, vmin = 0, vmax = 4)
        Tools.densityPlot(utilities, title = "Mean utility end, mean", name="localitySet/"+name0+"utilityMean", cmap="Wistia", minmax = True, vmin = 2, vmax = 3.5)
        #print('Mean utility is ' + str(np.mean(overallUtility)))
        
        carUsageVar = np.zeros((xMap,yMap))
        for cellId in range(nCells):
            carUsageVar[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = varCellRecordEnd[cellId][2]#/cellProperties[cellId][2]
        Tools.densityPlot(carUsageVar, title = "Car usage end, variance", name="localitySet/"+name0+"carUsageVar", cmap="Reds", minmax = True, vmin = 0, vmax = 3)  

        #plt.hist(overallUsage, bins=5, range=(0,1) )
        #plt.savefig('localitySet/'+name0+'carUsageHist.png', bbox_inches = 'tight')
        plt.plot(meanUtilityOverTime)
        
        print('---')
        
        
        if deleteFiles:
            for name in names:
                appendices = ['cellProperties.npy','cellRecord.npy','globalRecord.npy','personProperties.npy','personRecord.npy', 'network.npy','mobilityTypes.json', 'personsInCell.json','worldParameters.json']
                for appendix in appendices:
                    os.remove(name + appendix)
                
    

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gesine steudle
"""

import numpy as np
import json
import matplotlib.pyplot as plt
from tools import Tools
from inputs import Inputs

# ========== load results ==========
def loadResults(name):
    file = open(name+'worldParameters.json')
    simParas = json.load(file)     
    file.close()
    cellProperties = np.load(name+'cellProperties.npy')
    personProperties = np.load(name+'personProperties.npy')
    nCells = len(cellProperties)
    nPersons = len(personProperties)
    cellRecord = np.load(name+'cellRecord.npy')
    personRecord = np.load(name+'personRecord.npy')
    globalRecord = np.load(name+'globalRecord.npy')
    timeSteps = len(cellRecord)
    endTime = timeSteps - 1
    return endTime, nCells, cellProperties, cellRecord, nPersons, personProperties, personRecord, globalRecord, simParas

# ========== plot functions ==========

xMap = Inputs.density.shape[0]
yMap = Inputs.density.shape[1]

def plotUsagePerCell(timeSteps, nCells, cellProperties, cellRecord, allCells = True, coordinates = [0,0]):
    time = [t for t in range(timeSteps)]
    def plotCell(time, usersBrown, usersPubic):
        fig = plt.figure()
        plt.plot(time,usersBrown)
        plt.plot(time,usersPublic)
        fig.show()
    for cellId in range(nCells):
        if allCells:
            usersBrown = [cellRecord[t][cellId][2] for t in range(timeSteps)]
            usersPublic = [cellRecord[t][cellId][3] for t in range(timeSteps)]
            plotCell(time, usersBrown, usersPublic)
        else:
            if cellProperties[cellId][0] == coordinates[0] and cellProperties[cellId][1] == coordinates[1]:
                usersBrown = [cellRecord[t][cellId][2] for t in range(timeSteps)]
                usersPublic = [cellRecord[t][cellId][3] for t in range(timeSteps)]
                plotCell(time, usersBrown, usersPublic)
                break
          
def plotPopulationDensity(simParas, directory):
    Tools.densityPlot(Inputs.density, title='population map B', name = 'population', directory = directory)
    #Tools.densityPlot(Inputs.density, title='population map ' + str(simParas['density']), name = 'population', directory = directory)
          
def plotConvenience(t, nCells, cellProperties, cellRecord, mobType, directory):
    convenience = np.zeros((xMap,yMap))
    for cellId in range(nCells):
        convenience[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = cellRecord[t][cellId][mobType]
        name = 'convenience'
        if mobType==0:
            title = 'Car conveniences'
            colours = 'Blues'
            name = directory+'convenienceCar-time'+str(t)
        elif mobType==1:
            title = 'Public transport conveniences'
            colours = 'Greens'
            name = directory+'conveniencePt-time'+str(t)
    Tools.densityPlot(convenience, title = title, name = name, cmap=colours)        

def plotUsage(t, nCells, cellProperties, cellRecord, directory):
    carUsage = np.zeros((xMap,yMap))
    for cellId in range(nCells):
        carUsage[int(cellProperties[cellId][0])][int(cellProperties[cellId][1])] = cellRecord[t][cellId][2]/cellProperties[cellId][2]
    name = directory+'carUsage-time'+str(t)
    Tools.densityPlot(carUsage, title = "Car usage, t=" + str(t), name = name, cmap="Greys", minmax= True, vmin = 0, vmax = 1)

def plotVariableOverTime(timeSteps, variable, figname):
    time = [t for t in range(timeSteps)]
    fig = plt.figure()
    plt.plot(time,variable)
    plt.savefig(figname, bbox_inches = 'tight')
    fig.show()

def plotUtilitiesOverTime(timeSteps, utilities, utilitiesCar, utilitiesPublic, directory):
    time = [t for t in range(timeSteps)]
    fig = plt.figure()
    plt.plot(time,utilities)
    plt.plot(time,utilitiesPublic)
    plt.plot(time,utilitiesCar)
    plt.savefig(directory+'utilitiesOverTime.png', bbox_inches = 'tight')
    fig.show()
    


# ========== plot results ==========

def plotResults(selection, directory= '', **results):
    if selection['population']: plotPopulationDensity(results['simParas'], directory = directory)
    if selection['conveniencesStart']: 
        plotConvenience(0, results['nCells'], results['cellProperties'], results['cellRecord'], mobType = 0, directory = directory)
        plotConvenience(0, results['nCells'], results['cellProperties'], results['cellRecord'], mobType = 1, directory = directory)
    if selection['conveniencesEnd']: 
        plotConvenience(results['endTime'], results['nCells'], results['cellProperties'], results['cellRecord'], mobType = 0, directory = directory)
        plotConvenience(results['endTime'],  results['nCells'], results['cellProperties'], results['cellRecord'], mobType = 1, directory = directory)
    for coordinates in selection['usagePerCell']: 
        plotUsagePerCell(results['endTime']+1, results['nCells'], results['cellProperties'], results['cellRecord'], False, coordinates)
    if selection['usageMaps']: 
        plotUsage(0, results['nCells'], results['cellProperties'], results['cellRecord'], directory = directory)
        #plotUsage(int(results['endTime']/2), results['nCells'], results['cellProperties'], results['cellRecord'])
        plotUsage(results['endTime'],  results['nCells'], results['cellProperties'], results['cellRecord'], directory = directory)
    if selection['utilityOverTime']: 
        plotUtilitiesOverTime(results['endTime']+1, results['globalRecord'][:,1], results['globalRecord'][:,2], results['globalRecord'][:,3], directory = directory)
    if selection['carUsageOverTime']: plotVariableOverTime(results['endTime']+1, results['globalRecord'][:,0], figname = directory + 'carUsageOverTime.png')
    if selection['similarityOverTime']: plotVariableOverTime(results['endTime']+1, results['globalRecord'][:,4], directory + 'similarity.png' )

    

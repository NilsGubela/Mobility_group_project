#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gesine steudle
"""
import copy as cp
import numpy as np
import random as rd
import json

from inputs import Inputs
from cell import Cell
from person import Person


class World:
    
#----- Initialize ----- 
    def __init__(self, parameters):
        self.parameters = parameters
        self.mobTypeDict = {'car' : 0, 'public': 1}
        self.variables = {'carUsage': 0.5, 'meanUtility': 0, 'meanUtilityCar': 0, 'meanUtilityPublic': 0, 'meanSimilarity': parameters['nFriends']/2} 
        # setup simulation:
        self.population = self.initPopulation(parameters['density'])
        Cell.count = 0; Person.count = 0
        self.cells = self.initCells(self.parameters['convenienceBonus'],self.parameters['convenienceMalus'])
        self.persons = self.initPersons()
        self.nPersons = len(self.persons)
        self.initMobilityChoices(parameters['initialChoice'])
        self.network = np.zeros((self.nPersons,self.nPersons))
        self.generateSocialNetwork()
        self.time = 0
                                      
      
    def initPopulation(self, densityType):
        density = Inputs.initDensity(densityType)
        return density
    
    def initCells(self, bonus, malus):
        cells = list()
        for x in range(len(self.population)):
            for y in range(len(self.population[0])):
                cell = Cell([x,y], self.population[x][y], bonus, malus)
                cells.append(cell)
        return cells
    
    def initPersons(self):
        persons = Inputs.createPersons()
        personsDistributed = 0
        for cell in self.cells:
            personsInCell = [persons[i] for i in range(personsDistributed, personsDistributed + cell.final['density'])]
            cell.persons = personsInCell
            for person in personsInCell:
                person.cell = cell
            personsDistributed += cell.final['density']
        return persons
    
    def generateSocialNetwork(self):
        if self.parameters['loadNetwork']:
            initMatrix = np.load('initMatrix.npy')
            self.network = initMatrix
            for person in self.persons:
                person.friends = list()
                for other in self.persons:
                    if initMatrix[person.id][other.id] == 1:
                        person.friends.append(other)
                person.friendWeights = np.ones(len(person.friends))
        else:
            for person in self.persons:
                persons = cp.copy(self.persons)
                persons.remove(person)
                person.generateFriends(persons, self.parameters['nFriends'], self.parameters['friendsLocally'])
                for friend in person.friends:
                    self.network[person.id][friend.id] = 1
            # for person in self.persons:
            #     persons = cp.copy(self.persons)
            #     m = person.variable['mobilityType']
            #     persons = list(filter(lambda p: p.variable['mobilityType']!=m, persons))
            #     #persons.remove(person)
            #     person.generateFriends(persons, nFriends, self.parameters['friendsLocally'])
            
    def initMobilityChoices(self, initChoice):
        if initChoice == 1: mobTypes = Inputs.initChoice1
        elif initChoice == 2: mobTypes = Inputs.initChoice2
        elif initChoice == 3: mobTypes = Inputs.initChoice3
        else:
            mobTypes = list()
            for i in range(len(self.persons)):
                mobTypes.append(rd.randint(0,1))
        for p, person in enumerate(self.persons):
            person.variable['mobilityType'] = mobTypes[p]
            person.newMobilityType = mobTypes[p]
            person.updateUtility()
            
#    def initMobilityChoices2(self, initChoice):
#        for p, person in enumerate(self.persons):
#            if len(person.cell.persons) < 14:
#                person.variable['mobilityType'] = 1
#            elif len(person.cell.persons) > 14:
#                person.variable['mobilityType'] = 0
#            else:
#                person.variable['mobilityType'] = np.random.choice([0,1])
#            person.updateUtility()
                
    def finalizeInit(self):
        name = self.parameters['simulationName']
        cellProperties = np.zeros((len(self.cells), Cell.finalAttributes))
        personProperties = np.zeros((len(self.persons), Person.finalAttributes))
        mobilityTypes = dict()
        for key in self.mobTypeDict.keys():
            mobilityTypes[self.mobTypeDict[key]] = key
        file = open(name+'mobilityTypes.json', 'w')
        json.dump(mobilityTypes, file)  
        file.close()
        for person in self.persons:
            for k, key in enumerate(person.final.keys()):
                personProperties[person.id][k] = person.final[key]        
        personsInCell = dict()
        for cell in self.cells:
            personsInCell[cell.id] = [person.id for person in cell.persons]
            for k, key in enumerate(cell.final.keys()):
                cellProperties[cell.id][k] = cell.final[key]
        file = open(name+'personsInCell.json', 'w')
        json.dump(personsInCell, file)  
        file.close()
        np.save(name+'cellProperties',cellProperties)
        np.save(name+'personProperties',personProperties)
        file = open(name+'worldParameters.json', 'w')
        json.dump(self.parameters, file)  
        file.close()
        np.save(name+'network', self.network)

                       

#----- Run and Save -----       
    def runSimulation(self):
        self.finalizeInit()
        timeSteps = self.parameters['timeSteps']
        name = self.parameters['simulationName']
        
        self.cellRecord = np.zeros((timeSteps, len(self.cells), Cell.variableAttributes), dtype = float)
        self.personRecord = np.zeros((timeSteps, len(self.persons), Person.variableAttributes), dtype = float)
        self.globalRecord = np.zeros((timeSteps, len(self.variables)), dtype = float)
              
        for time in range(0,timeSteps):
            self.time = time
            self.step(time)   
            
        np.save(name+'cellRecord',self.cellRecord)
        np.save(name+'personRecord',self.personRecord)
        np.save(name+'globalRecord',self.globalRecord)       
#-- End Run and Save -----    



# ----- World Time Step -----
    def step(self,time):    
        utilities = list()
        utilitiesCar = list()
        utilitiesPublic = list()
        similarList = list()
        
        if time > 0:          
            for person in self.persons:
                person.updateMobilityType()
            
        for cell in self.cells:
            cell.step()
            for k, key in enumerate(cell.variable.keys()): 
                self.cellRecord[self.time][cell.id][k] = cell.variable[key] 
   
        for person in self.persons:
            person.updateUtility()
            
        for person in self.persons:
            person.step(self.time, self.parameters['weightFriends'])  
            
            # --- calculate global record ---    
            for k, key in enumerate(person.variable.keys()): 
                self.personRecord[self.time][person.id][k] = person.variable[key]
            utilities.append(person.variable['utility'])
            if person.variable['mobilityType']: utilitiesPublic.append(person.variable['utility'])
            else: utilitiesCar.append(person.variable['utility'])
            friendsMobTypes = [friend.variable['mobilityType'] for friend in person.friends]
            similar = friendsMobTypes.count(person.variable['mobilityType'])
            similarList.append(similar)
            
        # --- save global record ---    
        self.variables['meanUtility'] = np.mean(utilities)
        self.variables['meanUtilityCar'] = np.mean(utilitiesCar)
        self.variables['meanUtilityPublic'] = np.mean(utilitiesPublic)
        self.variables['carUsage'] = len(utilitiesCar)/self.nPersons
        self.variables['meanSimilarity'] = np.mean(similarList)
        for k, key in enumerate(self.variables.keys()): 
            self.globalRecord[self.time][k] = self.variables[key]
# ----- End Time Step -----        
                    



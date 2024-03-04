#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gesine steudle
"""

from tools import Tools
import numpy as np
import sys

class Person:
    count = 0
    finalAttributes = 0
    variableAttributes = 2
    
    def __init__(self):
        self.id = self.createId()
        self.final = {}
        self.variable = {'mobilityType': None, 'utility': 2.0}
        self.cell = None
        self.friends = list()
        self.friendWeights = list()
        self.utilityWeights = [1.]
        self.lastCopied = None
        self.lastUtility = self.variable['utility']
        self.newMobilityType = self.variable['mobilityType']

# ----- Init Functions-----        
    def createId(self):
        id = Person.count
        Person.count += 1
        return id
    
    def generateFriends(self, persons, nFriends, friendsLocally):
        if friendsLocally:
            measures = [1/(Tools.euclideanDistance(self.cell.coordinates, person.cell.coordinates)+0.1) for person in persons]
        else:
            measures = [1 for person in persons]
        probabilities = Tools.normalize(measures)
        self.friends = np.random.choice(persons, size=nFriends, replace=False, p=probabilities)
        self.friendWeights = np.ones(nFriends)
# ----- End Init -----           



    def returnConvenience(self):
        convenience = 0.
        if self.variable['mobilityType'] == 0: 
            convenience = self.cell.variable['convenienceCar']
        elif self.variable['mobilityType'] == 1: 
            convenience = self.cell.variable['conveniencePublic']      
        return convenience
 
    
    def updateMobilityType(self):
        self.variable['mobilityType'] = self.newMobilityType
    
    def updateUtility(self):
        self.lastUtility = self.variable['utility']
        self.variable['utility'] = self.returnConvenience()
   
    def imitate(self):               
        friendUtilities = [friend.variable['utility'] for friend in self.friends]
        probabilitiesRaw = [min(max(0.001,friendUtilities[i]*self.friendWeights[i]),1000) for i in range(len(self.friends))]
        probabilities = Tools.normalize(probabilitiesRaw)
        self.lastCopied = np.random.choice(self.friends, 1, p=probabilities)[0]

    def weightConnections(self, time):  
        if self.lastCopied != None:
            change = 1+(self.variable['utility']-self.lastUtility)/self.lastUtility
            friendCopied = self.lastCopied
            self.friendWeights[np.where(self.friends == friendCopied)]*=change
             
    def chooseNewMobilityType(self):
        if self.lastCopied.variable['utility'] <= self.variable['utility']:
            self.lastCopied = None
        else:
            self.newMobilityType = self.lastCopied.variable['mobilityType']
                
    def step(self, time, weightFriends):
        if weightFriends:
            self.weightConnections(time)
        self.imitate()
        self.chooseNewMobilityType()

                    

        
        
        
        
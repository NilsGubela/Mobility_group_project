#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  7 09:03:57 2021

@author: gesine
"""

import numpy as np

from mobilityTypes import PublicTransport, CombustionCar

class Cell():
    count = 0
    finalAttributes = 3
    variableAttributes = 5
    
    def __init__(self, coordinates, density, bonus, malus):
        self.id = self.createId()
        self.publicTransport = PublicTransport(density)
        self.combustionCar = CombustionCar(density)
        self.bonus = bonus
        self.malus = malus
        self.infraCar = 0
        self.infraPublic = 0
        self.final = {'x' : coordinates[0], 'y': coordinates[1], 'density' : density}
        self.variable = {'convenienceCar': self.combustionCar.convenience, 'conveniencePublic': self.publicTransport.convenience, 
                         'usageCar': 0,'usagePublic': 0, 'meanUtility': 2.0}
        self.persons = list()
        self.coordinates = coordinates

    def createId(self):
         id = Cell.count
         Cell.count += 1
         return id


    def updateMalus(self, proportion):
        if self.malus:
            factor = 1-proportion/3
        else:
            factor = 1
        return factor
    
    def updateConveniences(self):
        carProportion = self.variable['usageCar']/self.final['density']
        publicProportion = self.variable['usagePublic']/self.final['density']
        if self.bonus:
            self.infraCar = (self.infraCar*2 + carProportion)/3
            self.infraPublic = (self.infraPublic*2 + publicProportion)/3
        self.variable['convenienceCar'] = self.updateMalus(carProportion) * self.combustionCar.convenience + self.infraCar
        self.variable['conveniencePublic'] = self.updateMalus(publicProportion) * self.publicTransport.convenience + self.infraPublic
        
    
    def step(self):
        usageCar = 0
        usagePublic = 0
        for person in self.persons:
            if person.variable['mobilityType']: usagePublic += 1
            else: usageCar += 1
        self.variable['usageCar'] = usageCar
        self.variable['usagePublic'] = usagePublic
        self.updateConveniences()
        self.variable['meanUtility'] = (self.variable['convenienceCar']*usageCar + self.variable['conveniencePublic']*usagePublic) / (usageCar+usagePublic)
        
            
        
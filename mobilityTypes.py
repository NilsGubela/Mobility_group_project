#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gesine steudle
"""
from abc import ABC, abstractmethod
from tools import Tools
from inputs import Inputs


class MobilityType(ABC):
  
    @abstractmethod
    def getConvenience(self):
        pass
      
    
    
class CombustionCar(MobilityType):
    name = "car"
    def __init__(self, density):
        self.density = density
        self.convenience = self.getConvenience()

    def getConvenience(self):
        mu = Inputs.popMin
        sigma = (Inputs.popMax - mu)/2
        convenience = Tools.gaussian(sigma, mu, self.density)*100
        return convenience

       
    
class PublicTransport(MobilityType):
    name = "public"
    def __init__(self, density):
        self.density = density
        self.convenience = self.getConvenience()
    
    def getConvenience(self):
        mu = Inputs.popMax
        sigma = (mu - Inputs.popMin)/2
        convenience = Tools.gaussian(sigma, mu, self.density)*100
        return convenience


    

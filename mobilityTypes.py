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
    def __init__(self, av_ratio, cm, u_max):
        #self.density = density
        self.av_ratio = av_ratio
        self.infraPublic = 0
        self.cm = cm
        self.u_max = u_max
        self.convenience = self.getConvenience()
    
    def getConvenience(self):
        #mu = Inputs.popMax
        #sigma = (mu - Inputs.popMin)/2
        #convenience = Tools.gaussian(sigma, mu, self.density)*100

        convenience = Tools.sigmoidal(self.av_ratio*100, self.u_max, self.cm)
        # add the bonus and malus
        #return(convenience)
        #return (1-self.av_ratio/3) *convenience + self.infraPublic
        self.convenience = (1-self.av_ratio/3) *convenience + self.infraPublic

    def updateConvenience(self, av_ratio):
        self.av_ratio = av_ratio
        self.infraPublic = (self.infraPublic*2 + self.av_ratio)/3 
        #self.infraPublic = 1000 if self.av_ratio*100 < self.cm else 0


    

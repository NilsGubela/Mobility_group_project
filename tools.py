#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 13:29:07 2022

@author: gsteudle
"""
import math
import matplotlib.pyplot as plt
import numpy as np

class Tools:
    
    def gaussian(sigma, mu, rho):
        return math.exp(((rho-mu)/sigma)**2/(-2)) / math.sqrt(2*math.pi * sigma**2)

    def densityPlot(density, title = "Density Plot", name = "density", cmap="Oranges", minmax = False, **kwargs):
        plt.figure()
        if minmax:
            plt.imshow(density, cmap = cmap, vmin = kwargs['vmin'], vmax = kwargs['vmax'])
        else:
            plt.imshow(density, cmap = cmap)
        plt.title(title)
        plt.colorbar()
        plt.savefig(name +'.png', bbox_inches = 'tight')
        plt.show()

        
    def euclideanDistance(coordinatesA, coordinatesB):
        return math.sqrt((coordinatesA[0]-coordinatesB[0])**2 + (coordinatesA[1]-coordinatesB[1])**2)
    
    def normalize(array):
        sumArray = sum(array)
        return [element/sumArray for element in array]

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep  8 12:25:07 2021

@author: gesine steudle
"""

import numpy as np
import random as rd
from person import Person
from tools import Tools
import pandas as pd

class Inputs:

    density1 =  np.array([[2,2,2,2,14,14],
                          [2,2,2,2,14,14],
                          [2,2,2,14,14,14],
                          [2,2,14,14,14,14],
                          [14,14,14,14,14,14],
                          [14,14,14,14,14,26]])
    density2 =  np.array([[2,2,3,4,6,8],
                          [2,2,3,7,9,11],
                          [2,2,3,9,12,13],
                          [2,3,7,13,13,15],
                          [6,10,13,15,18,20],
                          [9,11,13,16,20,26]])
    density4 =  np.array([[26,14,14,14,14,14],
                          [14,14,14,14,2,14],
                          [14,14,2,14,14,14],
                          [14,14,14,14,14,14],
                          [14,14,14,14,14,26],
                          [2,14,2,14,14,14]])
    density3 = np.array([[5,4,3,3,2,2],
                         [7,5,4,4,2,3],
                         [11,9,8,4,7,7],
                         [19,22,15,12,10,8],
                         [26,24,21,11,9,5],
                         [26,24,20,12,11,5]])
    density = density4
    popMin = np.min(density)
    popMax = np.max(density)

    #density_phoenix = cls.create_Phoenix_density()

    #initChoice_phoenix = cls.create_Phoenix_density(density_phoenix)

    

    initChoice1 = np.random.binomial(1, 0.1 , 480)

    
    

    initChoice2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0,
 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1,
 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0,
 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0,
 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0,
 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0,
 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0,
 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0,
 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0,
 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0,
 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1,
 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1]



    initChoice1_og = [1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1,
       0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0,
       0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
       0, 0, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 0,
       0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0,
       0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1,
       1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1,
       1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0,
       1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1,
       1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
       0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0,
       1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0,
       0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1,
       1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
       0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1,
       1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0,
       0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0,
       1, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1,
       1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1,
       1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1,
       1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0,
       1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1]
    
    initChoice2_og = [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0,
       0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1,
       1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0,
       1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0,
       0, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0,
       0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0,
       0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1,
       0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1,
       1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1,
       0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0,
       1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0,
       0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0,
       0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1,
       1, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0,
       0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1,
       1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1,
       1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 1, 1, 1,
       0, 1, 1, 1, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 0, 0,
       0, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1,
       0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 1,
       0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0,
       0, 0, 0, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1]
    
    initChoice3 = [1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0,
       0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0,
       1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0,
       0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0,
       0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1,
       1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0,
       0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0,
       1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 1,
       0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 1,
       1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1,
       1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1,
       0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0,
       1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1,
       1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0,
       1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0,
       0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1,
       1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0,
       0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0,
       0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0,
       0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1,
       0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1,
       0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 1, 0]
 
    @classmethod  
    def initDensity(cls, densityType):
        if densityType == 1:
            cls.density = cls.density1
        elif densityType == 2:
            cls.density = cls.density2
        elif densityType == 3:
            cls.density = cls.density3
        elif densityType == "Phoenix":
            cls.density = cls.create_Phoenix_density()
        cls.popMin = np.min(cls.density)
        cls.popMax = np.max(cls.density)       
        return cls.density
      
    @classmethod  
    def createPersons(cls): 
        nPersons = sum([val for sublist in cls.density for val in sublist])
        persons = list()
        for i in range(int(nPersons)):
            person = Person()
            persons.append(person)
        return persons

    def create_Phoenix_density_unscaled():
        ve = pd.read_csv("HouseNo_and_VehicleNo1.csv")
        density = ve['hhn'].to_list()

        # Define the number of rows and columns for your matrix
        num_rows = 26
        num_cols = 25

        # Reshape the list into a matrix
        density_phoenix = np.flip(np.array(density).reshape(num_rows, num_cols), axis = 0)

        return density_phoenix

    def create_Phoenix_cars_scaled_unscaled():
        ve = pd.read_csv("HouseNo_and_VehicleNo1.csv")
        density = ve['hhn'].to_list()

        # Define the number of rows and columns for your matrix
        num_rows = 26
        num_cols = 25

        # Reshape the list into a matrix
        density_phoenix = np.flip(np.array(density).reshape(num_rows, num_cols), axis = 0)

        vehicle = ve['hvn'].to_list()

        # Define the number of rows and columns for your matrix
        num_rows = 26
        num_cols = 25

        # Reshape the list into a matrix
        vehicle_ownership_data = np.flip(np.array(vehicle).reshape(num_rows, num_cols), axis = 0)


        n_pop = sum(sum(density_phoenix))
        
        initChoice_phoenix = np.zeros(n_pop)
        l = 0
        for i in range(len(density_phoenix)):
            for j in range(len(density_phoenix[i])):
                density = density_phoenix[i,j]
                car_usage = vehicle_ownership_data[i,j]
                for k in range(density):
                    if k < car_usage:
                        initChoice_phoenix[l] = 1
                    else:
                        initChoice_phoenix[l] = 0
                    l += 1
        return(initChoice_phoenix)


    def create_Phoenix_density():
        ve = pd.read_csv("HouseNo_and_VehicleNo1.csv")
        density = ve['hhn'].to_list()

        # Define the number of rows and columns for your matrix
        num_rows = 26
        num_cols = 25

        # Reshape the list into a matrix
        density_data = np.flip(np.array(density).reshape(num_rows, num_cols), axis = 0)

        density_scaled = np.zeros((len(density_data), len(density_data[0])))

        max_density = max(density_data.flatten())

        for i in range(len(density_data)):
            for j in range(len(density_data[i])):
                density_scaled[i,j] = int(np.round(26*density_data[i,j]/max_density))

        return density_scaled.astype(int)

    def create_Phoenix_cars():
        ve = pd.read_csv("HouseNo_and_VehicleNo1.csv")
        density = ve['hhn'].to_list()

        # Define the number of rows and columns for your matrix
        num_rows = 26
        num_cols = 25

        # Reshape the list into a matrix
        density_data = np.flip(np.array(density).reshape(num_rows, num_cols), axis = 0)

        density_scaled = np.zeros((len(density_data), len(density_data[0])))

        max_density = max(density_data.flatten())

        for i in range(len(density_data)):
            for j in range(len(density_data[i])):
                density_scaled[i,j] = int(np.round(26*density_data[i,j]/max_density))

        vehicle = ve['hvn'].to_list()

        # Define the number of rows and columns for your matrix
        num_rows = 26
        num_cols = 25

        # Reshape the list into a matrix
        vehicle_ownership_data = np.flip(np.array(vehicle).reshape(num_rows, num_cols), axis = 0)


        n_pop = sum(sum(density_scaled))
        
        initChoice_phoenix = np.zeros(int(n_pop))

        l = 0
        for i in range(len(density_scaled)):
            for j in range(len(density_scaled[i])):
                density = int(density_scaled[i,j])
                car_usage = int(np.round(26*vehicle_ownership_data[i,j]/max_density))
                for k in range(density):
                    if k < car_usage:
                        initChoice_phoenix[l] = 0
                    else:
                        initChoice_phoenix[l] = 1
                    l += 1
        return(initChoice_phoenix.astype(int))
        

    

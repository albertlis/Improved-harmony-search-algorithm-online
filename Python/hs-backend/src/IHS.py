# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 17:10:54 2020

@author:
    Adrian Czupak & Albert Lis
"""

import numpy as np
from random import uniform
from IHSParameters import IHSParameters


class IHSAlgorithm:
    def __init__(self, parameters):
        self.IHSParameters = IHSParameters(parameters)
        self.__generation = 0
        self.__trace = []
        self.__lastBestSolutionIteration = 0
        self.__HM = []  # Harmony Memory
        self.__f = np.empty(self.IHSParameters.getHMS())
                
    def initializeHM(self):
        def catchZeroDivision(i):
            inputVector = {}
            varLowerBounds, varUpperBounds = self.IHSParameters.getBounds()
            for counter, var in enumerate(self.IHSParameters.getVariables()):
                inputVector.update({var: uniform(varLowerBounds[counter], varUpperBounds[counter])})
            self.__HM.append(inputVector)
            try:
                self._objective_function = self.IHSParameters.getObjectiveFunction()
                self.__f[i] = self.IHSParameters.getCompute()(self, inputVector)
            except ZeroDivisionError or RuntimeWarning:
                print("Nie wolno '/0' - Nununu")
                raise
        HMS = self.IHSParameters.getHMS()
        self.__f = np.empty(HMS)
        for i in range(HMS):
            catchZeroDivision(i)

    def improvise(self):
        new = {}
        lowerBounds, upperBounds = self.IHSParameters.getBounds()
        for i, variables in enumerate(self.IHSParameters.getVariables()):
            lowerBound = lowerBounds[i]
            upperBound = upperBounds[i]

            if uniform(0, 1) < self.IHSParameters.getHMCR():
                self.__makeMemoryConsideration(new, variables)

                if uniform(0, 1) < self.IHSParameters.getPAR():
                    self.__makePitchAdjustment(lowerBound, new, upperBound, variables)
            else:
                new.update({variables: uniform(lowerBound, upperBound)})
        return new

    def __makePitchAdjustment(self, lowerBound, new, upperBound, variables):
        BW = self.IHSParameters.getBW()
        if uniform(0, 1) < 0.5:
            D3 = (new.get(variables) - uniform(0, BW))
            if lowerBound <= D3:
                new.update({variables: D3})
        else:
            D3 = (new.get(variables) + uniform(0, BW))
            if upperBound >= D3:
                new.update({variables: D3})

    def __makeMemoryConsideration(self, new, variables):
        D1 = int(uniform(0, self.IHSParameters.getHMS()))
        D2 = self.__HM[D1].get(variables)
        new.update({variables: D2})

    def updateHM(self, new):
        f = self.IHSParameters.getCompute()(self, new)
        # for finding minimum
        fMaxValue = np.amax(self.__f)
        if f < fMaxValue:
            for i, value in enumerate(self.__f):
                if fMaxValue == value:
                    self.__f[i] = f
                    self.__HM[i] = new
                    break

    def __findTrace(self):
        index = np.argmin(self.__f)
        variables = self.__HM[index]
        if variables not in self.__trace:
            self.__trace.append(variables)
            self.__lastBestSolutionIteration = self.__generation

    def doYourTask(self):
        def catchZeroDivision():
            try:
                new = self.improvise()  # (self._generation - 1) % self.IHSParameters.getHMS()
                self.updateHM(new)
            except ZeroDivisionError or RuntimeWarning:
                print('i caughed ZeroDiv in IHS.updateHM')
                catchZeroDivision()
                
        self.initializeHM()
        while self.__generation < self.IHSParameters.getNumOfIterations():
            self.__generation += 1
            self.IHSParameters.updateHMCR(self.__generation)
            self.IHSParameters.updatePAR(self.__generation)
            self.IHSParameters.updateBW(self.__generation)
            catchZeroDivision()
            self.__findTrace()

    def getOptimalSolution(self):
        index = np.argmin(self.__f)
        functionValue = self.__f[index]
        variables = self.__HM[index]
        preparedVariables = dict()
        for key, value in variables.items():
            try:
                preparedVariables[key] = value
            except TypeError as e:
                print(e)
                return
        return functionValue, preparedVariables

    def getTrace(self):
        return self.__trace

    def getLastBestSolutionIteration(self):
        return self.__lastBestSolutionIteration
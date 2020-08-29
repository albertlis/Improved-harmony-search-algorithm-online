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
        self._generation = 0
        self._trace = []
        self._lastBestSolutionIteration = 0
        self._HM = []  # Harmony Memory
        self._f = np.empty(self.IHSParameters.getHMS())
                
    def initializeHM(self):
        def catchZeroDivision(i):
            inputVector = {}
            varLowerBounds, varUpperBounds = self.IHSParameters.getBounds()
            for counter, var in enumerate(self.IHSParameters.getVariables()):
                inputVector.update({var: uniform(varLowerBounds[counter], varUpperBounds[counter])})
            self._HM.append(inputVector)
            try:
                self._objective_function = self.IHSParameters.getObjectiveFunction()
                self._f[i] = self.IHSParameters.getCompute()(self, inputVector)
            except ZeroDivisionError or RuntimeWarning:
                print("Nie wolno '/0' - Nununu")
                raise
        HMS = self.IHSParameters.getHMS()
        self._f = np.empty(HMS)
        for i in range(HMS):
            catchZeroDivision(i)

    def improvise(self):
        new = {}
        lowerBounds, upperBounds = self.IHSParameters.getBounds()
        for i, variables in enumerate(self.IHSParameters.getVariables()):
            lowerBound = lowerBounds[i]
            upperBound = upperBounds[i]
            # memoryConsideration
            if uniform(0, 1) < self.IHSParameters.getHMCR():
                D1 = int(uniform(0, self.IHSParameters.getHMS()))
                D2 = self._HM[D1].get(variables)
                new.update({variables: D2})

                # pitchAdjustment
                if uniform(0, 1) < self.IHSParameters.getPAR():
                    BW = self.IHSParameters.getBW()
                    if uniform(0, 1) < 0.5:
                        D3 = (new.get(variables) - uniform(0, BW))
                        if lowerBound <= D3:
                            new.update({variables: D3})
                    else:
                        D3 = (new.get(variables) + uniform(0, BW))
                        if upperBound >= D3:
                            new.update({variables: D3})
            else:
                new.update({variables: uniform(lowerBound, upperBound)})
        return new

    def updateHM(self, new):
        f = self.IHSParameters.getCompute()(self, new)
        # for finding minimum
        fMaxValue = np.amax(self._f)
        if f < fMaxValue:
            for i, value in enumerate(self._f):
                if fMaxValue == value:
                    self._f[i] = f
                    self._HM[i] = new
                    break

    def _findTrace(self):
        index = np.argmin(self._f)
        variables = self._HM[index]
        if variables not in self._trace:
            self._trace.append(variables)
            self._lastBestSolutionIteration = self._generation

    def doYourTask(self):
        def catchZeroDivision():
            try:
                new = self.improvise()  # (self._generation - 1) % self.IHSParameters.getHMS()
                self.updateHM(new)
            except ZeroDivisionError or RuntimeWarning:
                print('i caughed ZeroDiv in IHS.updateHM')
                catchZeroDivision()
                
        self.initializeHM()
        while self._generation < self.IHSParameters.getNumOfIterations():
            self._generation += 1
            self.IHSParameters.updateHMCR(self._generation)
            self.IHSParameters.updatePAR(self._generation)
            self.IHSParameters.updateBW(self._generation)
            catchZeroDivision()
            self._findTrace()

    def getOptimalSolution(self):
        index = np.argmin(self._f)
        functionValue = self._f[index]
        variables = self._HM[index]
        preparedVariables = dict()
        for key, value in variables.items():
            try:
                preparedVariables[key] = value
            except TypeError as e:
                print(e)
                return
        return functionValue, preparedVariables

    def getTrace(self):
        return self._trace

    def getLastBestSolutionIteration(self):
        return self._lastBestSolutionIteration
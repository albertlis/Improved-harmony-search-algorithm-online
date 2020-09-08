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
    """! The main algorithm class.
        @author Albert Lis & Adrian Czupak
    """
    def __init__(self, parameters):
        """! The main algorithm class initializer.
        @param[in] parameters The dictonary with user defined parameters. See IHSParameters.
        @see IHSParameters.
        @return  An instance of the IHSAlgorithm class.
        """
        self.IHSParameters = IHSParameters(parameters)
        self._objective_function = self.IHSParameters.getObjectiveFunction()
        self.__generation = 0
        self.__trace = []
        self.__lastBestSolutionIteration = 0
        self.__HM = []  # Harmony Memory`
        self.__f = np.empty(self.IHSParameters.getHMS())
                
    def initializeHM(self):
        """! The function used to initialize harmony memory.
        """
        def catchZeroDivision(i):
            """! The function used to calculate and check correctness of data.
            """
            inputVector = {}
            varLowerBounds, varUpperBounds = self.IHSParameters.getBounds()
            for counter, var in enumerate(self.IHSParameters.getVariables()):
                inputVector.update({var: uniform(varLowerBounds[counter], varUpperBounds[counter])})
            self.__HM.append(inputVector)
            try:
                self.__f[i] = self.IHSParameters.getCompute()(self, inputVector)
            except ZeroDivisionError or RuntimeWarning:
                raise
        HMS = self.IHSParameters.getHMS()
        self.__f = np.empty(HMS)
        for i in range(HMS):
            catchZeroDivision(i)

    def improvise(self):
        """! The function is responsible for the improvisation step of the algorithm.
        """
        new = {}
        lowerBounds, upperBounds = self.IHSParameters.getBounds()
        for i, variable in enumerate(self.IHSParameters.getVariables()):
            lowerBound = lowerBounds[i]
            upperBound = upperBounds[i]

            if uniform(0, 1) < self.IHSParameters.getHMCR():
                self.__makeMemoryConsideration(new, variable)

                if uniform(0, 1) < self.IHSParameters.getPAR():
                    self.__makePitchAdjustment(lowerBound, new, upperBound, variable)
            else:
                new.update({variable: uniform(lowerBound, upperBound)})
        return new

    def __makePitchAdjustment(self, lowerBound, new, upperBound, variable):
        """! The function is responsible for the generating new values of pitch adjustment parameter.
        @param[in] lowerBound Float user defined lower bound of PAR parameter.
        @param[out] new Dictonary data row of currently calculated row of harmony memory.
        @param[in] upperBound Float user defined upper bound of PAR parameter.
        @param[in] variable String variable from extracted from function variable.
        """
        BW = self.IHSParameters.getBW()
        if uniform(0, 1) < 0.5:
            D3 = (new.get(variable) - uniform(0, BW))
            if lowerBound <= D3:
                new.update({variable: D3})
        else:
            D3 = (new.get(variable) + uniform(0, BW))
            if upperBound >= D3:
                new.update({variable: D3})

    def __makeMemoryConsideration(self, new, variable):
        """! The function is responsible for the generating new values of memory consideration parameter.
        @param[out] new Dictonary: currently calculated row of harmony memory.
        @param[in] variable String: variable from extracted from function variable.
        """
        D1 = int(uniform(0, self.IHSParameters.getHMS()))
        D2 = self.__HM[D1].get(variable)
        new.update({variable: D2})

    def updateHM(self, new):
        """! The function is responsible for updating harmony memory.
        @param[in] new Dictonary: calculated row of harmony memory.
        """
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
        """! The function is responsible for tracking algorithm trace.
        """
        index = np.argmin(self.__f)
        variables = self.__HM[index]
        if variables not in self.__trace:
            self.__trace.append(variables)
            self.__lastBestSolutionIteration = self.__generation

    def doYourTask(self):
        """! This function is main loop of algorithm.
        """
        def catchZeroDivision():
            """! The function used to calculate and check correctness of data.
            """
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
        """! Getter of optimal solution.
            @brief This function is used to get calculated optimal solution of function.
            @return Two values first Float: calculated minimum of function, second Dictonary: variables.
            names with values of optimal point.
        """
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
        """! Getter of trace.
            @brief This function is used to get trace of algorithm.
            @return List: All next optimal solutions found by algorithm
        """
        return self.__trace

    def getLastBestSolutionIteration(self):
        """! Getter of last iteration when algorithm found new solution.
            @return Integer: Last iteration when algorithm found new solution.
        """
        return self.__lastBestSolutionIteration
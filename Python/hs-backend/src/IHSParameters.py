from math import log, exp

import VP_WrongExpression
from VariablesParser import VariablesParser


class IHSParameters:
    """! The user defined parameters class.
        @brief This class holds all parameters defined by user.
        @author Albert Lis & Adrian Czupak
    """
    def __init__(self, parameters):
        """! The user defined parameters class initializer.
        @param[in] parameters The dictonary with user defined parameters.
        @return  An instance of the IHSParameters class initialized with the specified parameters.
        @warning The parameters dictonary has to have 9 key-vaule pairs. Example:
        @code{.json}
        {
            'function': 'x1 + x2',
            'iterations': 50000,
            'hms': 10,
            'hcmrmin': 0.5,
            'hcmrmax': 0.75,
            'parmin': 0.2,
            'parmax': 0.8,
            'bwmin': 0.1,
            'bwmax': 2.0
        }
        @endcode
        """
        assert len(parameters) == 9
        self.__varUpperBounds = []
        self.__varLowerBounds = []
        self.__setHMCR([parameters['hcmrmin'], parameters['hcmrmax']])
        self.__setPAR([parameters['parmin'], parameters['parmax']])
        self.__setBW([parameters['bwmin'], parameters['bwmax']])
        self.__setHMS(parameters['hms'])
        self.__setNumOfIterations(parameters['iterations'])
        self.__setVariables(VariablesParser(parameters['function']).getVariables())
        self.__setDefaultBounds()
        self.__setFunction(parameters['function'])

    def updateHMCR(self, generation):
        """! The function for updating current HMCR parameter.
            @brief This function is used for calculate new evolutive harmony memory change rate parameter.
            @param[in] generation Integer of the current generation number.
        """
        self._HMCR = (self._HMCRmax - generation *
                      (self._HMCRmax - self._HMCRmin) / self._NumOfIterations)

    def updatePAR(self, generation):
        """! The function for updating current PAR parameter.
            @brief This function is used for calculate new evolutive pitch adjustment ratio parameter.
            @param[in] generation Integer of the current generation number.
        """
        self._PAR = (self._PARmin + generation *
                     (self._PARmax - self._PARmin) / len(self.__variables))

    def updateBW(self, generation):
        """! The function for updating current BW parameter.
            @brief This function is used for calculate new evolutive distance bandwidth parameter.
            @param[in] generation Integer of the current generation number.
        """
        c = log(self._BWmin / self._BWmax)
        self._BW = self._BWmax * exp(generation * c)

    def __setHMCR(self, HMCRRange):
        """! Setter of HMCR range.
            @brief This function is used to set harmony memory change rate range.
            @param[in] HMCRRange List with user defined harmony memory change rate bounds.
        """
        self.__setPair('HMCR', 0, 1, HMCRRange)

    def __setPAR(self, PARRange):
        """! Setter of PAR range.
            @brief This function is used to set pitch adjustment ratio range.
            @param[in] PARRange List with user defined pitch adjustment ratio bounds.
        """
        self.__setPair('PAR', 0, 1, PARRange)

    def __setBW(self, BWRange):
        """! Setter of BW range.
            @brief This function is used to set distance bandwidth range.
            @param[in] BWRange List with user defined distance bandwidth bounds.
        """
        self.__setPair('BW', 1e-20, 1e20, BWRange)

    def __setNumOfIterations(self, NumOfIterations):
        """! Setter of number of algorithm iterations value.
            @brief This function is used to set algorithm iterations value.
            @param[in] NumOfIterations Integer with number of algorithm iterations.
        """
        self.__setInteger('NumOfIterations', NumOfIterations)

    def __setHMS(self, HMS):
        """! Setter of number of HMS value.
            @brief This function is used to set harmony memory size.
            @param[in] NumOfIterations Integer with harmony memory size.
        """
        self.__setInteger('HMS', HMS)

    def __setPair(self, parameter, minLimit, maxLimit, inputList):
        """! Setter of range of parameters.
            @brief This function is used to create class attributes with min/max values of given parameter.
            @param[in] parameter String with name of parameter.
            @param[in] minLimit Float with acceptable minimal value of parameter.
            @param[in] maxLimit Float with acceptable maximal value of parameter.
            @param[in] inputList List with user defined min/max values.
        """
        assert len(inputList) == 2, parameter + " input list has wrong size"
        assert isinstance(inputList[0], float) and isinstance(inputList[1], float), parameter + \
                                                                                    " should be a pair of floats"
        try:
            parameterMin = float(inputList[0])
            parameterMax = float(inputList[1])
        except ValueError:
            raise ValueError(parameter + " its floats but something went wrong")

        assert parameterMin >= minLimit, parameter + ": parameterMin should be >= minLimit"
        assert parameterMin <= maxLimit, parameter + ": parameterMin should be <= maxLimit"
        assert parameterMax <= maxLimit, parameter + ": parameterMax should be <= maxLimit"
        assert parameterMax >= minLimit, parameter + ": parameterMax should be >= minLimit"
        assert parameterMin <= parameterMax, parameter + ": parameterMin should be <= parameterMax"
        exec('self._' + parameter + 'max = parameterMax')
        exec('self._' + parameter + 'min = parameterMin')

    def __setInteger(self, parameter, value):
        """! Setter of integer parameters.
            @brief This function is used to create class attributes that are integers.
            @param[in] parameter String with name of parameter.
            @param[in] value Integer with user defined value.
        """
        assert isinstance(value, int), f'{parameter} should be an integer'
        assert value >= 1, f'{parameter} should be bigger than 1'
        exec('self._' + parameter + ' = value')

    def __setVariables(self, variables):
        """! Setter of variables.
            @brief This function is used to set variables extracted from user defined function.
            @param[in] variables List with variables.
        """
        self.__variables = variables

    def __setFunction(self, inputBoxExpression):
        """! Setter of lambdas with user defined function.
            @brief This function is used to set lambdas used to calculate values of user defined function.
            @param[in] inputBoxExpression String with raw function.
        """
        strOfVars = ''
        strOfVarsFinal = ''
        for var in self.__variables:
            strOfVars += var
            strOfVarsFinal += "X['" + var + "']"
            if var != self.__variables[-1]:
                strOfVars += ', '
                strOfVarsFinal += ', '
        self.__objective_function = eval('lambda ' + strOfVars + ': ' + inputBoxExpression)
        self.compute = eval('lambda self, X: self._objective_function(%s)' % strOfVarsFinal)

    def setBounds(self, index, lower, upper):
        """! Setter of bounds of variables.
            @brief This function is used to set variables bounds.
            @param[in] index The index  of variable.
            @param[in] lower The lower bound of variable.
            @param[in] upper The upper bound of variable.
        """
        assert lower < upper, 'Lower bound should be < upper bound'
        assert isinstance(index, int), 'index has to be a integer'
        assert index >= 0, 'index has to be > 0'
        if len(self.__varLowerBounds) <= index:
            self.__varLowerBounds.append(lower)
            self.__varUpperBounds.append(upper)
        else:
            self.__varLowerBounds[index] = lower
            self.__varUpperBounds[index] = upper

    def __setDefaultBounds(self):
        """! Default setter of extracted variables bounds.
            @brief This function is used to set default values of extracted variables bounds.
        """
        for i in range(len(self.__variables)):
            self.setBounds(i, -10, 10)

    def getBounds(self):
        """! Getter of bounds of variables.
            @brief This function is used to get variables bounds.
            @return Two lists. First with lower and second with upper bounds of variables.
        """
        return self.__varLowerBounds, self.__varUpperBounds

    def getFunction(self):
        """! Getter of function.
            @brief This function is used to get function.
            @return String containing function
        """
        return self.__objective_function

    def getHMS(self):
        """! Getter of HMS.
            @brief This function is used to get harmony memory size.
            @return Integer of size of harmony memory
        """
        return self._HMS

    def getObjectiveFunction(self):
        """! Getter of objective function.
            @brief This function is used to get lambda used for calculation values of user defined function.
            @return Lambda objective function.
        """
        return self.__objective_function

    def getCompute(self):
        """! Getter of compute lambda.
            @brief This function is used to get lambda used for calculation values of user defined function.
            @return Lambda compute function.
        """
        return self.compute

    def getVariables(self):
        """! Getter of objective function.
            @brief This function is used to get variables extracted from user defined function.
            @return List of variables extracted from user defined function.
        """
        return self.__variables

    def getPAR(self):
        """! Getter of PAR parameter.
            @brief This function is used to get calulated pitch adjustment rate parameter.
            @return Float of pitch adjustment rate parameter.
        """
        return self._PAR

    def getBW(self):
        """! Getter of BW parameter.
            @brief This function is used to get calculated distance bandwidth parameter.
            @return Float of distance bandwidth parameter.
        """
        return self._BW

    def getNumOfIterations(self):
        """! Getter of number of algorithm iterations.
            @brief This function is used to get user defined number of algorithm iterations.
            @return Integer of number of algorithm iterations.
        """
        return self._NumOfIterations

    def getHMCR(self):
        """! Getter of HMCR parameter.
            @brief This function is used to calculated get harmony memory change rate parameter.
            @return Float of harmony memory change rate parameter.
        """
        return self._HMCR

    def getHMCRRange(self):
        """! Getter of user defined HMCR range.
            @brief This function is used to get user defined harmony memory change rate range.
            @return Two float values. First with harmony memory change rate lower bound, second with
                    harmony memory change rate upper bound.
        """
        return self._HMCRmin, self._HMCRmax

    def getPARRange(self):
        """! Getter of user defined PAR range.
            @brief This function is used to get user defined pitch adjustment rate range.
            @return Two float values. First with pitch adjustment rate lower bound, second with pitch
                    adjustment rate upper bound.
        """
        return self._PARmin, self._PARmax

    def getBWRange(self):
        """! Getter of user defined BW range.
            @brief This function is used to get user defined distance bandwidth range.
            @return Float of distance bandwidth range.
        """
        return self._BWmin, self._BWmax

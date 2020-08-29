from math import log, exp
from VariablesParser import VariablesParser


class IHSParameters:
    def __init__(self, parameters):
        assert len(parameters) == 9
        self._varUpperBounds = []
        self._varLowerBounds = []
        self.setHMCR([parameters['hcmrmin'], parameters['hcmrmax']])
        self.setPAR([parameters['parmin'], parameters['parmax']])
        self.setBW([parameters['bwmin'], parameters['bwmax']])
        self.setHMS(parameters['hms'])
        self.setNumOfIterations(parameters['iterations'])
        self.setVariables(parameters['function'])
        self._setDefaultBounds()
        self.setFunction(parameters['function'])

    def updateHMCR(self, generation):
        self._HMCR = (self._HMCRmax - generation *
                      (self._HMCRmax - self._HMCRmin) / self._NumOfIterations)

    def updatePAR(self, generation):
        self._PAR = (self._PARmin + generation *
                     (self._PARmax - self._PARmin) / len(self._variables))

    def updateBW(self, generation):
        c = log(self._BWmin / self._BWmax)
        self._BW = self._BWmax * exp(generation * c)

    def setHMCR(self, HMCR):
        self._setPair('HMCR', 0, 1, HMCR)

    def setPAR(self, PAR):
        self._setPair('PAR', 0, 1, PAR)

    def setBW(self, BW):
        self._setPair('BW', 1e-20, 1e20, BW)

    def setNumOfIterations(self, NumOfIterations):
        self._setInteger('NumOfIterations', NumOfIterations)

    def setHMS(self, HMS):
        self._setInteger('HMS', HMS)

    def _setPair(self, parameter, minLimit, maxLimit, inputList):
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

    def _setInteger(self, parameter, value):
        try:
            value = int(value)
        except:
            raise Exception(parameter + " should be an integer")

        if value <= 1:
            raise Exception(parameter + " should be bigger than 1")
        else:
            exec('self._' + parameter + ' = value')

    def setVariables(self, expression, constants={}):
        try:
            p = VariablesParser(expression, constants)
            variables = p.getVariables()
            self._variables = variables
        except Exception as ex:
            # messageBox
            print(ex.args)

    def setFunction(self, inputBoxExpression):
        strOfVars = ''
        strOfVarsFinal = ''
        for var in self._variables:
            strOfVars += var
            strOfVarsFinal += "X['" + var + "']"
            if var != self._variables[-1]:
                strOfVars += ', '
                strOfVarsFinal += ', '
        self._objective_function = eval('lambda ' + strOfVars + ': ' + inputBoxExpression)
        self.compute = eval('lambda self, X: self._objective_function(%s)' % strOfVarsFinal)

    def setBounds(self, index, lower, upper):
        if len(self._varLowerBounds) <= index:
            self._varLowerBounds.append(lower)
            self._varUpperBounds.append(upper)
        else:
            self._varLowerBounds[index] = lower
            self._varUpperBounds[index] = upper

    def _setDefaultBounds(self):
        for i in range(len(self._variables)):
            self.setBounds(i, -10, 10)

    def getBounds(self):
        return self._varLowerBounds, self._varUpperBounds

    def getFunction(self):
        return self._objective_function

    def getHMS(self):
        return self._HMS

    def getObjectiveFunction(self):
        return self._objective_function

    def getCompute(self):
        return self.compute

    def getVariables(self):
        return self._variables

    def getPAR(self):
        return self._PAR

    def getBW(self):
        return self._BW

    def getNumOfIterations(self):
        return self._NumOfIterations

    def getHMCR(self):
        return self._HMCRmin, self._HMCRmax

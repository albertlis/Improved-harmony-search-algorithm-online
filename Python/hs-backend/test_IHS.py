import pytest
from IHS import IHSAlgorithm

@pytest.fixture(scope='module')
def parameters():
    parameters = dict()
    parameters['hcmrmin'] = 0.1
    parameters['hcmrmax'] = 0.8
    parameters['parmin'] = 0.1
    parameters['parmax'] = 0.9
    parameters['bwmin'] = 0.1
    parameters['bwmax'] = 2.0
    parameters['hms'] = 5
    parameters['iterations'] = 100
    parameters['function'] = 'pow(x,2)'
    yield parameters

@pytest.fixture(scope='module')
def ihs(parameters):
    ihs = IHSAlgorithm(parameters)
    yield ihs

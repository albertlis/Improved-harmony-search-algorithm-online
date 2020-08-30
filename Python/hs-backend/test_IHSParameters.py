import pytest
from IHSParameters import IHSParameters


@pytest.fixture(scope='function')
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
def ihsParameters(parameters):
    ihsParameters = IHSParameters(parameters)
    yield ihsParameters


@pytest.mark.parametrize("hcmrmin,message", [
    (2.0,  'HMCR: parameterMin should be <= maxLimit'),
    (-1.1,  'HMCR: parameterMin should be >= minLimit'),
    (1,  'HMCR should be a pair of floats'),
    ('abc',  'HMCR should be a pair of floats')
])
def test_HMCRmin(hcmrmin, message, parameters):
    with pytest.raises(AssertionError, match=message):
        parameters['hcmrmin'] = hcmrmin
        IHSParameters(parameters)


@pytest.mark.parametrize("hcmrmax,message", [
    (1.1,  'HMCR: parameterMax should be <= maxLimit'),
    (-2.0,  'HMCR: parameterMax should be >= minLimit'),
    (1,  'HMCR should be a pair of floats'),
    ('abc',  'HMCR should be a pair of floats')
])
def test_HMCRmax(hcmrmax, message, parameters):
    with pytest.raises(AssertionError, match=message):
        parameters['hcmrmax'] = hcmrmax
        IHSParameters(parameters)


def test_HCMRminmax(parameters):
    with pytest.raises(AssertionError, match='HMCR: parameterMin should be <= parameterMax'):
        parameters['hcmrmin'] = 0.9
        parameters['hcmrmax'] = 0.1
        IHSParameters(parameters)

    parameters['hcmrmin'] = 0.499
    parameters['hcmrmax'] = 0.999
    hmcr = IHSParameters(parameters).getHMCR()
    assert hmcr[0] == 0.499
    assert hmcr[1] == 0.999


@pytest.mark.parametrize("parmin,message", [
    (2.0,  'PAR: parameterMin should be <= maxLimit'),
    (-1.1,  'PAR: parameterMin should be >= minLimit'),
    (1,  'PAR should be a pair of floats'),
    ('abc',  'PAR should be a pair of floats')
])
def test_PARmin(parmin, message, parameters):
    with pytest.raises(AssertionError, match=message):
        parameters['parmin'] = parmin
        IHSParameters(parameters)


@pytest.mark.parametrize("parmax,message", [
    (1.1,  'PAR: parameterMax should be <= maxLimit'),
    (-2.0,  'PAR: parameterMax should be >= minLimit'),
    (1,  'PAR should be a pair of floats'),
    ('abc',  'PAR should be a pair of floats')
])
def test_PARmax(parmax, message, parameters):
    with pytest.raises(AssertionError, match=message):
        parameters['parmax'] = parmax
        IHSParameters(parameters)


def test_PARminmax(parameters):
    with pytest.raises(AssertionError, match='PAR: parameterMin should be <= parameterMax'):
        parameters['parmin'] = 0.9
        parameters['parmax'] = 0.1
        IHSParameters(parameters)

    parameters['parmin'] = 0.499
    parameters['parmax'] = 0.999
    par = IHSParameters(parameters).getPAR()
    assert par[0] == 0.499
    assert par[1] == 0.999


@pytest.mark.parametrize('bwmin', [1, 'abc'])
def test_BWmin(bwmin, parameters):
    with pytest.raises(AssertionError, match='BW should be a pair of floats'):
        parameters['bwmin'] = bwmin
        IHSParameters(parameters)


@pytest.mark.parametrize('bwmax', [1, 'abc'])
def test_BWmin(bwmax, parameters):
    with pytest.raises(AssertionError, match='BW should be a pair of floats'):
        parameters['bwmax'] = bwmax
        IHSParameters(parameters)


def test_BWminmax(parameters):
    bw = IHSParameters(parameters).getBW()
    assert bw[0] == parameters['bwmin']
    assert bw[1] == parameters['bwmax']

    with pytest.raises(AssertionError, match='BW: parameterMax should be >= minLimit'):
        parameters['bwmin'] = 1.0
        parameters['bwmax'] = -1.0
        IHSParameters(parameters)

@pytest.mark.parametrize('iterations,message', [
    (-1, 'NumOfIterations should be bigger than 1'),
    (2.5, 'NumOfIterations should be an integer')
])
def test_NumOfIterations(iterations, message, parameters):
    with pytest.raises(Exception, match=message):
        parameters['iterations'] = iterations
        IHSParameters(parameters)
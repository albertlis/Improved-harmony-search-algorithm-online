import pytest
from IHSParameters import IHSParameters


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
def ihsParameters(parameters):
    ihsParameters = IHSParameters(parameters)
    yield ihsParameters

def test_HMCR(parameters):
    params = parameters.copy()
    with pytest.raises(AssertionError, match='HMCR: parameterMin should be <= maxLimit'):
        params['hcmrmin'] = 2.0
        IHSParameters(params)
    with pytest.raises(AssertionError, match='HMCR: parameterMin should be >= minLimit'):
        params['hcmrmin'] = -1.1
        IHSParameters(params)

    params = parameters.copy()
    with pytest.raises(AssertionError, match='HMCR: parameterMax should be <= maxLimit'):
        params['hcmrmax'] = 1.1
        IHSParameters(params)
    with pytest.raises(AssertionError, match='HMCR: parameterMax should be >= minLimit'):
        params['hcmrmax'] = -2.0
        IHSParameters(params)

    with pytest.raises(AssertionError, match='HMCR: parameterMin should be <= parameterMax'):
        params['hcmrmin'] = 0.9
        params['hcmrmax'] = 0.1
        IHSParameters(params)

    with pytest.raises(AssertionError, match='HMCR should be a pair of floats'):
        params['hcmrmin'] = 1
        IHSParameters(params)
    with pytest.raises(AssertionError, match='HMCR should be a pair of floats'):
        params['hcmrmax'] = 'abc'
        IHSParameters(params)

    params = parameters.copy()
    params['hcmrmin'] = 0.499
    params['hcmrmax'] = 0.999
    hmcr = IHSParameters(params).getHMCR()
    assert hmcr[0] == 0.499
    assert hmcr[1] == 0.999

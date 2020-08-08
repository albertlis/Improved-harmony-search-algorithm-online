# !/usr/bin/python3
import json

from flask import Flask, jsonify, request
from flask_api import status
from flask_cors import CORS, cross_origin

from I_IHS import I_IHSAlgorithm
from VariablesParser import evaluateError, VariablesParser
import numpy as np
from waitress import serve

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/checkfunction', methods=['GET'])
@cross_origin()
def checkFunction():
    function = request.args.get('function', type=str).replace(' ', '+')
    message, error = evaluateError(function)
    if error:
        return jsonify(message=message), status.HTTP_400_BAD_REQUEST
    p = VariablesParser(function)
    variables = p.getVariables()
    return jsonify(message=message, variables=variables), status.HTTP_200_OK


@app.route('/calculate', methods=['GET'])
@cross_origin()
def calculateFunction():
    algorithmParameters = extractAlgorithmParameters()
    print(algorithmParameters['iterations'])
    message, error = evaluateError(algorithmParameters['function'])
    if error:
        return jsonify(message=message), status.HTTP_400_BAD_REQUEST
    p = VariablesParser(algorithmParameters['function'])
    variables = p.getVariables()
    variablesBandwidth = getVariablesBandwidth(variables)
    ihs = I_IHSAlgorithm(algorithmParameters)
    for i, variable in enumerate(variables):
        ihs.setBounds(i, variablesBandwidth[variable+'min'], variablesBandwidth[variable+'max'])
    try:
        ihs.doYourTask()
        functionValue, optimalVariables = ihs.getOptimalSolution()
        lastBestSolutionIteration = ihs.getLastBestSolutionIteration()
        trace = convertTrace(ihs.getTrace())

        Z = getZMatrix(ihs)
        return json.dumps({'functionValue': functionValue, 'optimalVariables': optimalVariables,
                           'iterations': lastBestSolutionIteration, 'trace': trace, 'Z': Z}), \
               status.HTTP_201_CREATED
    except ZeroDivisionError as e:
        print(e)
        return status.HTTP_400_BAD_REQUEST


def getZMatrix(ihs):
    lowBounds, upBounds = ihs.getBounds()
    x = np.linspace(lowBounds[0], upBounds[0], 50)
    y = np.linspace(lowBounds[1], upBounds[1], 50)
    Z = np.empty(shape=(len(x), len(y)))
    function = ihs.getFunction()
    for i in range(len(x)):
        for j in range(len(y)):
            val = function(x[i], y[j])
            if val == np.Inf:
                val = 1e+300
            elif val == -np.Inf:
                val = -1e+300
            Z[i][j] = val
    # Z1 = []
    # for sublist in reversed(Z.tolist()):
    #     Z1.append(list(reversed(sublist)))
    # return Z1
    return np.transpose(Z).tolist()


def convertTrace(tempTrace):
    trace = dict()
    for key in tempTrace[0].keys():
        tr = list()
        for point in tempTrace:
            tr.append(point[key])
        trace[key] = tr
    return trace


def getVariablesBandwidth(variables):
    variableValues = dict()
    for variable in variables:
        minName = variable + 'min'
        maxName = variable + 'max'
        minValue = request.args.get(minName, type=float)
        maxValue = request.args.get(maxName, type=float)
        variableValues[minName] = minValue
        variableValues[maxName] = maxValue
    return variableValues


def extractAlgorithmParameters():
    params = dict()
    params['function'] = request.args.get('function', type=str).replace(' ', '+')
    params['iterations'] = request.args.get('iterations', type=int)
    params['hms'] = request.args.get('hms', type=int)
    params['hcmrmin'] = request.args.get('hcmrmin', type=float)
    params['hcmrmax'] = request.args.get('hcmrmax', type=float)
    params['parmin'] = request.args.get('parmin', type=float)
    params['parmax'] = request.args.get('parmax', type=float)
    params['bwmin'] = request.args.get('bwmin', type=float)
    params['bwmax'] = request.args.get('bwmax', type=float)
    return params


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=80)
# !/usr/bin/python3
import json

from flask import Flask, jsonify, request
from flask_api import status
from flask_cors import CORS, cross_origin

from I_IHS import I_IHSAlgorithm
from VariablesParser import evaluateError, VariablesParser

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/checkfunction', methods=['GET'])
@cross_origin()
def checkFunction():
    # Example query:
    # ?function=(x+e*10)/y&iterations=1000&hms=10&hcmrmin=0.5&hcmrmax=0.75&parmin=0.2&parmax=0.8&bwmin=1&bwmax=2
    # parameters = extractAlgorithmParameters()
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
        trace = ihs.getTrace()
        return json.dumps({'functionValue': functionValue, 'optimalVariables': optimalVariables,
                           'iterations': lastBestSolutionIteration, 'trace': trace}), \
               status.HTTP_201_CREATED
    except ZeroDivisionError as e:
        print(e)
        return status.HTTP_400_BAD_REQUEST


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


app.run(debug=True, use_reloader=False)

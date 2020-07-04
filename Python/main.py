# !/usr/bin/python3
from flask import Flask, jsonify, request
from flask_api import status
from flask_cors import CORS

from VariablesParser import evaluateError, VariablesParser

app = Flask(__name__)
CORS(app)

@app.route('/checkfunction', methods=['GET'])
def checkFunction():
    # Example query:
    # ?function=(x+e*10)/y&iterations=1000&hms=10&hcmrmin=0.5&hcmrmax=0.75&parmin=0.2&parmax=0.8&bwmin=1&bwmax=2
    parameters = extractParameters()
    message, error = evaluateError(parameters['function'])
    if error:
        return jsonify(message=message), status.HTTP_400_BAD_REQUEST
    p = VariablesParser(parameters['function'])
    variables = p.getVariables()
    return jsonify(message=message, variables=variables), status.HTTP_200_OK


def extractParameters():
    params = dict()
    params['function'] = request.args.get('function', type=str)
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

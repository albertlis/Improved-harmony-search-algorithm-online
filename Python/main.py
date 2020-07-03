# !/usr/bin/python3
from flask import Flask, jsonify, request
from flask_api import status

app = Flask(__name__)


@app.route('/compute', methods=['GET'])
def compute():
    # ?function=(x+e*10)/y&iterations=1000&hms=10&hcmrmin=0.5&hcmrmax=0.75&parmin=0.2&parmax=0.8&bwmin=1&bwmax=2
    function = request.args.get('function', type=str)
    iterations = request.args.get('iterations', type=int)
    hms = request.args.get('hms', type=int)
    hcmrmin = request.args.get('hcmrmin', type=float)
    hcmrmax = request.args.get('hcmrmax', type=float)
    parmin = request.args.get('parmin', type=float)
    parmax = request.args.get('parmax', type=float)
    bwmin = request.args.get('bwmin', type=float)
    bwmax = request.args.get('bwmax', type=float)
    return jsonify(function=function, iterations=iterations, hms=hms, hcmrmin=hcmrmin,
                   hcmrmax=hcmrmax, parmin=parmin, parmax=parmax, bwmin=bwmin, bwmax=bwmax), \
           status.HTTP_200_OK


app.run(debug=True, use_reloader=False)

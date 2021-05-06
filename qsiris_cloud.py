import sys

import json

# Make sure flask is installed
from flask import request
from flask import jsonify
from flask import make_response
from flask import Flask
from flask import render_template

from qsiris_api import execute_qiskit, decompose_qiskit,real_device_qiskit

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template('test_server.html')


@app.route("/QO_QK_convertor", methods=["POST"])
def qo_qk():

    # data = json.loads(request.form.get('jsonfile'))
    file = request.files['jsonfile']
    puz = None
    try:
        puz = json.load(file)
        print(puz, file=sys.stderr)
    except:
        return "Not json file", 400

    s_counts = execute_qiskit(puz)
    qasm_circuit,qiskit_circuit = decompose_qiskit(puz)

    result = {"simulated_counts": s_counts, "qasm_circuit": qasm_circuit, "qiskit_circuit":qiskit_circuit,}
    #print('\n \n ##################')
    #print(result)
    #print('\n \n ##################')
    res = make_response(jsonify(result), 200)

    #print(res)
    return res



@app.route("/QO_QK_real", methods=["POST"])
def qk_real():
    if request.is_json:
        req = request.get_json()
        return real_device_qiskit(req)
    else:
        return "Not json fie", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

# http://127.0.0.1:8008/execute_qiskit?circuit_file=GROVER-14-14.qpf
# http://127.0.0.1:8008/do_qiskit_test

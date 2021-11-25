import sys

import json

# Make sure flask is installed
from flask import request
from flask import jsonify
from flask import make_response
from flask import Flask
from flask import render_template

from qsiris_api import execute_qiskit, decompose_qiskit,real_device_qiskit,qiskit_extraction

app = Flask(__name__)

@app.route("/")
def welcome():
    return render_template('test_server.html')

@app.route("/QK_QO", methods=["POST"])
def qk_qo():
    if request:
        req = request.data
        print("!!!!!")
        print("request:",req)
        print("!!!!!")
        return qiskit_extraction(req)
    else:
        return "Not qc circui fie", 400


    

@app.route("/QO_QK_convertor", methods=["POST"])
def qo_qk():
    print("/QO_QK_convertor")
    try:
        data = request.get_json()
        #file = request.files['jsonfile']
        #print(data)
        puz = None
        try:
            #puz = json.load(file)
            print(puz, file=sys.stderr)
            puz = data
        except:
            return "Not json file", 300
        
        
        if int(puz["QiskitShotsUsed"])>1000:
            print("QiskitShotsUsed:",puz["QiskitShotsUsed"])
            return "Maximum nr of QiskitShotsUsed >1000 !", 400
            

        s_counts = execute_qiskit(puz)
        
        qasm_circuit,qiskit_circuit = decompose_qiskit(puz)

        result = {"simulated_counts": s_counts, "qasm_circuit": qasm_circuit, "qiskit_circuit":qiskit_circuit,}
        print('\n \n ##################')
        print("Result: ",result)
        print('\n \n ##################')
        res = make_response(jsonify(result), 200)
        return res
    except Exception as e:
        print("Exception e ",e)
        file = request.files['jsonfile']
        puz = None
        try:
            puz = json.load(file)
            print(puz, file=sys.stderr)
        except:
            return "Not json file", 300



        decompose = decompose_qiskit(puz)

        result = {"simulated_counts": s_counts, "qasm_circuit": decompose}

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
    app.run(host="192.168.0.107", port=591)

# http://127.0.0.1:8008/execute_qiskit?circuit_file=GROVER-14-14.qpf
# http://127.0.0.1:8008/do_qiskit_test

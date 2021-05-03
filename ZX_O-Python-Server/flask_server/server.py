from flask import request
from flask import jsonify
from flask import make_response
from flask import Flask

from api import execute_qiskit, decompose_qiskit,real_device_qiskit

app = Flask(__name__)


@app.route("/")
def welcome():
    return "Hi little spider!"


@app.route("/QO_QK_convertor", methods=["POST"])
def qo_qk():

    if request.is_json:
        req = request.get_json()
        s_counts = execute_qiskit(req)
        decompose = decompose_qiskit(req)
        result = {"simulated_counts": s_counts, "qasm_circuit": decompose}

        res = make_response(jsonify(result), 200)
        return res
    else:
        return "Not json fie", 400

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

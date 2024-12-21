from qiskit import transpile
# from qiskit import QuantumCircuit
# from qiskit import IBMQ
# from qiskit.tools.monitor import job_monitor
from qiskit_aer import AerSimulator
from project_qsiris.conversion_qo_qiskit import *
import base64
import zlib

import logging



def decompress_string(compressed_data: str) -> str:
    """
    Decompress a compressed and possibly Base64-encoded string.

    Args:
        compressed_data (str): The compressed string, optionally Base64 encoded.

    Returns:
        str: The decompressed string.

    Raises:
        ValueError: If the input data cannot be decompressed.
    """
    try:
        # Attempt Base64 decoding first (if applicable)
        try:
            compressed_data = base64.b64decode(compressed_data)
        except Exception:
            pass  # Assume it's already raw compressed data

        # Decompress using zlib
        decompressed_data = zlib.decompress(compressed_data, zlib.MAX_WBITS | 16)

        # Decode to a readable string
        return decompressed_data.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Failed to decompress string: {e}") from e

def parse_json_string(json_string):
    """
    Converts a JSON string into a Python list of dictionaries.

    Parameters:
        json_string (str): The JSON string to be converted.

    Returns:
        list: A list of dictionaries parsed from the JSON string.

    Raises:
        ValueError: If the input string is not valid JSON.
    """
    # Replace JavaScript-style keywords with Python equivalents
    json_string = json_string.replace('true', 'True').replace('false', 'False').replace('null', 'None')

    try:
        # Parse the JSON string into Python objects
        return eval(json_string)
    except SyntaxError as e:
        raise ValueError("Invalid JSON string: {}".format(e))

def proces_zip(res):
    print(res)
    #res=res["puzzles"][0]
    print(res.keys())

    pgs=parse_json_string(decompress_string(res["puzzleGateSlots"]))
    print("tiiis",type(pgs))
    g_list=[[] for _ in range(res["qubitCapacity"])]
    for g in pgs:
        print(g["CircuitPosition"]["Item2"])
        g_list[g["CircuitPosition"]["Item1"]].append(g)
    print(pgs)
    new_res={
        "PuzzleDefinition":{
            "QubitCapacity":res["qubitCapacity"],

        },
        "PuzzleGates": g_list
    }

    return new_res


def qiskit_test():

    # test circuit
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    circ.measure_all()


    simulator = AerSimulator()
    compiled_circuit = transpile(circ, simulator)
    sim_result = simulator.run(compiled_circuit, shots=100).result()
    counts = sim_result.get_counts()

    return counts


def execute_qiskit(res):



    process_puzzle = proces_zip(res)

    qc = odyssey_to_qiskit(process_puzzle, incl_initial_state=False,
                           incl_all_measurements=True)

    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    sim_result = simulator.run(compiled_circuit, shots=100).result()
    counts = sim_result.get_counts()

    return counts


def decompose_qiskit(res):
    process_puzzle = proces_zip(res)
    qc = odyssey_to_qiskit(process_puzzle,
                           incl_initial_state=False,
                           use_barrier=True,
                           incl_all_measurements=True)
    try:
        qasm_circuit = qc.qasm()
    except:
        qasm_circuit = (
            "The matrix is not unitary."
            " At the moment the error is probably caused by the fact that "
            "the numbers do not have enough decimals"
        )

    return qasm_circuit

#
# def real_device_qiskit(res):
#
#     IBMQ.load_account()
#     provider = IBMQ.get_provider('ibm-q')
#     ibmq_lima = provider.get_backend("ibmq_lima")
#
#     qc = odyssey_to_qiskit(res,
#                            incl_initial_state=False,
#                            use_barrier=True,
#                            incl_all_measurements=True)
#
#     try:
#         qasm_circuit = qc.qasm()
#         job=execute(qc, backend=ibmq_lima, shots=100)
#         job_monitor(job)
#         result = job.result()
#         counts = result.get_counts()
#
#     except:
#         qasm_circuit = (
#             "The matrix is not unitary."
#             " At the moment the error is probably caused by the fact that "
#             "the numbers do not have enough decimals"
#         )
#     result = {"ibmq_lima_counts": counts, "qasm_circuit": qasm_circuit}
#     return result

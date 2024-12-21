import numpy as np
import base64
import zlib
from qiskit import QuantumRegister, QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

from project_qsiris.conversion_qo_qiskit import odyssey_to_qiskit, load_oddysey_puzzle
from project_qsiris.conversion_qiskit_qo import qiskit_to_odyssey, save_odyssey_puzzle

"""
    Odyssey to Qiskit
"""
path = "/Users/voicutomut/Documents/GitHub/Qsiris-Quantum-Odyssey-and-Qiskit/circuits/odyssey_circuits/New_Superposition_Challenge__Explore_Infinite_Flavors.qpf"#"circuits/qiskit_to_odyssey/example_002.qpf"

puzzle = load_oddysey_puzzle(path)



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


import json


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
    res=res["puzzles"][0]
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

process_puzzle=proces_zip(puzzle)


qc = odyssey_to_qiskit(process_puzzle, incl_initial_state = False,
                       incl_all_measurements=True)
# qc.draw('mpl')

simulator = AerSimulator()
compiled_circuit = transpile(qc, simulator)
sim_result = simulator.run(compiled_circuit, shots=1000).result()
counts = sim_result.get_counts()
plot_histogram(counts)

print("Odyssey to Qiskit done!")


"""
    Qiskit to Odyssey
"""

qreg_q = QuantumRegister(3, 'q')
circuit = QuantumCircuit(qreg_q)

circuit.cx(qreg_q[1], qreg_q[2])
circuit.h(qreg_q[1])
circuit.z(qreg_q[2])
circuit.u(np.pi/7, np.pi/3, np.pi/5, qreg_q[0])

# circuit.draw('mpl')

puzzle = qiskit_to_odyssey(circuit, puzzle_type="General")
save_odyssey_puzzle(puzzle, 'example_001')
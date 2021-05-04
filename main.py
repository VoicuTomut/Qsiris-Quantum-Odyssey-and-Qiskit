import numpy as np
import cmath

from qiskit import QuantumCircuit, transpile
from qiskit import Aer, execute
from qiskit import IBMQ
from qiskit.tools.monitor import job_monitor
from qiskit.visualization import plot_histogram

from project_qsiris.conversion_qo_qiskit import puzzle_to_circuit, add_gates, odyssey_get_nr_q


"""
    Odyssey to Qiskit
"""
#Step 1: read the puzzle is like a python dictionary

path = "circuits/qiskit_to_odyssey/example_002.qpf"
# puzzle = read_circuit(path)

#Step 2: convert your puzzle to a Qiskit circuit

qc = puzzle_to_circuit(path, initial_state=False)
qc.measure_all()
qc.draw('mpl')

#Step 3: Runn your puzzle on a qiskit simulator

backend = Aer.get_backend('qasm_simulator')
job = execute(qc, backend,shots=1000)
result = job.result()
counts = result.get_counts()
plot_histogram(counts)


"""
    Qiskit to Odyssey
"""

import numpy as np

from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from qiskit.compiler import transpile


import matplotlib.pyplot as plt
import matplotlib.image as mpimg


from project_qsiris.conversion_qiskit_qo import circuit_to_puzzle, save_puzzle

qreg_q = QuantumRegister(3,'q')
circuit = QuantumCircuit(qreg_q)

circuit.cx(qreg_q[1],qreg_q[2])


circuit.h(qreg_q[1])
circuit.z(qreg_q[2])
circuit.u(np.pi/7, np.pi/3, np.pi/5, qreg_q[0])


circuit.draw('mpl')

puzzle = circuit_to_puzzle(circuit, puzzle_type="General")
save_puzzle(puzzle, 'example_001' )
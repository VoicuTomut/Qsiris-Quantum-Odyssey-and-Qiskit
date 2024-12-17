import numpy as np

from qiskit import QuantumRegister, QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

from project_qsiris.conversion_qo_qiskit import odyssey_to_qiskit, load_oddysey_puzzle
from project_qsiris.conversion_qiskit_qo import qiskit_to_odyssey, save_odyssey_puzzle

"""
    Odyssey to Qiskit
"""
path = "circuits/qiskit_to_odyssey/xy.qpf"#"circuits/qiskit_to_odyssey/example_002.qpf"

puzzle = load_oddysey_puzzle(path)
qc = odyssey_to_qiskit(puzzle, incl_initial_state = False,
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
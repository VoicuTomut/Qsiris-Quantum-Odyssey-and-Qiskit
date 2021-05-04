import json
import numpy as np

from qiskit import QuantumCircuit

import project_qsiris.conversion_gates as conv
from project_qsiris.conversion_intermediates import OdysseyMoment

def get_odyssey_nr_qubits(res):
    """
    :param res: (puzzle)dictionary
    :return: (number of qubits from puzzle)int
    """
    nr_q = res["PuzzleDefinition"]["QubitCapacity"]
    return nr_q


def extract_odyssey_matrix(mat):
    """
    :param mat: matrix  of complex numbers in dictionary form
    :return: matrix ov 'complex' numbers

    #example:
    mat=[[{'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
          {'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}],
         [{'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0},
          {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}]]

    g_mat = extract_odyssey_matrix(mat)
    print("matrice:\n",g_mat)
    """
    mat_conv = []
    for i in mat:
        linie = []
        for j in i:
            linie.append(conv._odyssey_to_complex(j))
        mat_conv.append(linie)

    return mat_conv


def add_odyssey_moment(puzzle_gate, qc):
    """
    :param puzzle_gate: string of gates
    :param qc: QuantumCircuit Qiskit
    Add gates from moment to the  Qiskit circuit
    """

    moment = OdysseyMoment(puzzle_gate)

    if len(moment.control_q) == 0:
        """
            This is the default case
        """
        for qubit in range(moment.nr_q):
            gate_name = moment.original_form[qubit]["GateInSlot"]["Name"]
            if gate_name == "X":
                qc.x(qubit)
            elif gate_name == "Y":
                qc.y(qubit)
            elif gate_name == "Z":
                qc.z(qubit)
            elif gate_name == "H":
                qc.h(qubit)
            elif gate_name == "I":
                qc.id(qubit)
            elif gate_name == "Filler":
                print(
                    "The fillers are empty gates so they will not be converted to qiskit",
                    qubit,
                )
            else:
                unit = extract_odyssey_matrix(
                    moment.original_form[qubit]["GateInSlot"]["DefinitionMatrix"]
                )
                qubits = [k for k in moment.filler_q]
                qubits.append(qubit)
                qc.unitary(unit, qubits, moment.original_form[qubit]["GateInSlot"]["Name"])
                if len(moment.filler_q) > 0:
                    print(
                        "This gate {} is not necessarily converted correctly."
                        " The order of the qubits maybe reversed Please check! ".format(
                            gate_name
                        )
                    )
        return

    """
        If there are controls on the puzzle gate
    """
    for i in range(moment.nr_q):
        if (
            (moment.original_form[i]["GateInSlot"]["Name"] != "CTRL")
            and (moment.original_form[i]["GateInSlot"]["Name"] != "I")
            and (moment.original_form[i]["GateInSlot"]["Name"] != "Filler")
        ):

            control = moment.control_q.copy()
            qubits = [l for l in control]
            for l in range(len(moment.filler_q)):
                qubits.append(moment.filler_q[l])
            qubits.append(i)

            unit = np.identity(2 ** len(qubits), dtype=complex)
            mat = extract_odyssey_matrix(moment.original_form[i]["GateInSlot"]["DefinitionMatrix"])
            """
            unit[-1][-1]=mat[1][1]
            unit[-1][-2]=mat[1][0]
            unit[-2][-1]=mat[0][1]
            unit[-2][-2]=mat[0][0]
            """
            for k in range(1, len(mat) + 1):
                for j in range(1, len(mat) + 1):
                    unit[-k][-j] = mat[-k][-j]

            qc.unitary(
                unit,
                qubits,
                "C "
                + str(moment.control_q)
                + " -> "
                + moment.original_form[i]["GateInSlot"]["Name"]
                + "["
                + str(i)
                + "]",
            )

def odyssey_to_qiskit(path, incl_initial_state = False, use_barrier = False):
    """
    :param path: (puzzle) path to puzzle
    :param initial_state: (initial qubits state ) string of dictionaries
    :return: quantum circuit in qiskit equivalent with the circuit from puzzle
    """

    file = open(path, "r")
    content = file.read()
    puzzle = json.loads(content)

    nr_q = get_odyssey_nr_qubits(puzzle)
    qc = QuantumCircuit(nr_q)

    if incl_initial_state != False:
        qc.initialize(incl_initial_state)

    for puzzle_gate in conv._transpose_list(puzzle["PuzzleGates"]):
        if use_barrier:
            qc.barrier()
        add_odyssey_moment(puzzle_gate, qc)

    return qc

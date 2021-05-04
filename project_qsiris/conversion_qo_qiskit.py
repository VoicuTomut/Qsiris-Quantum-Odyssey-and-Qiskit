import json
import numpy as np

from qiskit import QuantumCircuit

import project_qsiris.conversion_gates as conv


def odyssey_get_nr_q(res):
    """
    :param res: (puzzle)dictionary
    :return: (number of qubits from puzzle)int
    """
    nr_q = res["PuzzleDefinition"]["QubitCapacity"]
    return nr_q


"""
#example:
nr_q=get_nr_q(res)
("Number of qubits:",nr_q)
"""


def get_complex(comp):
    """
    :param comp: complex number as a dictionary
    :return:'complex'
    """
    return comp["Real"] + 1j * comp["Imaginary"]


"""
#example:
comp={'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}
comp_nr=get_complex(comp)
print("Complex number:",comp_nr)
"""


def get_statevector(stv):
    """
    :param stv: vector of complex numbers in dictionary form
    :return: vector of complex numbers
    """
    init_st = []
    for i in stv:
        init_st.append(get_complex(i[0]))
    return init_st


"""
#example:
stv=[[{'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}],
     [{'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}],
     [{'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}],
     [{'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}]]
stat_v=get_statevector(stv)
print(stat_v)
"""


def get_mat(mat):
    """
    :param mat: matrix  of complex numbers in dictionary form
    :return: martix ov 'complex' mubers
    """
    mat_conv = []
    for i in mat:
        linie = []
        for j in i:
            linie.append(get_complex(j))
        mat_conv.append(linie)

    return mat_conv


"""
#example:
mat=[[{'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
      {'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}],
     [{'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0},
      {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}]]

g_mat=get_mat(mat)
print("matrice:\n",g_mat)
"""


class OdysseyMoment:
    def __init__(self, original_form):
        self.original_form = original_form
        self.nr_q = len(self.original_form)
        self.control_q = self.get_control_q()
        self.filler_q = self.get_filler_q()

    def get_control_q(self):
        cq = []
        for j in range(self.nr_q):
            gate_name = self.original_form[j]["GateInSlot"]["Name"]
            if gate_name == "CTRL":
                cq.append(j)

        return cq

    def get_filler_q(self):
        filler = []
        for j in range(self.nr_q):
            gate_name = self.original_form[j]["GateInSlot"]["Name"]
            if gate_name == "Filler":
                filler.append(j)
        return filler


def mat_gate(mat, name):
    """
    :param mat:  unitary matrix
    :param name: ( gate name )str
    :return: qiskit gate
    """
    nr_q = int(np.log2(len(mat)))
    qc = QuantumCircuit(nr_q, name=name)
    qubits = [i for i in range(nr_q)]
    qc.unitary(mat, qubits)
    custom_gate = qc.to_instruction()
    return custom_gate


def add_moment(puzzle_gate, qc):
    """
    :param puzzle_gate: string of gates
    :param qc: QuantumCircuit qiskit
    Add gates from moment to the  qiskit circuit
    """

    moment = OdysseyMoment(puzzle_gate)

    if len(moment.control_q) == 0:
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
                unit = get_mat(
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

    if len(moment.control_q) != 0:
        moment_mat = get_mat(moment.original_form[0]["GateInSlot"]["DefinitionMatrix"])
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
                mat = get_mat(moment.original_form[i]["GateInSlot"]["DefinitionMatrix"])
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


def add_gates(res, qc, barrier=True):
    """
    :param res: (puzzle)dictionary
    :param qc: Qiskit Circuit
    Add gate fro puzzle to qiskit circuit
    """
    mo = 0
    for puzzle_gate in conv._transpose_list(res["PuzzleGates"]):
        mo = mo + 1
        nr_gates_moment = len(puzzle_gate)

        if barrier:
            qc.barrier()

        add_moment(puzzle_gate, qc)


def odyssey_puzzle_to_qiskit_circuit(path, initial_state=False):
    """
    :param path: (puzzle) path to puzzle
    :param initial_state: (initial qubits state ) string of dictionaries
    :return: quantum circuit in qiskit equivalent with the circuit from puzzle
    """

    file = open(path, "r")
    content = file.read()
    puzzle = json.loads(content)

    nr_q = odyssey_get_nr_q(puzzle)
    qc = QuantumCircuit(nr_q)

    if initial_state != False:
        qc.initialize(initial_state)

    add_gates(puzzle, qc, barrier=True)

    return qc

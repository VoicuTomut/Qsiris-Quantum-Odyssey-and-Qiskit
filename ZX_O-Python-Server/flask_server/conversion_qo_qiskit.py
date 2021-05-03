import json

import numpy as np
import cmath

from qiskit import QuantumCircuit, transpile
from qiskit import Aer, execute


def get_nr_q(res):
    nr_q = res["PuzzleDefinition"]["QubitCapacity"]
    return nr_q


"""
#example:
nr_q=get_nr_q(res)
("Number of qubits:",nr_q)
"""


def get_complex(comp):
    return comp["Real"] + 1j * comp["Imaginary"]


"""
#example:
comp={'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}
comp_nr=get_complex(comp)
print("Complex number:",comp_nr)
"""


def get_statevector(stv):
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


def transpose_list(A):
    c = len(A[0])
    l = len(A)

    B = [["" for i in range(l)] for j in range(c)]

    b_c = 0

    for j in range(c):
        for i in range(l):
            B[j][i] = A[i][j]

    return B


class Moment:
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
    nr_q = int(np.log2(len(mat)))
    qc = QuantumCircuit(nr_q, name=name)
    qubits = [i for i in range(nr_q)]
    qc.unitary(mat, qubits)
    custom_gate = qc.to_instruction()
    return custom_gate


def add_moment(moment, qc):
    if len(moment.control_q) == 0:
        for i in range(moment.nr_q):
            if moment.original_form[i]["GateInSlot"]["Name"] == "X":
                qc.x(i)
            elif moment.original_form[i]["GateInSlot"]["Name"] == "Y":
                qc.y(i)
            elif moment.original_form[i]["GateInSlot"]["Name"] == "Z":
                qc.z(i)
            elif moment.original_form[i]["GateInSlot"]["Name"] == "H":
                qc.h(i)
            elif moment.original_form[i]["GateInSlot"]["Name"] == "I":
                qc.id(i)
            elif moment.original_form[i]["GateInSlot"]["Name"] == "Filler":
                print(
                    "The fillers are empty gates so they will not be converted to qiskit",
                    i,
                )
            else:
                unit = get_mat(
                    moment.original_form[i]["GateInSlot"]["DefinitionMatrix"]
                )
                qubits = [k for k in moment.filler_q]
                qubits.append(i)
                qc.unitary(unit, qubits, moment.original_form[i]["GateInSlot"]["Name"])
                if len(moment.filler_q) > 0:
                    print(
                        "This gate {} is not necessarily converted correctly. The order of the qubits maybe reversed Please check! ".format(
                            moment.original_form[i]["GateInSlot"]["Name"]
                        )
                    )

    if len(moment.control_q) != 0:
        moment_mat = get_mat(moment.original_form[0]["GateInSlot"]["DefinitionMatrix"])
        for i in range(moment.nr_q):
            # as putea sa scot sii identitatiile daca vrei
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
        # Pot incerca si o solutie in care sa descompun efectiv poarta ca aici :https://arxiv.org/pdf/quant-ph/9503016.pdf


def add_gates(res, qc, barrier=True):
    mo = 0
    for i in transpose_list(res["PuzzleGates"]):
        mo = mo + 1
        nr_gates_moment = len(i)
        momnet_i = Moment(i)
        if barrier:
            qc.barrier()
        add_moment(momnet_i, qc)


def read_circuit(path):
    file = open(path, "r")
    content = file.read()
    res = json.loads(content)
    return res


def puzzle_to_circuit(puzzle, initial_state=False):

    nr_q = get_nr_q(puzzle)
    if initial_state != False:
        qc = QuantumCircuit(nr_q)
        qc.initialize(initial_state)
        add_gates(puzzle, qc, barrier=True)
    else:
        qc = QuantumCircuit(nr_q)
        add_gates(puzzle, qc, barrier=True)
    return qc

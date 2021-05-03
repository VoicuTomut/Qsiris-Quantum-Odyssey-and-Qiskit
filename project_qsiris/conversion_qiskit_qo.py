import json

from .conversion_gates import *


class IntermediateGate:
    def __init__(self, gate):
        """Create a new IntermediateGate"""
        """
        :param gate: Qiskit gate
        """
        self.name = gate[0].name
        self.matrice = gate[0].to_matrix()
        self.nrq = len(gate[1])
        self.qubits = [j.index for j in gate[1]]

    def print_description(self):
        print("name:", self.name)
        print("matrice:\n", self.matrice)
        print("qubits:", self.qubits)


def fill_slot(
        gate,
        visib=False,
        h_aux=False,
        ag_slo=None,
):
    """
    :param gate: (gate) dictionary
    :param visib: (True/False)
    :param h_aux: (True/False)

    :return: dictionary with the following structure:
    ex:
    {'IsGateVisible': True,
    'HasAuxGate': False,
    'GateInSlot': gate
    'AuxGateInSlot': None}
    """

    slot = {}
    slot["IsGateVisible"] = visib
    slot["HasAuxGate"] = h_aux
    slot["GateInSlot"] = gate
    slot["AuxGateInSlot"] = ag_slo
    return slot


def get_odyssey_circuit(qiskit_circuit):
    """
    :param qiskit_circuit: qiskit circuit
    :return: odyssey circuit as a dictionary
    """
    nr_q = len(qiskit_circuit.qubits)
    gate_depth = 7
    depth = [0 for i in range(nr_q)]

    qo_circuit = [[fill_slot(I) for i in range(nr_q)] for j in range(gate_depth)]

    for qiskit_gate in qiskit_circuit.data:
        p = IntermediateGate(qiskit_gate)

        if p.name == "cx":
            if len(p.qubits) > 1:
                moments = [depth[k] for k in range(nr_q)]

                moment = max(moments)
                for j in range(nr_q):
                    depth[j] = moment

                q_0 = p.qubits[0]
                qo_circuit[depth[q_0]][q_0] = fill_slot(CT, visib=True)

                q_1 = p.qubits[1]
                qo_circuit[depth[q_1]][q_1] = fill_slot(X, visib=True)

                for j in range(nr_q):
                    depth[j] = depth[j] + 1

        else:

            if len(p.qubits) > 1:
                moments = [depth[k] for k in p.qubits]

                moment = max(moments)
                for j in p.qubits:
                    depth[j] = moment

            for j in range(len(p.qubits) - 1):
                q = p.qubits[j]
                # Circuit[depth[q]][q]=p.name+'-F'
                qo_circuit[depth[q]][q] = fill_slot(F, visib=True)  # ADD Filler
                depth[q] = depth[q] + 1

            q = p.qubits[len(p.qubits) - 1]

            # Create gate:
            if p.name in Gates_list.keys():
                gate = Gates_list[p.name]
            else:
                gate = _get_gate(name=p.name, matrix=p.matrice)
            qo_circuit[depth[q]][q] = fill_slot(gate, visib=True)  # ADD Gate
            depth[q] = depth[q] + 1

    return qo_circuit


def generate_ball(nr_q):
    """
     :param nr_q: (number of qubits) int
     :return: vector of dictionaries that represent ball states:
     ex:
    [{'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
     {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
     {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
     {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}],
    """
    ball = [[c0 for k in range(2 ** nr_q)] for ko in range(2 ** nr_q)]
    ball[0][0] = c1
    return ball


def circuit_to_puzzle(qiskit_circuit, gate_cap=7, puzzle_type="General"):
    """
    :param qiskit_circuit: qiskit circuit
    :param gate_cap: (depth of the circuit in odyssey)int
    :param puzzle_type:(puzzle type)str
    :return: (puzzle)dictionary
    """
    puzzle = {}
    puzzle["PuzzleDefinition"] = ""
    puzzle["PuzzleGates"] = ""
    puzzle["AvailableGates"] = ""
    puzzle["Tooltips"] = []

    initial_state = [[0] for i in range(2 ** len(qiskit_circuit.qubits))]
    initial_state[0][0] = 1

    puzzle["PuzzleDefinition"] = {}
    puzzle["PuzzleDefinition"]["ModuleID"] = "Qiskit"
    puzzle["PuzzleDefinition"]["ID"] = 57
    puzzle["PuzzleDefinition"]["QubitCapacity"] = len(qiskit_circuit.qubits)
    puzzle["PuzzleDefinition"]["GateCapacity"] = gate_cap
    puzzle["PuzzleDefinition"]["Name"] = qiskit_circuit.name
    puzzle["PuzzleDefinition"]["InitialState"] = _matrix_to_odyssey(initial_state)  #
    puzzle["PuzzleDefinition"]["FinalState"] = _matrix_to_odyssey(initial_state)  #
    puzzle["PuzzleDefinition"]["FinalBallState"] = generate_ball(
        len(qiskit_circuit.qubits))  #
    puzzle["PuzzleDefinition"]["Difficulty"] = "Beginner"
    puzzle["PuzzleDefinition"]["PuzzleType"] = puzzle_type
    puzzle["PuzzleDefinition"]["Description"] = "SavePuzzlePanel(Clone)"

    puzzle["PuzzleGates"] = _transpose_list(get_odyssey_circuit(qiskit_circuit))

    puzzle["AvailableGates"] = [H, Z, Y, X, CT]

    return puzzle


def change_init_state(puzzle, vec):
    """
    :param puzzle: (puzzle)
    :param vec: ([])np.array
    change initial state of puzzle
    """
    puzzle["PuzzleDefinition"]["InitialState"] = _vector_to_odyssey(vec)


def change_final_state(puzzle, vec):
    """
    :param puzzle: (puzzle)
    :param vec: ([])np.array
    change final state of puzzle
    """
    puzzle["PuzzleDefinition"]["FinalState"] = _vector_to_odyssey(vec)


def add_gate(puzzle, gate):
    """
    Add gate to a puzzle as "AvailableGates"
    """
    puzzle["AvailableGates"].append(gate)


def save_puzzle(puzzle, name):
    """
    :param puzzle: (puzzle)dictionary
    :param name: (name)str
    Save puzzle in qpf format for Odissey
    """

    fname = "circuits/qiskit_to_odyssey/" + name + ".qpf"
    with open(fname, "w") as f:
        json.dump(puzzle, f, indent=4)
    print(
        puzzle["PuzzleDefinition"]["Name"]
        + " saved:"
        + fname
    )

import numpy as np
import cmath
import json


class intermediate_gate:
    def __init__(self, poarta):
        self.name = poarta[0].name
        self.matrice = poarta[0].to_matrix()
        self.nrq = len(poarta[1])
        self.qubits = [j.index for j in poarta[1]]

    def print_description(self):
        print("name:", self.name)
        print("matrice:\n", self.matrice)
        print("qubits:", self.qubits)


def complex_to_QO(com):
    return {
        "Real": com.real,
        "Imaginary": com.imag,
        "Magnitude": abs(com),
        "Phase": cmath.phase(com),
    }


def vec_to_QO(vec):
    v = []
    for i in vec:
        v.append(complex_to_QO(i))
    return v


def mat_to_QO(mat):
    m = []
    for i in mat:
        m.append(vec_to_QO(i))
    return m


def transpose_list(A):
    c = len(A[0])
    l = len(A)

    B = [["" for i in range(l)] for j in range(c)]

    b_c = 0

    for j in range(c):
        for i in range(l):
            B[j][i] = A[i][j]

    return B


def get_gate(name, matrix, i_d=9, t=8, icon_path="Artwork/GatesIcons/CustomGate"):
    gate = {}
    gate["ID"] = i_d
    gate["Name"] = name
    gate["Type"] = t
    gate["IconPath"] = icon_path
    gate["CompatibleQubits"] = int(np.log2(len(matrix)))
    gate["DefinitionMatrix"] = mat_to_QO(matrix)  # p.matrice
    return gate


I = get_gate(
    name="I",
    matrix=[[1.0, 0.0], [0.0, 1.0]],
    i_d=5,
    t=0,
    icon_path="Artwork/GatesIcons/IGate",
)
X = get_gate(
    name="X",
    matrix=[[0.0, 1.0], [1.0, 0.0]],
    i_d=3,
    t=3,
    icon_path="Artwork/GatesIcons/XGate",
)
Y = get_gate(
    name="Y",
    matrix=[[0.0, 0.0 - 1j], [0.0 + 1j, 0.0]],
    i_d=2,
    t=5,
    icon_path="Artwork/GatesIcons/YGate",
)
Z = get_gate(
    name="Z",
    matrix=[[1.0, 0.0], [0.0, -1.0]],
    i_d=1,
    t=1,
    icon_path="Artwork/GatesIcons/ZGate",
)
F = get_gate(
    name="Filler",
    matrix=[[1.0, 0.0], [0.0, 1.0]],
    i_d=1010,
    t=7,
    icon_path="Artwork/GatesIcons/FillerGate",
)
CT = get_gate(
    name="CTRL",
    matrix=[[0.0, 0.0], [0.0, 1.0]],
    i_d=5,
    t=6,
    icon_path="Artwork/GatesIcons/CTRLGate",
)
H = get_gate(
    name="H",
    matrix=[[1 / np.sqrt(2), 1 / np.sqrt(2)], [1 / np.sqrt(2), -1 / np.sqrt(2)]],
    i_d=0,
    t=2,
    icon_path="Artwork/GatesIcons/HGate",
)
G_list = {"h": H, "x": X, "z": Z}


def fill_slot(
    gate,
    vizib=False,
    h_aux=False,
    ag_slo=None,
):
    slot = {}
    slot["IsGateVisible"] = vizib
    slot["HasAuxGate"] = h_aux
    slot["GateInSlot"] = gate
    slot["AuxGateInSlot"] = ag_slo
    return slot


def get_QO_Circuit(circuit):
    nr_q = len(circuit.qubits)
    gate_depth = 7
    depth = [0 for i in range(nr_q)]

    Circuit = [[fill_slot(I) for i in range(nr_q)] for j in range(gate_depth)]

    for i in circuit.data:
        p = intermediate_gate(i)

        if p.name == "cx":
            if len(p.qubits) > 1:
                moments = [depth[k] for k in range(nr_q)]

                moment = max(moments)
                for j in range(nr_q):
                    depth[j] = moment

                Circuit[depth[p.qubits[0]]][p.qubits[0]] = fill_slot(CT, vizib=True)
                Circuit[depth[p.qubits[1]]][p.qubits[1]] = fill_slot(X, vizib=True)

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
                Circuit[depth[q]][q] = fill_slot(F, vizib=True)  # ADD Filler
                depth[q] = depth[q] + 1

            q = p.qubits[len(p.qubits) - 1]

            # Create gate:
            if p.name in G_list.keys():
                gate = G_list[p.name]
            else:
                gate = get_gate(name=p.name, matrix=p.matrice)
            Circuit[depth[q]][q] = fill_slot(gate, vizib=True)  # ADD Gate
            depth[q] = depth[q] + 1

    return Circuit


c0 = {"Real": 0.0, "Imaginary": 0.0, "Magnitude": 0.0, "Phase": 0.0}
c1 = {"Real": 1.0, "Imaginary": 0.0, "Magnitude": 0.0, "Phase": 0.0}


def generate_ball(nr_q):
    ball = [[c0 for k in range(2 ** nr_q)] for ko in range(2 ** nr_q)]
    ball[0][0] = c1
    return ball


def circuit_to_puzzle(circuit,gate_cap=7,puzzle_type="General"):
    puzzle = {}
    puzzle["PuzzleDefinition"] = ""
    puzzle["PuzzleGates"] = ""
    puzzle["AvailableGates"] = ""
    puzzle["Tooltips"] = []

    initial_state = [[0] for i in range(2 ** len(circuit.qubits))]
    initial_state[0][0] = 1

    puzzle["PuzzleDefinition"] = {}
    puzzle["PuzzleDefinition"]["ModuleID"] = "Qiskit"
    puzzle["PuzzleDefinition"]["ID"] = 57
    puzzle["PuzzleDefinition"]["QubitCapacity"] = len(circuit.qubits)
    puzzle["PuzzleDefinition"]["GateCapacity"] = gate_cap
    puzzle["PuzzleDefinition"]["Name"] = circuit.name
    puzzle["PuzzleDefinition"]["InitialState"] = mat_to_QO(initial_state)  #
    puzzle["PuzzleDefinition"]["FinalState"] = mat_to_QO(initial_state)  #
    puzzle["PuzzleDefinition"]["FinalBallState"] = generate_ball(len(circuit.qubits))  #
    puzzle["PuzzleDefinition"]["Difficulty"] = "Beginner"
    puzzle["PuzzleDefinition"]["PuzzleType"] =puzzle_type
    puzzle["PuzzleDefinition"]["Description"] = "SavePuzzlePanel(Clone)"

    puzzle["PuzzleGates"] = transpose_list(get_QO_Circuit(circuit))

    puzzle["AvailableGates"] = [H, Z, Y, X, CT]

    return puzzle


def change_init_state(puzzle, vec):
    puzzle["PuzzleDefinition"]["InitialState"] = vec_to_QO(vec)


def change_final_state(puzzle, vec):
    puzzle["PuzzleDefinition"]["FinalState"] = vec_to_QO(vec)


def add_gate(puzzle, gate):
    puzzle["AvailableGates"].append(gate)


def seve_puzzle(puzzle, name):
    with open("Circuits/QK_QO/" + name + ".qpf", "w") as f:
        json.dump(puzzle, f, indent=4)
    print(
        puzzle["PuzzleDefinition"]["Name"]
        + " saved:"
        + "Circuits/QK_QO/"
        + name
        + ".qpf"
    )

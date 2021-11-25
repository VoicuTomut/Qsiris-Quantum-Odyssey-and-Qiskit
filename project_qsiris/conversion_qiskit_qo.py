import json

import project_qsiris.conversion_gates as conv
from project_qsiris.conversion_intermediates import IntermediateGate


def _fill_slot(
        gate,
        slot_position,
        visib=False,

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
    slot["GateDefinition"] = gate
    # slot["CircuitPosition"] = { "Item1": slot_position[0],"Item2": slot_position[1] }
    slot["SlaveGatesIDs"] = None
    slot["MasterGateID"] = -1
    slot["OrderInPlacement"] = 0
    # slot["ID"] = slot_position[0]+slot_position[1]*slot_position[0]

    return slot


def _get_odyssey_circuit(qiskit_circuit):
    """
    :param qiskit_circuit: qiskit circuit
    :return: odyssey circuit as a dictionary
    """
    nr_q = len(qiskit_circuit.qubits)
    gate_depth = 7

    depth = [0 for _ in range(nr_q)]
    qo_circuit = [[_fill_slot(conv.I, slot_position=(q, g)) for q in range(nr_q)] for g in range(gate_depth)]

    for qiskit_gate in qiskit_circuit.data:
        interm_gate = IntermediateGate(qiskit_gate)

        if interm_gate.name == "cx":
            if len(interm_gate.qubits) > 1:
                moments = [depth[k] for k in range(nr_q)]

                moment = max(moments)
                for j in range(nr_q):
                    depth[j] = moment

                q_0 = interm_gate.qubits[0]
                qo_circuit[depth[q_0]][q_0] = _fill_slot(conv.CT, visib=True, slot_position=(depth[q_0], q_0))

                q_1 = interm_gate.qubits[1]
                qo_circuit[depth[q_1]][q_1] = _fill_slot(conv.X, visib=True, slot_position=(depth[q_0], q_0))

                for j in range(nr_q):
                    depth[j] = depth[j] + 1

        else:

            if len(interm_gate.qubits) > 1:
                moments = [depth[k] for k in interm_gate.qubits]

                moment = max(moments)
                for j in interm_gate.qubits:
                    depth[j] = moment

            for j in range(len(interm_gate.qubits) - 1):
                q = interm_gate.qubits[j]
                # Circuit[depth[q]][q]=p.name+'-F'
                qo_circuit[depth[q]][q] = _fill_slot(conv.F, visib=True, slot_position=(depth[q], q))  # ADD Filler
                depth[q] = depth[q] + 1

            q = interm_gate.qubits[len(interm_gate.qubits) - 1]

            # Create gate:
            if interm_gate.name in conv.Gates_list.keys():
                gate = conv.Gates_list[interm_gate.name]
            else:
                gate = conv._get_odyssey_gate(name=interm_gate.name, matrix=interm_gate.matrice)
            qo_circuit[depth[q]][q] = _fill_slot(gate, visib=True, slot_position=(depth[q], q))  # ADD Gate
            depth[q] = depth[q] + 1

    return qo_circuit


def _generate_ball(nr_q):
    """
     :param nr_q: (number of qubits) int
     :return: vector of dictionaries that represent ball states:
     ex:
    [{'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
     {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
     {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
     {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}],
    """
    ball = [[conv.c0 for k in range(2 ** nr_q)] for ko in range(2 ** nr_q)]
    ball[0][0] = conv.c1
    return ball


def qiskit_to_odyssey(qiskit_circuit, gate_cap=7, puzzle_type="General", SolutionMinimumGates=1):
    """
    :param qiskit_circuit: qiskit circuit
    :param gate_cap: (depth of the circuit in odyssey)int
    :param puzzle_type:(puzzle type)str
    :return: (puzzle)dictionary
    """
    puzzle = {}
    puzzle["PuzzleDefinition"] = ""
    puzzle["PuzzleGateSlots"] = ""
    puzzle["AvailableGates"] = ""
    puzzle["Tooltips"] = []

    initial_state = [[0] for t in range(2 ** len(qiskit_circuit.qubits))]
    initial_state[0][0] = 1

    puzzle["PuzzleDefinition"] = {}

    puzzle["PuzzleDefinition"]["ID"] = 57
    puzzle["PuzzleDefinition"]["QubitCapacity"] = len(qiskit_circuit.qubits)
    puzzle["PuzzleDefinition"]["GateCapacity"] = gate_cap
    puzzle["PuzzleDefinition"]["SolutionMinimumGates"] = SolutionMinimumGates
    puzzle["PuzzleDefinition"]["Name"] = qiskit_circuit.name
    puzzle["PuzzleDefinition"]["InitialState"] = conv._matrix_to_odyssey(initial_state)  #
    puzzle["PuzzleDefinition"]["FinalState"] = conv._matrix_to_odyssey(initial_state)  #
    puzzle["PuzzleDefinition"]["FinalBallState"] = _generate_ball(len(qiskit_circuit.qubits))  #

    ps = []
    for line in conv._transpose_list(_get_odyssey_circuit(qiskit_circuit)):
        for slot in line:
            ps.append(slot)
    puzzle["PuzzleGateSlots"] = ps  # conv._transpose_list(_get_odyssey_circuit(qiskit_circuit))

    puzzle["AvailableGates"] = [conv.H, conv.Z, conv.Y, conv.X, conv.CT]

    return puzzle


def odyssey_change_init_state(puzzle, vec):
    """
    :param puzzle: (puzzle)
    :param vec: ([])np.array
    change initial state of puzzle
    """
    puzzle["PuzzleDefinition"]["InitialState"] = conv._vector_to_odyssey(vec)


def odyssey_change_final_state(puzzle, vec):
    """
    :param puzzle: (puzzle)
    :param vec: ([])np.array
    change final state of puzzle
    """
    puzzle["PuzzleDefinition"]["FinalState"] = conv._vector_to_odyssey(vec)


def odyssey_add_gate(puzzle, gate):
    """
    Add gate to a puzzle as "AvailableGates"
    """
    puzzle["AvailableGates"].append(gate)


def save_odyssey_puzzle(puzzle, name):
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

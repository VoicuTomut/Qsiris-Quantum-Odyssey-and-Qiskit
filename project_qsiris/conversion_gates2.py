
from project_qsiris.conversion_gates import _matrix_to_odyssey,_vector_to_odyssey
from project_qsiris.conversion_gates import c0, c1
from project_qsiris.conversion_intermediates import IntermediateGate
from qiskit_qo_class import GateDefinition, Slot



def _get_odyssey_circuit(qiskit_circuit):
    """
    :param qiskit_circuit: qiskit circuit
    :return: odyssey circuit as a dictionary
    """
    nr_q = len(qiskit_circuit.qubits)
    gate_depth = 7

    depth = [0 for _ in range(nr_q)]
    qo_circuit = [[Slot(I,slot_position=(q,g)) for q in range(nr_q)] for g in range(gate_depth)]

    for qiskit_gate in qiskit_circuit.data:
        interm_gate = IntermediateGate(qiskit_gate)

        if interm_gate.name == "cx":
            if len(interm_gate.qubits) > 1:
                moments = [depth[k] for k in range(nr_q)]

                moment = max(moments)
                for j in range(nr_q):
                    depth[j] = moment

                q_0 = interm_gate.qubits[0]
                qo_circuit[depth[q_0]][q_0] = Slot(CT, visib=True, slot_position=(depth[q_0],q_0))

                q_1 = interm_gate.qubits[1]
                qo_circuit[depth[q_1]][q_1] = Slot(X, visib=True, slot_position=(depth[q_0],q_0))

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
                qo_circuit[depth[q]][q] = _fill_slot(conv.F, visib=True, slot_position=(depth[q],q))  # ADD Filler
                depth[q] = depth[q] + 1

            q = interm_gate.qubits[len(interm_gate.qubits) - 1]

            # Create gate:
            if interm_gate.name in conv.Gates_list.keys():
                gate = conv.Gates_list[interm_gate.name]
            else:
                gate = conv._get_odyssey_gate(name=interm_gate.name, matrix=interm_gate.matrice)
            qo_circuit[depth[q]][q] = _fill_slot(gate, visib=True, slot_position=(depth[q],q))  # ADD Gate
            depth[q] = depth[q] + 1

    return qo_circuit









I = GateDefinition(
    name="I",
    matrix=[[1.0, 0.0], [0.0, 1.0]],
    i_d=5,
    t=0,
    icon_path="Artwork/GatesIcons/IGate",
)

X = GateDefinition(
    name="X",
    matrix=[[0.0, 1.0], [1.0, 0.0]],
    i_d=3,
    t=3,
    icon_path="Artwork/GatesIcons/XGate",
)

Y = GateDefinition(
    name="Y",
    matrix=[[0.0, 0.0 - 1j], [0.0 + 1j, 0.0]],
    i_d=2,
    t=5,
    icon_path="Artwork/GatesIcons/YGate",
)

Z = GateDefinition(
    name="Z",
    matrix=[[1.0, 0.0], [0.0, -1.0]],
    i_d=1,
    t=1,
    icon_path="Artwork/GatesIcons/ZGate",
)

F = GateDefinition(
    name="Filler",
    matrix=[[1.0, 0.0], [0.0, 1.0]],
    i_d=1010,
    t=7,
    icon_path="Artwork/GatesIcons/FillerGate",
)

CT = GateDefinition(
    name="CTRL",
    matrix=[[0.0, 0.0], [0.0, 1.0]],
    i_d=5,
    t=6,
    icon_path="Artwork/GatesIcons/CTRLGate",
)

H = GateDefinition(
    name="H",
    matrix=[[1 / np.sqrt(2), 1 / np.sqrt(2)],
            [1 / np.sqrt(2), -1 / np.sqrt(2)]],
    i_d=0,
    t=2,
    icon_path="Artwork/GatesIcons/HGate",
)

Gates_list = {"h": H, "x": X, "z": Z}
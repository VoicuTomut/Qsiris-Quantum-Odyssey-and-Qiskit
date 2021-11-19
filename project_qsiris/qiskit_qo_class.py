import json

import project_qsiris.conversion_gates2 as conv2


class Puzzle:
    def __init__(self, qiskit_circuit, gate_cap):
        """
        
        """

        self.PuzzleDefinition = PuzzleDefinition(qiskit_circuit, gate_cap)  #
        self.Tooltips = []  #
        self.AvailableGates = [conv2.H, conv2.Z, conv2.Y, conv2.X, conv2.CT]  #
        self.PuzzleGateSlots = populagte_PuzzleGateSlots(self, qiskit_circuit, gate_cap)

    def populagte_PuzzleGateSlots(self, qiskit_circuit, gate_cap):
        pass


class PuzzleDefinition:
    def __init__(self, qiskit_circuit, gate_cap):
        self.ID = 57
        self.QubitCapacity = len(qiskit_circuit.qubits)
        self.GateCapacity = gate_cap
        self.SolutionMinimumGates = 1
        self.Name = qiskit_circuit.name
        self.InitialState = conv2._matrix_to_odyssey(self._default_initial_state())
        self.FinalState = conv2._matrix_to_odyssey(self._default_initial_state())
        self.FinalBallState = self._generate_ball()

    def _default_initial_state(self):
        initial_state = [[0] for t in range(2 ** self.QubitCapacity)]
        initial_state[0][0] = 1
        return initial_state

    def _generate_ball(self):
        """
         :param self fot self.QubitCapacity: (number of qubits) int
         :return: vector of dictionaries that represent ball states:
         ex:
        [{'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
         {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
         {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
         {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}],
        """
        nr_q = self.QubitCapacity
        ball = [[conv2.c0 for k in range(2 ** nr_q)] for ko in range(2 ** nr_q)]
        ball[0][0] = conv2.c1
        return ball

    def odyssey_change_init_state(self, vec):
        """
        :param puzzle: (puzzle)
        :param vec: ([])np.array
        change initial state of puzzle
        """
        self.InitialState = conv2._vector_to_odyssey(vec)

    def odyssey_change_final_state(self, vec):
        """
        :param puzzle: (puzzle)
        :param vec: ([])np.array
        change final state of puzzle
        """
        self.InitialState.FinalState = conv2._vector_to_odyssey(vec)


class GateDefinition:

    def __inint__(self, name, matrix, i_d=9, t=8, icon_path="Artwork/GatesIcons/CustomGate"):
        """"
        
        """
        self.ID = i_d
        self.Name = name
        self.Type = t
        self.IconPath = icon_path
        self.CompatibleQubits = int(np.log2(len(matrix)))
        self.DefinitionMatrix = conv2._matrix_to_odyssey(matrix)


class Slot:
    def __init__(self, gate, visib=False, slot_position={'Item1': -1, 'Item2': -1}):
        """
        
        """
        self.IsGateVisible = visib
        self.GateDefinition = gate
        self.CircuitPosition = slot_position
        self.SlaveGatesIDs = None
        self.MasterGateID = -1
        self.OrderInPlacement = 0

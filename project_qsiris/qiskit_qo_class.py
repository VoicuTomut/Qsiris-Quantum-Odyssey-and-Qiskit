import json

import project_qsiris.conversion_gates2 as conv2


class Puzzle:
    def __init__(self, qiskit_circuit, gate_cap):
        """
        
        """

        self.PuzzleDefinition = PuzzleDefinition(qiskit_circuit, gate_cap)  #
        self.Tooltips = []  #
        self.AvailableGates = [conv2.H, conv2.Z, conv2.Y, conv2.X, conv2.CT]  #
        self.PuzzleGateSlots = self.populagte_PuzzleGateSlots( qiskit_circuit, gate_cap)

    def populagte_PuzzleGateSlots(self, qiskit_circuit, gate_cap):

        circ=conv2._get_odyssey_circuit(qiskit_circuit)

        pgs=[ ]
        for i in range(len(circ)):
            gate_line=circ[i]
            for j in range(len(gate_line)):
                slot=gate_line[j]
                # slot correction:
                slot.CircuitPosition=(i,  j)
                pgs.append(slot)

        return pgs


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

    def print_info(self):

        print("Id:",self.ID)
        print("QubitCapacity:", self.QubitCapacity)
        print("GateCapacity:", self.GateCapacity)
        print("SolutionMinimumGates:", self.SolutionMinimumGates)
        print("InitialState:", self.InitialState)
        print("FinalState:", self.FinalState)
        print("FinalBallState:", self.FinalBallState)



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




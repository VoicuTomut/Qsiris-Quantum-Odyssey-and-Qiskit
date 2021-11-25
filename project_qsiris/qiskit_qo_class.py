from typing import Any

import json

import project_qsiris.conversion_gates2 as conv2


class Challenge:

    def __init__(self, qiskit_circuit, gate_cap):
        self.ID = "UNASSIGNED_ID"
        self.Difficulty = "Beginner"
        self.Puzzles = [Puzzle(qiskit_circuit, gate_cap)]
        self.name = "Qiskit_QO"
        self.AuthorName = "QuarksInteractive"
        self.AuthorUserID = "3bab5751-5826-4503-8603-3e91d0619eb7"
        self.NumberOfPuzzles = 1
        self.IsTimed = False
        self.TimeAvailable = 0
        self.IsPublic = False
        self.Description = "Descriere"

    def get_challenge(self):
        challenge = {"ID": self.ID,
                     "Difficulty": self.Difficulty,
                     "Puzzles": [self.Puzzles[0].get_puzzle()],
                     "Name": self.name,
                     "AuthorName": self.AuthorName,
                     "AuthorUserID": self.AuthorUserID,
                     "NumberOfPuzzles": self.NumberOfPuzzles,
                     "IsTimed": self.IsTimed,
                     "TimeAvailable": self.TimeAvailable,
                     "IsPublic": self.IsPublic,
                     "Description": self.Description}
        return challenge

    def to_json(self):
        challenge = self.get_challenge()
        return json.dumps(challenge, sort_keys=False, indent=4)


class Puzzle:
    def __init__(self, qiskit_circuit, gate_cap):
        """
        
        """

        self.PuzzleDefinition = PuzzleDefinition(qiskit_circuit, gate_cap)  #
        self.Tooltips = []  #
        self.AvailableGates = [conv2.H, conv2.Z, conv2.Y, conv2.X, conv2.CT]  #
        self.PuzzleGateSlots = self.populagte_PuzzleGateSlots(qiskit_circuit, gate_cap)

    def populagte_PuzzleGateSlots(self, qiskit_circuit, gate_cap):

        circ = conv2._get_odyssey_circuit(qiskit_circuit)

        pgs = []
        for i in range(len(circ)):
            gate_line = circ[i]
            for j in range(len(gate_line)):
                slot = gate_line[j]
                # slot correction:
                slot.CircuitPosition = {"Item1": j, "Item2": i}
             
                pgs.append(slot)
        for i in range(len(pgs)):
            pgs[i].ID=i

        return pgs

    def get_puzzle(self):
        puzzle = {"PuzzleDefinition": self.PuzzleDefinition.get_puzzle_deff(),
                  "PuzzleGateSlots": [slot.get_slot() for slot in self.PuzzleGateSlots],
                  "AvailableGates": [gate.get_def() for gate in self.AvailableGates],
                  "Tooltips": self.Tooltips, }
        return puzzle

    def to_json(self):
        puzzle = self.get_puzzle()
        return json.dumps(puzzle, sort_keys=False, indent=4)


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
        print("Id:", self.ID)
        print("QubitCapacity:", self.QubitCapacity)
        print("GateCapacity:", self.GateCapacity)
        print("SolutionMinimumGates:", self.SolutionMinimumGates)
        print("InitialState:", self.InitialState)
        print("FinalState:", self.FinalState)
        print("FinalBallState:", self.FinalBallState)

    def get_puzzle_deff(self):
        puzzledef = {
            "ID": self.ID,
            "QubitCapacity": self.QubitCapacity,
            "GateCapacity": self.GateCapacity,
            "SolutionMinimumGates": self.SolutionMinimumGates,
            "Name": self.Name,
            "InitialState": self.InitialState,
            "FinalState": self.FinalState,
            "FinalBallState": self.FinalBallState, }
        return puzzledef

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

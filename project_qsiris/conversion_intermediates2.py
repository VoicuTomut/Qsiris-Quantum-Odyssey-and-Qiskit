class IntermediateGate:
    """
        Helper for Qiskit -> Odyssey
    """
    def __init__(self, gate):
        """
            Create a new IntermediateGate
            :param gate: Qiskit gate
        """
        self.name = gate[0].name 
        self.matrice = gate[0].to_matrix()
        self.nrq = len(gate[1])
        self.qubits = [j.index for j in gate[1]]

    def __str__(self):
        print("name:", self.name)
        print("matrice:\n", self.matrice)
        print("qubits:", self.qubits)


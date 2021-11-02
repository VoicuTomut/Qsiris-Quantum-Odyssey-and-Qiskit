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


class OdysseyMoment:
    """
        Helper for Odyssey -> Qiskit
    """
    def __init__(self, original_form):
        self.original_form = original_form
        self.nr_q = len(self.original_form)
        self.control_q = self.get_control_q()
        self.filler_q = self.get_filler_q()

    def _filter_qubits(self, param_gate_name):
        cq = []
        for j in range(self.nr_q):
            print(self.original_form[j])
            gate_name = self.original_form[j]["GateDefinition"]["Name"]
            if gate_name == param_gate_name:
                cq.append(j)
        return cq

    def get_control_q(self):
        return self._filter_qubits("CTRL")

    def get_filler_q(self):
        return self._filter_qubits("Filler")
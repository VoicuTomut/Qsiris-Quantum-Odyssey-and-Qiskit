import json
import numpy as np

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister

import project_qsiris.conversion_gates as conv
from project_qsiris.conversion_intermediates import OdysseyMoment

def get_odyssey_nr_qubits(res):
    """
    :param res: (puzzle)dictionary
    :return: (number of qubits from puzzle)int
    """
    nr_q = res["PuzzleDefinition"]["QubitCapacity"]
    return nr_q


def extract_odyssey_matrix(mat):
    """
    :param mat: matrix  of complex numbers in dictionary form
    :return: matrix ov 'complex' numbers

    #example:
    mat=[[{'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0},
          {'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}],
         [{'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0},
          {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}]]

    g_mat = extract_odyssey_matrix(mat)
    print("matrice:\n",g_mat)
    """
    mat_conv = []
    for i in mat:
        linie = []
        for j in i:
            linie.append(conv._odyssey_to_complex(j))
        mat_conv.append(linie)

    return mat_conv


def add_odyssey_moment(puzzle_gate, qc,qiskit_circuit):
    """
    :param puzzle_gate: string of gates
    :param qc: QuantumCircuit Qiskit
    Add gates from moment to the  Qiskit circuit
    """

    moment = OdysseyMoment(puzzle_gate)

    if len(moment.control_q) == 0:
        """
            This is the default case
        """
        for qubit in range(moment.nr_q):
            gate_name = moment.original_form[qubit]["GateInSlot"]["Name"]
            if gate_name == "X":
                qc.x(qubit)
                ########################################################
                qiskit_circuit=qiskit_circuit+'qc.x({}) \n'.format(str(qubit))
                ########################################################
            elif gate_name == "Y":
                qc.y(qubit)
                ########################################################
                qiskit_circuit=qiskit_circuit+'qc.y({}) \n'.format(str(qubit))
                ########################################################              
            elif gate_name == "Z":
                qc.z(qubit)
                ########################################################
                qiskit_circuit=qiskit_circuit+'qc.z({}) \n'.format(str(qubit))
                ########################################################
            elif gate_name == "H":
                qc.h(qubit)
                ########################################################
                qiskit_circuit=qiskit_circuit+'qc.h({}) \n'.format(str(qubit))
                ########################################################
            elif gate_name == "I":
                qc.id(qubit)
                ########################################################
                qiskit_circuit=qiskit_circuit+'qc.id({}) \n'.format(str(qubit))
                ########################################################               
            elif gate_name == "Filler":
                print(
                    "The fillers are empty gates so they will not be converted to qiskit",
                    qubit,
                )
            else:
                unit = extract_odyssey_matrix(
                    moment.original_form[qubit]["GateInSlot"]["DefinitionMatrix"]
                )
                qubits = [k for k in moment.filler_q]
                qubits.append(qubit)
                ########################################################
                qiskit_circuit=qiskit_circuit+'unit={} \n'.format(unit)
                qiskit_circuit=qiskit_circuit+'qubits={} \n'.format(qubits)
                ########################################################
                
                qc.unitary(unit, qubits, moment.original_form[qubit]["GateInSlot"]["Name"].lower())
                ########################################################
                qiskit_circuit=qiskit_circuit+'qc.unitary(unit, qubits, {})'.format(moment.original_form[qubit]["GateInSlot"]["Name"].lower())
                ########################################################
                if len(moment.filler_q) > 0:
                    print(
                        "This gate {} is not necessarily converted correctly."
                        " The order of the qubits maybe reversed Please check! ".format(
                            gate_name.lower()
                        )
                    )
        
        
        return qiskit_circuit
    """
        If there are controls on the puzzle gate
    """
    for i in range(moment.nr_q):
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
            mat = extract_odyssey_matrix(moment.original_form[i]["GateInSlot"]["DefinitionMatrix"])
            """
            unit[-1][-1]=mat[1][1]
            unit[-1][-2]=mat[1][0]
            unit[-2][-1]=mat[0][1]
            unit[-2][-2]=mat[0][0]
            """
            for k in range(1, len(mat) + 1):
                for j in range(1, len(mat) + 1):
                    unit[-k][-j] = mat[-k][-j]
            #print(unit)
            #print("control:",moment.control_q)
            #print("qubits:",qubits[::-1])
            mc_q='_'
            for l in moment.control_q:
                mc_q=mc_q+str(l)+'_'
            name="c"+ mc_q+ moment.original_form[i]["GateInSlot"]["Name"]+ "_"+ str(i)+ "_"
            #print(name)
            ########################################################
            qiskit_circuit=qiskit_circuit+'unit={} \n'.format(repr(unit))
            qiskit_circuit=qiskit_circuit+'qubits={} \n'.format(repr(qubits))
            qiskit_circuit=qiskit_circuit+'name="{}" \n'.format(name.lower())
            ########################################################
            qc.unitary(
                unit,
                qubits[::-1],
                name.lower(),
            )
            ########################################################
            qiskit_circuit=qiskit_circuit+'qc.unitary(unit,qubits[::-1],name) \n'.format(name.lower())
            ########################################################
    return qiskit_circuit


def load_oddysey_puzzle(path):
    file = open(path, "r")
    content = file.read()
    puzzle = json.loads(content)
    return puzzle


def odyssey_to_qiskit(puzzle, incl_initial_state = False,
                      use_barrier = False,
                      incl_all_measurements = False):
    """
    :param path: (puzzle) path to puzzle
    :param initial_state: (initial qubits state ) string of dictionaries
    :return: quantum circuit in qiskit equivalent with the circuit from puzzle
    """

    nr_q = get_odyssey_nr_qubits(puzzle)
    qc = QuantumCircuit(QuantumRegister(nr_q), ClassicalRegister(nr_q))
    
    ########################################################
    qiskit_circuit='import numpy as np \n'
    qiskit_circuit=qiskit_circuit+'from numpy import array\n'
    qiskit_circuit=qiskit_circuit+'from qiskit import QuantumCircuit,QuantumRegister,ClassicalRegister \n \n'
   
    # initializae circuit:
    qiskit_circuit=qiskit_circuit+'nr_q={} \n'.format(nr_q)
    qiskit_circuit=qiskit_circuit+'qc = QuantumCircuit(QuantumRegister({}), ClassicalRegister({})) \n \n'.format(nr_q,nr_q)
    ########################################################
    
    if incl_initial_state != False:
        qc.initialize(incl_initial_state)

    for puzzle_gate in conv._transpose_list(puzzle["PuzzleGates"]):
        if use_barrier:
            qc.barrier()
            ########################################################
            qiskit_circuit=qiskit_circuit+'qc.barrier() \n'
            ########################################################
        qiskit_circuit=add_odyssey_moment(puzzle_gate, qc,qiskit_circuit)

    if incl_all_measurements:
        for index in range(nr_q):
            qc.measure(qc.qregs[0][index], qc.cregs[0][nr_q - 1 - index])
            ########################################################
            qiskit_circuit=qiskit_circuit+'qc.measure(qc.qregs[0][{}], qc.cregs[0][{}]) \n'.format(index,str(nr_q - 1 - index))
            ########################################################
    #print(qiskit_circuit)

    return qc , qiskit_circuit

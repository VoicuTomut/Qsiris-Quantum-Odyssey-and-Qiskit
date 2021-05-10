import numpy as np 
from numpy import array
from qiskit import QuantumCircuit,QuantumRegister,ClassicalRegister 
 
nr_q=2 
qc = QuantumCircuit(QuantumRegister(2), ClassicalRegister(2)) 
 
qc.h(0) 
qc.id(1) 
unit=array([[1.+0.j, 0.+0.j, 0.+0.j, 0.+0.j],
       [0.+0.j, 1.+0.j, 0.+0.j, 0.+0.j],
       [0.+0.j, 0.+0.j, 0.+0.j, 1.+0.j],
       [0.+0.j, 0.+0.j, 1.+0.j, 0.+0.j]]) 
qubits=[0, 1] 
name="c_0_x_1_" 
qc.unitary(unit,qubits[::-1],name) 
qc.measure(qc.qregs[0][0], qc.cregs[0][1]) 
qc.measure(qc.qregs[0][1], qc.cregs[0][0]) 

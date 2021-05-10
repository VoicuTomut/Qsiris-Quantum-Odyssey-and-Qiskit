import numpy as np 
from numpy import array
from qiskit import QuantumCircuit,QuantumRegister,ClassicalRegister 
 
nr_q=3 
qc = QuantumCircuit(QuantumRegister(3), ClassicalRegister(3)) 
 
qc.h(0) 
qc.h(1) 
qc.h(2) 
unit=array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j]]) 
qubits=[0, 2] 
name="c_0_z_2_" 
qc.unitary(unit,qubits[::-1],name) 
unit=array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j, -1.+0.j]]) 
qubits=[1, 2] 
name="c_1_z_2_" 
qc.unitary(unit,qubits[::-1],name) 
qc.id(0) 
qc.id(1) 
qc.id(2) 
qc.h(0) 
qc.h(1) 
qc.h(2) 
qc.x(0) 
qc.x(1) 
qc.x(2) 
unit=array([[ 1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
         0.+0.j],
       [ 0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
         0.+0.j],
       [ 0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
         0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
         0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j,  0.+0.j,
         0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j,  0.+0.j,
         0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  1.+0.j,
         0.+0.j],
       [ 0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,  0.+0.j,
        -1.+0.j]]) 
qubits=[0, 1, 2] 
name="c_0_1_z_2_" 
qc.unitary(unit,qubits[::-1],name) 
qc.x(0) 
qc.x(1) 
qc.x(2) 
qc.h(0) 
qc.h(1) 
qc.h(2) 
qc.measure(qc.qregs[0][0], qc.cregs[0][2]) 
qc.measure(qc.qregs[0][1], qc.cregs[0][1]) 
qc.measure(qc.qregs[0][2], qc.cregs[0][0]) 

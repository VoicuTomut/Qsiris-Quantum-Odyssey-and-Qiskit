# Project Qsiris

QO gives the opportunity gamers worldwide to work on quantum algorithms 
as if they are a fun puzzle game, without needing to know actual 
quantum computing, coding ... or even linear algebra.  

Quantum Odyssey (QO) can be downloaded [here](https://www.quarksinteractive.com/) 


## Concept

Qsiris you to create using Python and [Qiskit](https://qiskit.org) a puzzle in 
Quarks Interactive’s Quantum Odyssey (QO) video game.

You can create two types of QO puzzle files using Qiskit: 

*Editor* puzzle file – these allows you to visualize your algorithm 
from code to Quantum Odyssey visuals. This is a useful thing to do,
 using the actual QO Editor you can continue to work on the algorithm 
 straight in QO, set winning conditions and save it as a General puzzle 
 file straight in QO. 

*General* puzzle file – these can be uploaded in Quantum Odyssey as an 
actual puzzle for gamers to solve. Simply set the desired final state vector 
and any gates requirements you have and let’s see if gamers that run QO can 
find ways to optimize your algorithm! 


## *Server* branch (work in progress)
 
In python-server branch is a server which can receive as requests 
circuits in QO format and return a result of the circuit run in Qiskit and 
a QASM decomposition. Qiskit circuits will be executed on different backends 
incl. real hardware. 


## Project Organization
-------------
    │
    ├── circuits                              < Colection of circuits       
    │   ├── qiskit_to_odyssey                 < Qsiris saves files here               
    │   └── odyssey_circuits                  < QO refence files
    │
    ├── project_qsiris                        <  The code
    │   ├── conversion_qiskit_qo.py                      
    │   └── conversion__qo_qiskit.py                                   
    │
    ├── example_odyssey_to_qiskit.ipynb       < QO to Qiskit examples 
    │
    ├── example_qiskit_to_odyssey.ipynb       < Qiskit to Qo examples
    │
    ├── README.md
    │
    └── requirements.txt


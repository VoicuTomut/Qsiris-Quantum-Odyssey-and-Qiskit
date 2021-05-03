# Project Qsiris

Allows you to create using Python and Qiskit a puzzle in 
Quarks Interactive’s Quantum Odyssey (QO) video game.

QO gives the opportunity gamers worldwide to work on quantum algorithms 
as if they are a fun puzzle game, without needing to know actual 
quantum computing, coding ... or even linear algebra.  

Quantum Odyssey (QO) can be downloaded [here](https://www.quarksinteractive.com/) 

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


# QO_zxo

QO_zxo is a tool that makes Quantum Oddysey circuits compatible with Qiskit and allows circuits from [Qiskit](https://qiskit.org) to be visualized and run as puzzles in [Quantum Oddisey](https://www.quarksinteractive.com).

## Idea 

Quantum Odyssey(QO) is a game that allows you to develop a quantum intuition. But a lot of my quantum experiments are made in Qiskit so it would be useful if I could visualize them in QO representation. 

It would also be great if the puzzles from QO would run on a real hardware from IBM . That is why I added a QO to Qiskit convertor.

In python-server branch I implemented a server which can receive as requests circuits in QO format and return a result of the circuit run in qiskit and a qasm decomposition. I hope that, in the future, it will be connected directly to QO (see  old work branch).


## Project Organization
------------

    │
    ├── circuits                              < Colection of circuits       
    │   ├── qiskit_to_odyssey                 < Examples generate by Qsiris               
    │   └── odyssey_circuits                  < QO save files
    │
    ├── project_qisiris                       <  The code
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



# QO_zxo

QO_zxo is a tool that makes Quantum Oddysey circuits compatible with Qiskit and allows circuits from [Qiskit](https://qiskit.org) to be visualized and run as puzzles in [Quantum Oddisey](https://www.quarksinteractive.com).

## Idea 

Quantum Odyssey(QO)is a game that allows you to develop a quantum intuition. But a lot of my quantum experiments are made in Qiskit so it would be useful if I could visualize them in QO representation. 

It would also be great if the puzzles from QO would run on a real hardware from IBM . That is why I added a QO to Qiskit convertor.

In python-server branch I implemented a server which can receive as requests circuits in QO format and return a result of the circuit run in qiskit and a qasm decomposition. I hope that, in the future, it will be connected directly to QO (see  old work branch).


## Project Organization
------------

    │
    ├── Circuits                                         < Colection of QO circuits       
    │   ├── QK_QO                                        
    │   └── QO_circuits                                   
    │
    ├── q_to_q                                           <    
    │   ├── conversion_qiskit_qo.py                      
    │   └── conversion__qo_qiskit.py                                   
    │
    ├── QO_Qiskit.ipynb                                  < QO to Qiskit examples 
    │
    ├── Qiskit_QO.ipynb                                  < Qiskit to Qo examples
    │
    ├── README.md
    │
    └── requirements.txt


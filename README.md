# Project Qsiris

Quantum Odyssey (QO) gives the opportunity gamers worldwide to work on quantum algorithms 
as if they are a fun puzzle game, without needing to know actual 
quantum computing, coding... or even linear algebra.  

Quantum Odyssey (QO) can be downloaded [here](https://www.quarksinteractive.com/) 


## Concept

With Qsiris you area able to create using Python and [Qiskit](https://qiskit.org) a puzzle in 
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


## *Server* branch 
 
With the server you can use Quantum Odyssey puzzles inside of other python Qiskit projects or execute QO puzzle files on an IBM machine without having QO installed. At the click of a button, the QO puzzle is converted to a qiskit circuit and simulated. If the user wants to run on real hardware he just needs to add his token and change the path in test_server.html from "http://0.0.0.0:5000/QO_QK_convertor" to "http://0.0.0.0:5000//QO_QK_real".

### Steps to use server: 
1. pip install -r requirements_server.txt
2.   cd .../Qsiris-Quantum-Odyssey-and-Qiskit
3. python qsiris_cloud.py
4. open page test_server.html from /Qsiris-Quantum-Odyssey-and-Qiskit/templates/test_server.html
5. Quanutm Odyssey puzzle files by default are saved here: C:\Games\Quantum Odyssey 09\Quantum Odyssey 0.9\default\game\Quantum Odyssey_Data\Data\PuzzleContainer\General
6. upload your Quantum Odyssey puzzle file "puzzle_name.qpf" on the test_server.html
7. Server convets the puzzle file to a Qiskit circuit and returns qasm decomposition of the circuit and the result of simulation in Qiskit for 100 shots.



## Project Organization
-------------
    │
    ├── circuits                                    
    │   ├── odyssey_circuits                  < store here QO puzzle files you want to use with Qsiris            
    │   └── qiskit_to_odyssey                 < QO puzzle files made with example_qiskit_to_odyssey.ipynb 
    │
    ├── img                                   < Images showing final results from examples
    │   ├── qiskit_circuit_diagram.png
    │   ├── qiskit_circuit_to_QO.png
    │   └── qo_circuit_as_1gate.png
    │
    ├── project_qsiris                        <  Backend code for Qsiris 
    │   ├── conversion_gates.py                      
    │   ├── conversion_intermediates.py
    │   ├── conversion_qiskit_qo.py
    │   └── conversion_qo_qiskit.py    
    │
    ├── tamplates                       
    │   └── test_server.html                   < use this html page to convert QO to  Qiskit 
    │
    ├── README.md
    ├── example.py                            < Run from console
    ├── example_odyssey_to_qiskit.ipynb       < Use this to convert QO to Qiskit 
    ├── example_qiskit_to_odyssey.ipynb       < Use this to convert Qiskit to QO 
    ├── qsiris_api.py                         < Backend for qsiris_cloud
    ├── qsiris_cloud.py                       < Run this to start the server
    ├── requirements.txt
    └── requirements_server.txt               < Requirements just for the server 


from qiskit import Aer, execute
from qiskit import QuantumCircuit
from qiskit import IBMQ
from qiskit.tools.monitor import job_monitor
import flask

from project_qsiris.conversion_qo_qiskit import *

def qiskit_test():

    # test circuit
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    circ.measure_all()

    backend = Aer.get_backend("qasm_simulator")
    result = execute(circ, backend=backend, shots=10).result()
    counts = result.get_counts()

    return counts



def execute_qiskit(res):

    qc,qiskit_circuit = odyssey_to_qiskit(res,
                           incl_initial_state = False,
                           use_barrier = True,
                           incl_all_measurements = True)

    backend = Aer.get_backend("qasm_simulator")
    result = execute(qc, backend=backend, shots=int(res["QiskitShotsUsed"])).result()
    counts = result.get_counts()

    return counts


def decompose_qiskit(res):

    qc,qiskit_circuit = odyssey_to_qiskit(res,
                           incl_initial_state=False,
                           use_barrier=True,
                           incl_all_measurements=True)
    try:
        qasm_circuit = qc.qasm()
    except:
        qasm_circuit = (
            "The matrix is not unitary."
            " At the moment the error is probably caused by the fact that "
            "the numbers do not have enough decimals"
        )

    return qasm_circuit,qiskit_circuit


def real_device_qiskit(res):

    IBMQ.load_account()
    provider = IBMQ.get_provider('ibm-q')
    ibmq_lima = provider.get_backend("ibmq_lima")

    qc,qiskit_circuit = odyssey_to_qiskit(res,
                           incl_initial_state=False,
                           use_barrier=True,
                           incl_all_measurements=True)

    try:
        qasm_circuit = qc.qasm()
        job=execute(qc, backend=ibmq_lima, shots=100)
        job_monitor(job)
        result = job.result()
        counts = result.get_counts()

    except:
        qasm_circuit = (
            "The matrix is not unitary."
            " At the moment the error is probably caused by the fact that "
            "the numbers do not have enough decimals"
        )
    result = {"ibmq_lima_counts": counts, "qasm_circuit": qasm_circuit}
    return result

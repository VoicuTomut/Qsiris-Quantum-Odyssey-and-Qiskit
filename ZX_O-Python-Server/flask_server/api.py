from conversion_qo_qiskit import *
from qiskit import Aer, execute
from qiskit import QuantumCircuit
from qiskit import IBMQ
from qiskit.tools.monitor import job_monitor

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

    nr_q = get_nr_q(res)
    qc = QuantumCircuit(nr_q)

    add_gates(res, qc, barrier=True)

    qc.measure_all()
    backend = Aer.get_backend("qasm_simulator")
    result = execute(qc, backend=backend, shots=100).result()
    counts = result.get_counts()

    return counts


def decompose_qiskit(res):

    nr_q = get_nr_q(res)
    qc = QuantumCircuit(nr_q)
    add_gates(res, qc, barrier=True)
    qc.measure_all()

    try:
        qasm_circuit = qc.qasm()
    except:
        qasm_circuit = (
            "The matrix is not unitary."
            " At the moment the error is probably caused by the fact that the numbers do not have enough decimals"
        )

    return qasm_circuit


def real_device_qiskit(res):

    IBMQ.load_account()
    provider =IBMQ.get_provider('ibm-q')
    ibmq_lima=provider.get_backend("ibmq_lima")

    nr_q = get_nr_q(res)
    qc = QuantumCircuit(nr_q)
    add_gates(res, qc, barrier=True)
    qc.measure_all()

    try:
        qasm_circuit = qc.qasm()
        job=execute(qc, backend=ibmq_lima, shots=100)
        job_monitor(job)
        result = job.result()
        counts = result.get_counts()

    except:
        qasm_circuit = (
            "The matrix is not unitary."
            " At the moment the error is probably caused by the fact that the numbers do not have enough decimals"
        )
    result = {"ibmq_lima_counts": counts, "qasm_circuit": qasm_circuit}
    return result

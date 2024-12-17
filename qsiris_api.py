from qiskit import transpile
# from qiskit import QuantumCircuit
# from qiskit import IBMQ
# from qiskit.tools.monitor import job_monitor
from qiskit_aer import AerSimulator
from project_qsiris.conversion_qo_qiskit import *

def qiskit_test():

    # test circuit
    circ = QuantumCircuit(2)
    circ.h(0)
    circ.cx(0, 1)
    circ.measure_all()


    simulator = AerSimulator()
    compiled_circuit = transpile(circ, simulator)
    sim_result = simulator.run(compiled_circuit, shots=100).result()
    counts = sim_result.get_counts()

    return counts


def execute_qiskit(res):

    qc = odyssey_to_qiskit(res,
                           incl_initial_state = False,
                           use_barrier = True,
                           incl_all_measurements = True)

    simulator = AerSimulator()
    compiled_circuit = transpile(qc, simulator)
    sim_result = simulator.run(compiled_circuit, shots=100).result()
    counts = sim_result.get_counts()

    return counts


def decompose_qiskit(res):

    qc = odyssey_to_qiskit(res,
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

    return qasm_circuit

#
# def real_device_qiskit(res):
#
#     IBMQ.load_account()
#     provider = IBMQ.get_provider('ibm-q')
#     ibmq_lima = provider.get_backend("ibmq_lima")
#
#     qc = odyssey_to_qiskit(res,
#                            incl_initial_state=False,
#                            use_barrier=True,
#                            incl_all_measurements=True)
#
#     try:
#         qasm_circuit = qc.qasm()
#         job=execute(qc, backend=ibmq_lima, shots=100)
#         job_monitor(job)
#         result = job.result()
#         counts = result.get_counts()
#
#     except:
#         qasm_circuit = (
#             "The matrix is not unitary."
#             " At the moment the error is probably caused by the fact that "
#             "the numbers do not have enough decimals"
#         )
#     result = {"ibmq_lima_counts": counts, "qasm_circuit": qasm_circuit}
#     return result

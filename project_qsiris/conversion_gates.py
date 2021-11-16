import numpy as np
import cmath

c0 = {"Real": 0.0, "Imaginary": 0.0, "Magnitude": 0.0, "Phase": 0.0}
c1 = {"Real": 1.0, "Imaginary": 0.0, "Magnitude": 0.0, "Phase": 0.0}

def _odyssey_to_complex(comp):
    """
    :param comp: complex number as a dictionary
    :return:'complex'

    #example:
    comp={'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}
    comp_nr=get_complex(comp)
    print("Complex number:",comp_nr)
    """
    return comp["Real"] + 1j * comp["Imaginary"]

def _complex_to_odyssey(com):
    """
    :param com:'complex'
    :return: dictionary with the following structure:
    {'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}
    """
    return {
        "Real": com.real,
        "Imaginary": com.imag,
        "Magnitude": abs(com),
        "Phase": cmath.phase(com),
    }


def _vector_to_odyssey(vec):
    """
    :param vec: vector of complex numbers.
    :return: vector of dictionaries with the following structure:
    {'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}
    """

    v = []
    for i in vec:
        l=_complex_to_odyssey(i)
        v.append(l)
    return v


def _matrix_to_odyssey(mat):
    """
    :param mat: matrix of complex numbers
    :return: matrix of dictionaries with the following structure:
    ex:
    {'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}
    """
    m = []
    for i in mat:
        m.append(_vector_to_odyssey(i))

    return m


def _transpose_list(A):
    """
    :param A: []
    :return: transpose of A
    """

    c = len(A[0])
    l = len(A)

    B = [["" for i in range(l)] for j in range(c)]

    b_c = 0

    for j in range(c):
        for i in range(l):
            B[j][i] = A[i][j]
            B[j][i]['CircuitPosition']={'Item1':j,'Item2':i}
            B[j][i]["ID"] = j + j * i

    '''
    for gate in A:
        print(gate)
        gate['CircuitPosition']={'Item1':j,Item1':i}
        gate["ID"] = j+j*i

        B[i][j] = gate
    '''
    return B


def _transpose_list2(L,nr_q):
    """
    :param A: []
    :return: transpose of A
    """

    A = []
    for line in L:
        for gate in line:
            A.append(gate)
    c = nr_q
    l = int(len(A) / nr_q)

    B = [["" for i in range(c)] for j in range(l)]

    for gate in A:

        j=gate['CircuitPosition']['Item1']
        i=gate['CircuitPosition']['Item2']
        print("i",i)
        print("j", j)
        B[i][j] = gate
    return B


def _get_odyssey_gate(name, matrix, i_d=9, t=8,
                      icon_path="Artwork/GatesIcons/CustomGate"):
    """
    :param name: (name of the gate) str
    :param matrix: (unitary matrix)np.array
    :param i_d: (ID)int
    :param t: (gate Type)int
    :param icon_path: (path to the gate icon)str
    :return: gate as a dictionary with the following structure:
    ex:
    {'ID': 3,
       'Name': 'X',
       'Type': 3,
       'IconPath': 'Artwork/GatesIcons/XGate',
       'CompatibleQubits': 1,
       'DefinitionMatrix': [[{'Real': 0.0,'Imaginary': 0.0,'Magnitude': 0.0,'Phase': 0.0},
         {'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0}],
        [{'Real': 1.0, 'Imaginary': 0.0, 'Magnitude': 1.0, 'Phase': 0.0},
         {'Real': 0.0, 'Imaginary': 0.0, 'Magnitude': 0.0, 'Phase': 0.0}]]}

    """
    gate = {}
    gate["ID"] = i_d
    gate["Name"] = name
    gate["Type"] = t
    gate["IconPath"] = icon_path
    gate["CompatibleQubits"] = int(np.log2(len(matrix)))
    gate["DefinitionMatrix"] = _matrix_to_odyssey(matrix)  # p.matrice

    return gate


I = _get_odyssey_gate(
    name="I",
    matrix=[[1.0, 0.0], [0.0, 1.0]],
    i_d=5,
    t=0,
    icon_path="Artwork/GatesIcons/IGate",
)

X = _get_odyssey_gate(
    name="X",
    matrix=[[0.0, 1.0], [1.0, 0.0]],
    i_d=3,
    t=3,
    icon_path="Artwork/GatesIcons/XGate",
)

Y = _get_odyssey_gate(
    name="Y",
    matrix=[[0.0, 0.0 - 1j], [0.0 + 1j, 0.0]],
    i_d=2,
    t=5,
    icon_path="Artwork/GatesIcons/YGate",
)

Z = _get_odyssey_gate(
    name="Z",
    matrix=[[1.0, 0.0], [0.0, -1.0]],
    i_d=1,
    t=1,
    icon_path="Artwork/GatesIcons/ZGate",
)

F = _get_odyssey_gate(
    name="Filler",
    matrix=[[1.0, 0.0], [0.0, 1.0]],
    i_d=1010,
    t=7,
    icon_path="Artwork/GatesIcons/FillerGate",
)

CT = _get_odyssey_gate(
    name="CTRL",
    matrix=[[0.0, 0.0], [0.0, 1.0]],
    i_d=5,
    t=6,
    icon_path="Artwork/GatesIcons/CTRLGate",
)

H = _get_odyssey_gate(
    name="H",
    matrix=[[1 / np.sqrt(2), 1 / np.sqrt(2)],
            [1 / np.sqrt(2), -1 / np.sqrt(2)]],
    i_d=0,
    t=2,
    icon_path="Artwork/GatesIcons/HGate",
)

Gates_list = {"h": H, "x": X, "z": Z}
import sympy as sp


def matrix_determinant(matrix_data):
    matrix = sp.Matrix(matrix_data)
    return matrix.det()


def matrix_inverse(matrix_data):
    matrix = sp.Matrix(matrix_data)
    return matrix.inv()


def matrix_transpose(matrix_data):
    matrix = sp.Matrix(matrix_data)
    return matrix.T


def matrix_rank(matrix_data):
    matrix = sp.Matrix(matrix_data)
    return matrix.rank()


def matrix_eigenvalues(matrix_data):
    matrix = sp.Matrix(matrix_data)
    return matrix.eigenvals()


def matrix_multiply(matrix_a, matrix_b):
    matrix_a = sp.Matrix(matrix_a)
    matrix_b = sp.Matrix(matrix_b)

    return matrix_a * matrix_b
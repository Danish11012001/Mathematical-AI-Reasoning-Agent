import sympy as sp


def matrix_determinant(matrix_data):
    matrix = sp.Matrix(matrix_data)
    return matrix.det()


def matrix_inverse(matrix_data):
    matrix = sp.Matrix(matrix_data)
    return matrix.inv()
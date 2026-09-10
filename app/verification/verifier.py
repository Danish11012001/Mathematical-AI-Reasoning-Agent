import sympy as sp


# =========================
# EQUATION VERIFICATION
# =========================

def verify_equation(equation_text, solutions):
    x = sp.symbols('x')

    if "=" in equation_text:
        left, right = equation_text.split("=")

        left = sp.sympify(left)
        right = sp.sympify(right)

        for solution in solutions:
            result = sp.simplify(
                left.subs(x, solution) - right.subs(x, solution)
            )

            if result != 0:
                return False

        return True

    else:
        expression = sp.sympify(equation_text)

        for solution in solutions:
            result = sp.simplify(
                expression.subs(x, solution)
            )

            if result != 0:
                return False

        return True


# =========================
# MATRIX DETERMINANT
# =========================

def verify_determinant(matrix_data, result):

    matrix = sp.Matrix(matrix_data)

    expected = matrix.det()

    return sp.simplify(expected - result) == 0


# =========================
# MATRIX INVERSE
# =========================

def verify_inverse(matrix_data, result):

    matrix = sp.Matrix(matrix_data)
    inverse = sp.Matrix(result)

    # A × A⁻¹ should equal Identity Matrix
    identity = matrix * inverse

    return identity == sp.eye(matrix.rows)


# =========================
# MATRIX TRANSPOSE
# =========================

def verify_transpose(matrix_data, result):

    matrix = sp.Matrix(matrix_data)
    transpose = sp.Matrix(result)

    return transpose == matrix.T


# =========================
# MATRIX RANK
# =========================

def verify_rank(matrix_data, result):

    matrix = sp.Matrix(matrix_data)

    expected = matrix.rank()

    return expected == result


# =========================
# MATRIX EIGENVALUES
# =========================

def verify_eigenvalues(matrix_data, result):

    matrix = sp.Matrix(matrix_data)

    # SymPy returns eigenvalues along with
    # their algebraic multiplicities.
    expected = matrix.eigenvals()

    # The matrix_eigenvalues() function returns
    # a dictionary such as:
    #
    # {2: 2, 3: 1}
    #
    # where:
    # eigenvalue 2 has multiplicity 2
    # eigenvalue 3 has multiplicity 1

    if not isinstance(result, dict):
        return False

    # Compare the complete eigenvalue dictionary.
    # This checks both:
    #
    # 1. Eigenvalue values
    # 2. Algebraic multiplicities

    return expected == result


# =========================
# MATRIX MULTIPLICATION
# =========================

def verify_matrix_multiply(matrix_a, matrix_b, result):

    matrix_a = sp.Matrix(matrix_a)
    matrix_b = sp.Matrix(matrix_b)
    result = sp.Matrix(result)

    # Calculate the expected product independently.
    expected = matrix_a * matrix_b

    # Compare the calculated result
    # with the expected matrix.
    return result == expected


# ==================================================
# DERIVATIVE VERIFICATION
# ==================================================

def verify_derivative(expression, result):

    x = sp.symbols('x')

    expression = sp.sympify(expression)

    expected = sp.diff(expression, x)

    return sp.simplify(expected - result) == 0


# ==================================================
# INTEGRAL VERIFICATION
# ==================================================

def verify_integral(expression, result):

    x = sp.symbols('x')

    expression = sp.sympify(expression)

    # Differentiate the calculated integral.
    # The derivative should reproduce the
    # original expression.

    expected = sp.diff(result, x)

    return sp.simplify(expected - expression) == 0
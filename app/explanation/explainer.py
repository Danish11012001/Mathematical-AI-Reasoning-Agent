import sympy as sp


def explain_linear_equation(equation_text):
    """
    Generate step-by-step explanation for a linear equation.
    """

    x = sp.symbols("x")

    left, right = equation_text.split("=")

    left = sp.sympify(left)
    right = sp.sympify(right)

    solution = sp.solve(sp.Eq(left, right), x)

    steps = []

    steps.append(f"Original equation: {left} = {right}")

    # Move everything to one side
    expression = sp.expand(left - right)

    steps.append(
        f"Move all terms to the left side: {expression} = 0"
    )

    coefficient = expression.coeff(x)
    constant = expression.subs(x, 0)

    if coefficient != 0:

        steps.append(
            f"Isolate x: {coefficient}x = {-constant}"
        )

        steps.append(
            f"Divide both sides by {coefficient}"
        )

    steps.append(
        f"Therefore, x = {solution[0]}"
    )

    return steps


def explain_quadratic_equation(equation_text):
    """
    Generate step-by-step explanation for a quadratic equation.
    """

    x = sp.symbols("x")

    left, right = equation_text.split("=")

    left = sp.sympify(left)
    right = sp.sympify(right)

    expression = sp.expand(left - right)

    a = expression.coeff(x, 2)
    b = expression.coeff(x, 1)
    c = expression.coeff(x, 0)

    discriminant = sp.simplify(b**2 - 4*a*c)

    solutions = sp.solve(sp.Eq(left, right), x)

    steps = []

    steps.append(
        f"Original equation: {left} = {right}"
    )

    steps.append(
        f"Rewrite in standard form: {expression} = 0"
    )

    steps.append(
        f"Identify coefficients: a = {a}, b = {b}, c = {c}"
    )

    steps.append(
        f"Calculate the discriminant: b² - 4ac"
    )

    steps.append(
        f"Discriminant = {discriminant}"
    )

    steps.append(
        "Use the quadratic formula:"
    )

    steps.append(
        "x = (-b ± √(b² - 4ac)) / (2a)"
    )

    steps.append(
        f"Substitute the values: "
        f"x = (-({b}) ± √({discriminant})) / (2({a}))"
    )

    steps.append(
        f"Solutions: {solutions}"
    )

    return steps


def explain_derivative(expression):
    """
    Generate a basic step-by-step explanation for polynomial derivatives.
    """

    x = sp.symbols("x")

    expr = sp.sympify(expression)

    steps = []

    steps.append(f"Given function: f(x) = {expr}")

    terms = sp.Add.make_args(sp.expand(expr))

    steps.append("Differentiate each term separately.")

    for term in terms:

        derivative_term = sp.diff(term, x)

        steps.append(
            f"d/dx ({term}) = {derivative_term}"
        )

    result = sp.diff(expr, x)

    steps.append(
        f"Therefore, f'(x) = {result}"
    )

    return steps


def explain_integral(expression):
    import sympy as sp

    x = sp.symbols("x")

    expression = sp.sympify(expression)
    result = sp.integrate(expression, x)

    steps = [
        f"Original expression: {expression}",
        "Identify the variable of integration: x",
        f"Integrate each term with respect to x.",
        f"Integral result: {result}",
        "Add the constant of integration: C"
    ]

    steps[-2] = f"Antiderivative: {result}"

    steps.append(
        f"Final answer: {result} + C"
    )

    return steps
# =========================
# MATRIX DETERMINANT
# =========================

def explain_determinant(matrix_data):
    matrix = sp.Matrix(matrix_data)

    steps = []

    steps.append(f"Given matrix:\n{matrix}")

    rows, cols = matrix.shape

    if rows != cols:
        steps.append("A determinant can only be calculated for a square matrix.")
        return steps

    if rows == 2:
        a = matrix[0, 0]
        b = matrix[0, 1]
        c = matrix[1, 0]
        d = matrix[1, 1]

        steps.append(
            "For a 2 × 2 matrix, use: det(A) = ad - bc"
        )

        steps.append(
            f"Substitute the values: det(A) = ({a})({d}) - ({b})({c})"
        )

        steps.append(
            f"Calculate: det(A) = {a*d} - {b*c}"
        )

        result = matrix.det()

        steps.append(
            f"Therefore, det(A) = {result}"
        )

    else:
        result = matrix.det()

        steps.append(
            "The determinant is calculated using matrix expansion."
        )

        steps.append(
            f"Therefore, det(A) = {result}"
        )

    return steps


# =========================
# MATRIX INVERSE
# =========================

def explain_inverse(matrix_data):
    matrix = sp.Matrix(matrix_data)

    steps = []

    steps.append(f"Given matrix:\n{matrix}")

    if matrix.rows != matrix.cols:
        steps.append(
            "The matrix must be square to calculate its inverse."
        )
        return steps

    determinant = matrix.det()

    steps.append(
        f"Step 1: Calculate the determinant: det(A) = {determinant}"
    )

    if determinant == 0:
        steps.append(
            "Since the determinant is 0, the matrix has no inverse."
        )
        return steps

    if matrix.rows == 2:
        a = matrix[0, 0]
        b = matrix[0, 1]
        c = matrix[1, 0]
        d = matrix[1, 1]

        steps.append(
            "For a 2 × 2 matrix:"
        )

        steps.append(
            "A⁻¹ = 1/(ad-bc) × [[d,-b],[-c,a]]"
        )

        steps.append(
            f"Substitute: A⁻¹ = 1/{determinant} × "
            f"[[{d},{-b}],[{-c},{a}]]"
        )

    result = matrix.inv()

    steps.append(
        f"Therefore, A⁻¹ =\n{result}"
    )

    return steps


# =========================
# MATRIX TRANSPOSE
# =========================

def explain_transpose(matrix_data):
    matrix = sp.Matrix(matrix_data)

    steps = []

    steps.append(f"Given matrix:\n{matrix}")

    steps.append(
        "Transpose is obtained by converting rows into columns."
    )

    result = matrix.T

    steps.append(
        f"Therefore, Aᵀ =\n{result}"
    )

    return steps


# =========================
# MATRIX RANK
# =========================

def explain_rank(matrix_data):
    matrix = sp.Matrix(matrix_data)

    steps = []

    steps.append(f"Given matrix:\n{matrix}")

    steps.append(
        "Convert the matrix to row-reduced form."
    )

    rref_matrix, pivots = matrix.rref()

    steps.append(
        f"Row-reduced form:\n{rref_matrix}"
    )

    steps.append(
        f"Number of pivot columns = {len(pivots)}"
    )

    result = matrix.rank()

    steps.append(
        f"Therefore, rank(A) = {result}"
    )

    return steps


# =========================
# MATRIX EIGENVALUES
# =========================

def explain_eigenvalues(matrix_data):
    matrix = sp.Matrix(matrix_data)

    steps = []

    steps.append(f"Given matrix:\n{matrix}")

    x = sp.symbols("x")

    characteristic_polynomial = matrix.charpoly(x).as_expr()

    steps.append(
        f"Form the characteristic equation:"
    )

    steps.append(
        f"det(A - λI) = {characteristic_polynomial}"
    )

    eigenvalues = matrix.eigenvals()

    steps.append(
        f"Solve the characteristic equation."
    )

    steps.append(
        f"Eigenvalues = {eigenvalues}"
    )

    return steps
import sympy as sp

from tools.equations import solve_equation

from tools.calculus import (
    derivative,
    integral
)

from tools.matrices import (
    matrix_determinant,
    matrix_inverse,
    matrix_transpose,
    matrix_rank,
    matrix_eigenvalues,
    matrix_multiply
)

from verification.verifier import (
    verify_equation,
    verify_derivative,
    verify_integral,
    verify_determinant,
    verify_inverse,
    verify_transpose,
    verify_rank,
    verify_eigenvalues,
    verify_matrix_multiply
)

from explanation.explainer import (
    explain_linear_equation,
    explain_quadratic_equation,
    explain_derivative,
    explain_integral,
    explain_determinant,
    explain_inverse,
    explain_transpose,
    explain_rank,
    explain_eigenvalues
)

from agent.planner import create_plan
from agent.tool_selector import select_tool


# ==================================================
# MATRIX INPUT
# ==================================================

def get_matrix():

    while True:

        try:
            rows = int(input("Enter number of rows: "))
            cols = int(input("Enter number of columns: "))

            if rows <= 0 or cols <= 0:
                print("Rows and columns must be greater than 0.")
                continue

            matrix = []

            for i in range(rows):

                while True:

                    values = input(
                        f"Enter row {i + 1} "
                        f"({cols} values separated by spaces): "
                    ).split()

                    if len(values) != cols:
                        print(
                            f"Please enter exactly {cols} values."
                        )
                        continue

                    try:

                        row = [
                            sp.sympify(value)
                            for value in values
                        ]

                        matrix.append(row)

                        break

                    except Exception:

                        print(
                            "Please enter valid numbers."
                        )

            return matrix

        except ValueError:

            print(
                "Please enter valid integer values."
            )


# ==================================================
# EQUATION HANDLER
# ==================================================

def handle_equation(user_input):

    if user_input.lower().startswith("solve"):

        expression = user_input[5:].strip()

    else:

        expression = user_input

    result = solve_equation(expression)

    verification = verify_equation(
        expression,
        result
    )

    x = sp.symbols("x")

    if "=" in expression:

        left, right = expression.split("=")

        equation_expression = sp.expand(
            sp.sympify(left)
            -
            sp.sympify(right)
        )

    else:

        equation_expression = sp.sympify(
            expression
        )

    degree = sp.degree(
        equation_expression,
        x
    )

    if degree == 1:

        steps = explain_linear_equation(
            expression
        )

    elif degree == 2:

        steps = explain_quadratic_equation(
            expression
        )

    else:

        steps = [
            f"Original equation: {expression}",
            f"Detected polynomial degree: {degree}",
            f"Solutions calculated using SymPy: {result}"
        ]

    return {
        "operation": "Equation Solving",
        "result": result,
        "verification": verification,
        "steps": steps
    }


# ==================================================
# DERIVATIVE HANDLER
# ==================================================

def handle_derivative(user_input):

    if user_input.lower().startswith("derivative"):

        expression = user_input[10:].strip()

    else:

        expression = user_input

    result = derivative(
        expression
    )

    verification = verify_derivative(
        expression,
        result
    )

    steps = explain_derivative(
        expression
    )

    return {
        "operation": "Derivative",
        "result": result,
        "verification": verification,
        "steps": steps
    }

# ==================================================
# INTEGRAL HANDLER
# ==================================================

def handle_integral(user_input):

    if user_input.lower().startswith("integral"):

        expression = user_input[8:].strip()

    else:

        expression = user_input

    result = integral(
        expression
    )

    verification = verify_integral(
        expression,
        result
    )

    steps = explain_integral(
        expression
    )

    return {
        "operation": "Integral",
        "result": result,
        "verification": verification,
        "steps": steps
    }

# ==================================================
# MATRIX DETERMINANT HANDLER
# ==================================================

def handle_determinant():

    matrix = get_matrix()

    result = matrix_determinant(
        matrix
    )

    verification = verify_determinant(
        matrix,
        result
    )

    steps = explain_determinant(
        matrix
    )

    return {
        "operation": "Matrix Determinant",
        "matrix": matrix,
        "result": result,
        "verification": verification,
        "steps": steps
    }


# ==================================================
# MATRIX INVERSE HANDLER
# ==================================================

def handle_inverse():

    matrix = get_matrix()

    if len(matrix) != len(matrix[0]):

        return {
            "operation": "Matrix Inverse",
            "error":
                "Matrix inverse requires "
                "a square matrix."
        }

    result = matrix_inverse(
        matrix
    )

    verification = verify_inverse(
        matrix,
        result
    )

    steps = explain_inverse(
        matrix
    )

    return {
        "operation": "Matrix Inverse",
        "matrix": matrix,
        "result": result,
        "verification": verification,
        "steps": steps
    }


# ==================================================
# MATRIX TRANSPOSE HANDLER
# ==================================================

def handle_transpose():

    matrix = get_matrix()

    result = matrix_transpose(
        matrix
    )

    verification = verify_transpose(
        matrix,
        result
    )

    steps = explain_transpose(
        matrix
    )

    return {
        "operation": "Matrix Transpose",
        "matrix": matrix,
        "result": result,
        "verification": verification,
        "steps": steps
    }


# ==================================================
# MATRIX RANK HANDLER
# ==================================================

def handle_rank():

    matrix = get_matrix()

    result = matrix_rank(
        matrix
    )

    verification = verify_rank(
        matrix,
        result
    )

    steps = explain_rank(
        matrix
    )

    return {
        "operation": "Matrix Rank",
        "matrix": matrix,
        "result": result,
        "verification": verification,
        "steps": steps
    }


# ==================================================
# MATRIX EIGENVALUES HANDLER
# ==================================================

def handle_eigenvalues():

    matrix = get_matrix()

    result = matrix_eigenvalues(
        matrix
    )

    verification = verify_eigenvalues(
        matrix,
        result
    )

    steps = explain_eigenvalues(
        matrix
    )

    return {
        "operation": "Matrix Eigenvalues",
        "matrix": matrix,
        "result": result,
        "verification": verification,
        "steps": steps
    }


# ==================================================
# MATRIX MULTIPLICATION HANDLER
# ==================================================

def handle_multiply():

    print("\nEnter the first matrix:")
    matrix_a = get_matrix()

    print("\nEnter the second matrix:")
    matrix_b = get_matrix()

    # Matrix multiplication condition:
    # columns of A == rows of B

    if len(matrix_a[0]) != len(matrix_b):

        return {
            "operation": "Matrix Multiplication",
            "matrix_a": matrix_a,
            "matrix_b": matrix_b,
            "error":
                "Matrix multiplication is not possible. "
                "The number of columns in the first matrix "
                "must equal the number of rows in the second matrix."
        }

    result = matrix_multiply(
        matrix_a,
        matrix_b
    )

    verification = verify_matrix_multiply(
        matrix_a,
        matrix_b,
        result
    )

    # Step-by-step explanation
    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])
    cols_b = len(matrix_b[0])

    steps = [
        "Write the first matrix A.",
        "Write the second matrix B.",
        (
            f"Matrix A has dimensions "
            f"{rows_a} × {cols_a}."
        ),
        (
            f"Matrix B has dimensions "
            f"{len(matrix_b)} × {cols_b}."
        ),
        (
            "Matrix multiplication is possible because "
            "the columns of A equal the rows of B."
        ),
        (
            "Multiply each row of A by each column of B "
            "and add the corresponding products."
        ),
        f"Resulting matrix has dimensions {rows_a} × {cols_b}.",
        f"Final result: {result}"
    ]

    return {
        "operation": "Matrix Multiplication",
        "matrix_a": matrix_a,
        "matrix_b": matrix_b,
        "result": result,
        "verification": verification,
        "steps": steps
    }


# ==================================================
# MAIN AGENT
# ==================================================

def run_agent(user_input):

    # --------------------------------------------------
    # STEP 1: CREATE PLAN
    # --------------------------------------------------

    plan = create_plan(
        user_input
    )

    # --------------------------------------------------
    # STEP 2: SELECT TOOL
    # --------------------------------------------------

    tool = select_tool(
        plan
    )

    # --------------------------------------------------
    # UNKNOWN OPERATION
    # --------------------------------------------------

    if tool is None:

        return {
            "error":
                "I could not understand the "
                "mathematical operation.",
            "plan": plan
        }

    try:

        # --------------------------------------------------
        # EQUATION
        # --------------------------------------------------

        if tool == "solve_equation":

            result = handle_equation(
                user_input
            )

        # --------------------------------------------------
        # DERIVATIVE
        # --------------------------------------------------

        elif tool == "derivative":

            result = handle_derivative(
                user_input
            )

        # --------------------------------------------------
        # INTEGRAL
        # --------------------------------------------------

        elif tool == "integral":

            result = handle_integral(
                user_input
            )

        # --------------------------------------------------
        # MATRIX DETERMINANT
        # --------------------------------------------------

        elif tool == "matrix_determinant":

            result = handle_determinant()

        # --------------------------------------------------
        # MATRIX INVERSE
        # --------------------------------------------------

        elif tool == "matrix_inverse":

            result = handle_inverse()

        # --------------------------------------------------
        # MATRIX TRANSPOSE
        # --------------------------------------------------

        elif tool == "matrix_transpose":

            result = handle_transpose()

        # --------------------------------------------------
        # MATRIX RANK
        # --------------------------------------------------

        elif tool == "matrix_rank":

            result = handle_rank()

        # --------------------------------------------------
        # MATRIX EIGENVALUES
        # --------------------------------------------------

        elif tool == "matrix_eigenvalues":

            result = handle_eigenvalues()

        # --------------------------------------------------
        # MATRIX MULTIPLICATION
        # --------------------------------------------------

        elif tool == "matrix_multiply":

            result = handle_multiply()

        # --------------------------------------------------
        # TOOL NOT IMPLEMENTED
        # --------------------------------------------------

        else:

            return {
                "error":
                    f"Tool '{tool}' is not implemented.",
                "plan": plan,
                "selected_tool": tool
            }

        # --------------------------------------------------
        # ADD PLAN INFORMATION
        # --------------------------------------------------

        result["plan"] = plan
        result["selected_tool"] = tool

        return result

    except Exception as e:

        return {
            "operation": plan["operation"],
            "error": str(e),
            "plan": plan,
            "selected_tool": tool
        }

#agent.py
import sympy as sp
import ast

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
from agent.llm_planner import create_llm_plan
from agent.tool_selector import select_tool


# ==================================================
# MATRIX INPUT
# ==================================================

def get_matrix():

    while True:

        try:

            rows = int(
                input("Enter number of rows: ")
            )

            cols = int(
                input("Enter number of columns: ")
            )

            if rows <= 0 or cols <= 0:

                print(
                    "Rows and columns must be greater than 0."
                )

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
# MATRIX VALIDATION
# ==================================================

def validate_matrix(matrix):

    if not isinstance(matrix, list):
        return False

    if len(matrix) == 0:
        return False

    if not all(
            isinstance(row, list)
            for row in matrix
    ):
        return False

    if not all(
            len(row) == len(matrix[0])
            for row in matrix
    ):
        return False

    if len(matrix[0]) == 0:
        return False

    return True


def normalize_matrix(matrix):

    if not validate_matrix(matrix):

        raise ValueError(
            "Invalid matrix format."
        )

    return [
        [
            sp.sympify(value)
            for value in row
        ]
        for row in matrix
    ]


# ==================================================
# MATRIX EXTRACTION FALLBACK
# ==================================================

def extract_matrices_from_input(user_input):

    """
    Extract matrix-like Python/JSON arrays from
    the user's natural-language request.

    Example:

    Multiply [[1,2],[3,4]] and [[5,6],[7,8]]

    returns:

    [
        [[1,2],[3,4]],
        [[5,6],[7,8]]
    ]
    """

    matrices = []

    text = user_input

    depth = 0
    start = None

    for index, char in enumerate(text):

        if char == "[":

            if depth == 0:
                start = index

            depth += 1

        elif char == "]":

            if depth > 0:

                depth -= 1

                if depth == 0 and start is not None:

                    candidate = text[
                        start:index + 1
                    ]

                    try:

                        value = ast.literal_eval(
                            candidate
                        )

                        if validate_matrix(value):

                            matrices.append(
                                value
                            )

                    except Exception:

                        pass

                    start = None

    return matrices


# ==================================================
# EXPRESSION EXTRACTION FALLBACK
# ==================================================

def get_expression(plan, user_input):

    expression = plan.get("expression")

    if expression is not None:

        expression = str(expression).strip()

        if expression:
            return expression

    text = user_input.strip()
    text = text.rstrip("?!.")

    operation = plan.get(
        "operation",
        ""
    ).lower()

    lower_text = text.lower()

    # --------------------------------------------------
    # EQUATION / ROOTS
    # --------------------------------------------------

    if operation == "solve":

        markers = [
            "equation given",
            "the equation",
            "solve equation",
            "solve",
            "roots of",
            "root of",
            "roots for",
            "root for",
            "find the roots of",
            "find roots of",
            "find the root of",
            "find root of"
        ]

        # Try the longest/more specific phrases first
        markers = sorted(
            markers,
            key=len,
            reverse=True
        )

        for marker in markers:

            position = lower_text.find(marker)

            if position != -1:

                candidate = text[
                    position + len(marker):
                ].strip()

                candidate = candidate.lstrip(": ")

                if candidate.lower().startswith("given "):

                    candidate = candidate[
                        6:
                    ].strip()

                if candidate:
                    return candidate

    # --------------------------------------------------
    # DERIVATIVE
    # --------------------------------------------------

    elif operation == "derivative":

        markers = [
            "derivative of",
            "differentiate",
            "derivative",
            "rate of change of"
        ]

        markers = sorted(
            markers,
            key=len,
            reverse=True
        )

        for marker in markers:

            position = lower_text.find(marker)

            if position != -1:

                candidate = text[
                    position + len(marker):
                ].strip()

                candidate = candidate.lstrip(": ")

                if candidate:
                    return candidate

    # --------------------------------------------------
    # INTEGRAL
    # --------------------------------------------------

    elif operation == "integral":

        markers = [
            "integral of",
            "integrate",
            "integral"
        ]

        markers = sorted(
            markers,
            key=len,
            reverse=True
        )

        for marker in markers:

            position = lower_text.find(marker)

            if position != -1:

                candidate = text[
                    position + len(marker):
                ].strip()

                candidate = candidate.lstrip(": ")

                if candidate:
                    return candidate

    return user_input

# ==================================================
# EQUATION HANDLER
# ==================================================

def handle_equation(expression):

    # The LLM planner has already extracted the
    # mathematical expression. Do not parse natural
    # language again here.

    expression = str(expression).strip()

    if not expression:
        raise ValueError(
            "No mathematical expression was provided."
        )

    result = solve_equation(
        expression
    )

    verification = verify_equation(
        expression,
        result
    )

    x = sp.symbols("x")

    if "=" in expression:

        left, right = expression.split(
            "=",
            1
        )

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

        if "=" in expression:

            steps = explain_linear_equation(
                expression
            )

        else:

            polynomial = sp.Poly(
                equation_expression,
                x
            )

            a = polynomial.coeff_monomial(x)
            b = polynomial.coeff_monomial(1)

            steps = [
                f"Original expression: {expression}",
                f"Rewrite as an equation: {a}*x + {b} = 0",
                f"Move the constant term: {a}*x = {-b}",
                f"Divide by {a}: x = {-b}/{a}",
                f"Solution: {result}"
            ]

    elif degree == 2:

        # The quadratic explainer expects an equation
        # containing "=". For an expression such as
        # "3*x**2 - 12*x + 9", create a safe explanation
        # directly instead of sending the expression to
        # an explainer that tries to split on "=".

        if "=" in expression:

            steps = explain_quadratic_equation(
                expression
            )

        else:

            polynomial = sp.Poly(
                equation_expression,
                x
            )

            a = polynomial.coeff_monomial(x**2)
            b = polynomial.coeff_monomial(x)
            c = polynomial.coeff_monomial(1)

            discriminant = sp.expand(
                b**2 - 4*a*c
            )

            steps = [
                f"Original expression: {expression}",
                f"Rewrite in standard form: {a}*x**2 + {b}*x + {c} = 0",
                f"Identify coefficients: a = {a}, b = {b}, c = {c}",
                "Calculate the discriminant: b² - 4ac",
                f"Discriminant = {discriminant}",
                "Use the quadratic formula:",
                "x = (-b ± √(b² - 4ac)) / (2a)",
                f"Solutions: {result}"
            ]

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

    if user_input.lower().startswith(
            "derivative"
    ):

        expression = user_input[
            10:
        ].strip()

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

    if user_input.lower().startswith(
            "integral"
    ):

        expression = user_input[
            8:
        ].strip()

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

def handle_determinant(matrix=None):

    if matrix is None:

        matrix = get_matrix()

    matrix = normalize_matrix(
        matrix
    )

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

def handle_inverse(matrix=None):

    if matrix is None:

        matrix = get_matrix()

    matrix = normalize_matrix(
        matrix
    )

    if len(matrix) != len(matrix[0]):

        return {
            "operation": "Matrix Inverse",
            "matrix": matrix,
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

def handle_transpose(matrix=None):

    if matrix is None:

        matrix = get_matrix()

    matrix = normalize_matrix(
        matrix
    )

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

def handle_rank(matrix=None):

    if matrix is None:

        matrix = get_matrix()

    matrix = normalize_matrix(
        matrix
    )

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

def handle_eigenvalues(matrix=None):

    if matrix is None:

        matrix = get_matrix()

    matrix = normalize_matrix(
        matrix
    )

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

def handle_multiply(
        matrix_a=None,
        matrix_b=None
):

    if matrix_a is None:

        print(
            "\nEnter the first matrix:"
        )

        matrix_a = get_matrix()

    if matrix_b is None:

        print(
            "\nEnter the second matrix:"
        )

        matrix_b = get_matrix()

    matrix_a = normalize_matrix(
        matrix_a
    )

    matrix_b = normalize_matrix(
        matrix_b
    )

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

    rows_a = len(matrix_a)
    cols_a = len(matrix_a[0])

    rows_b = len(matrix_b)
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
            f"{rows_b} × {cols_b}."
        ),

        (
            "Matrix multiplication is possible because "
            "the columns of A equal the rows of B."
        ),

        (
            "Multiply each row of A by each column of B "
            "and add the corresponding products."
        ),

        (
            f"Resulting matrix has dimensions "
            f"{rows_a} × {cols_b}."
        ),

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
    # STEP 1: CREATE PLAN USING LLM
    # --------------------------------------------------

    planner_used = "LLM"

    try:

        plan = create_llm_plan(
            user_input
        )

        if not isinstance(plan, dict):

            raise ValueError(
                "LLM planner did not return a dictionary."
            )

        if "category" not in plan:

            raise ValueError(
                "LLM plan is missing category."
            )

        if "operation" not in plan:

            raise ValueError(
                "LLM plan is missing operation."
            )

    except Exception as e:

        print(
            "\nLLM planner failed."
        )

        print(
            f"Reason: {e}"
        )

        print(
            "Using keyword planner as fallback."
        )

        planner_used = "Keyword Fallback"

        plan = create_plan(
            user_input
        )

    # --------------------------------------------------
    # STEP 2: MATRIX DATA FALLBACK
    # --------------------------------------------------

    if plan.get("category") == "matrix":

        operation = plan.get(
            "operation"
        )

        matrices = extract_matrices_from_input(
            user_input
        )

        # Single matrix operation
        if operation in {
            "determinant",
            "inverse",
            "transpose",
            "rank",
            "eigenvalues"
        }:

            if "matrix" not in plan:

                if len(matrices) >= 1:

                    plan["matrix"] = matrices[0]

        # Matrix multiplication
        elif operation == "multiply":

            if (
                    "matrix_a" not in plan
                    and len(matrices) >= 1
            ):

                plan["matrix_a"] = matrices[0]

            if (
                    "matrix_b" not in plan
                    and len(matrices) >= 2
            ):

                plan["matrix_b"] = matrices[1]

    # --------------------------------------------------
    # STEP 3: SELECT TOOL
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
            "plan": plan,
            "planner_used": planner_used
        }

    try:

        # --------------------------------------------------
        # EQUATION
        # --------------------------------------------------

        if tool == "solve_equation":

            expression = get_expression(
                plan,
                user_input
            )

            result = handle_equation(
                expression
            )

        # --------------------------------------------------
        # DERIVATIVE
        # --------------------------------------------------

        elif tool == "derivative":

            expression = get_expression(
                plan,
                user_input
            )

            result = handle_derivative(
                expression
            )

        # --------------------------------------------------
        # INTEGRAL
        # --------------------------------------------------

        elif tool == "integral":

            expression = get_expression(
                plan,
                user_input
            )

            result = handle_integral(
                expression
            )

        # --------------------------------------------------
        # MATRIX DETERMINANT
        # --------------------------------------------------

        elif tool == "matrix_determinant":

            matrix = plan.get(
                "matrix"
            )

            if matrix is None:

                result = handle_determinant()

            else:

                result = handle_determinant(
                    matrix
                )

        # --------------------------------------------------
        # MATRIX INVERSE
        # --------------------------------------------------

        elif tool == "matrix_inverse":

            matrix = plan.get(
                "matrix"
            )

            if matrix is None:

                result = handle_inverse()

            else:

                result = handle_inverse(
                    matrix
                )

        # --------------------------------------------------
        # MATRIX TRANSPOSE
        # --------------------------------------------------

        elif tool == "matrix_transpose":

            matrix = plan.get(
                "matrix"
            )

            if matrix is None:

                result = handle_transpose()

            else:

                result = handle_transpose(
                    matrix
                )

        # --------------------------------------------------
        # MATRIX RANK
        # --------------------------------------------------

        elif tool == "matrix_rank":

            matrix = plan.get(
                "matrix"
            )

            if matrix is None:

                result = handle_rank()

            else:

                result = handle_rank(
                    matrix
                )

        # --------------------------------------------------
        # MATRIX EIGENVALUES
        # --------------------------------------------------

        elif tool == "matrix_eigenvalues":

            matrix = plan.get(
                "matrix"
            )

            if matrix is None:

                result = handle_eigenvalues()

            else:

                result = handle_eigenvalues(
                    matrix
                )

        # --------------------------------------------------
        # MATRIX MULTIPLICATION
        # --------------------------------------------------

        elif tool == "matrix_multiply":

            matrix_a = plan.get(
                "matrix_a"
            )

            matrix_b = plan.get(
                "matrix_b"
            )

            if (
                    matrix_a is None
                    or matrix_b is None
            ):

                result = handle_multiply()

            else:

                result = handle_multiply(
                    matrix_a,
                    matrix_b
                )

        # --------------------------------------------------
        # TOOL NOT IMPLEMENTED
        # --------------------------------------------------

        else:

            return {
                "error":
                    f"Tool '{tool}' is not implemented.",
                "plan": plan,
                "selected_tool": tool,
                "planner_used": planner_used
            }

        # --------------------------------------------------
        # ADD AGENT INFORMATION
        # --------------------------------------------------

        result["plan"] = plan

        result["selected_tool"] = tool

        result["planner_used"] = planner_used

        return result

    except Exception as e:

        return {
            "operation": plan.get(
                "operation",
                "unknown"
            ),
            "error": str(e),
            "plan": plan,
            "selected_tool": tool,
            "planner_used": planner_used
        }

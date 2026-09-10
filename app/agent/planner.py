def create_plan(user_input):
    """
    Analyze the user's request and create a basic
    mathematical plan.
    """

    text = user_input.lower().strip()

    # Equation
    if (
            text.startswith("solve")
            or "solve equation" in text
            or "find the root" in text
            or "find roots" in text
            or "find the solution" in text
    ):
        return {
            "category": "equation",
            "operation": "solve",
            "input": user_input
        }

    # Derivative
    if (
            text.startswith("derivative")
            or "differentiate" in text
    ):
        return {
            "category": "calculus",
            "operation": "derivative",
            "input": user_input
        }

    # Integral
    if (
            text.startswith("integral")
            or "integrate" in text
    ):
        return {
            "category": "calculus",
            "operation": "integral",
            "input": user_input
        }

    # Matrix determinant
    if "determinant" in text:
        return {
            "category": "matrix",
            "operation": "determinant",
            "input": user_input
        }

    # Matrix inverse
    if (
            "inverse matrix" in text
            or "matrix inverse" in text
            or text.startswith("inverse")
    ):
        return {
            "category": "matrix",
            "operation": "inverse",
            "input": user_input
        }

    # Matrix transpose
    if "transpose" in text:
        return {
            "category": "matrix",
            "operation": "transpose",
            "input": user_input
        }

    # Matrix rank
    if "rank" in text:
        return {
            "category": "matrix",
            "operation": "rank",
            "input": user_input
        }

    # Matrix eigenvalues
    if (
            "eigenvalue" in text
            or "eigenvalues" in text
    ):
        return {
            "category": "matrix",
            "operation": "eigenvalues",
            "input": user_input
        }

    if "multiply" in text or "multiplication" in text:
        return {
            "category": "matrix",
            "operation": "multiply",
            "input": user_input
        }

    return {
        "category": "unknown",
        "operation": "unknown",
        "input": user_input
    }
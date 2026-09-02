from tools.equations import solve_equation
from tools.calculus import derivative, integral
from verification.verifier import verify_equation


def run_agent(user_input):

    text = user_input.lower().strip()

    # -------------------------
    # EQUATION SOLVING
    # -------------------------

    if (
            text.startswith("solve")
            or "solve equation" in text
            or "find the root" in text
            or "find roots" in text
            or "find the solution" in text
    ):

        if text.startswith("solve"):
            expression = user_input[5:].strip()
        else:
            expression = user_input

        try:
            result = solve_equation(expression)

            verification = verify_equation(expression, result)

            return {
                "operation": "Equation Solving",
                "result": result,
                "verification": verification
            }

        except Exception as e:
            return {
                "operation": "Equation Solving",
                "error": str(e)
            }

    # -------------------------
    # DERIVATIVE
    # -------------------------

    elif (
            text.startswith("derivative")
            or "differentiate" in text
    ):

        if text.startswith("derivative"):
            expression = user_input[10:].strip()
        else:
            expression = user_input

        try:
            result = derivative(expression)

            return {
                "operation": "Derivative",
                "result": result
            }

        except Exception as e:
            return {
                "operation": "Derivative",
                "error": str(e)
            }

    # -------------------------
    # INTEGRAL
    # -------------------------

    elif (
            text.startswith("integral")
            or "integrate" in text
    ):

        if text.startswith("integral"):
            expression = user_input[8:].strip()
        else:
            expression = user_input

        try:
            result = integral(expression)

            return {
                "operation": "Integral",
                "result": result
            }

        except Exception as e:
            return {
                "operation": "Integral",
                "error": str(e)
            }

    # -------------------------
    # UNKNOWN OPERATION
    # -------------------------

    else:

        return {
            "error": "I could not understand the mathematical operation."
        }
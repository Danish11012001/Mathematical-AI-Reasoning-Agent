import sympy as sp


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
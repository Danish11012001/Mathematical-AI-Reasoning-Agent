import sympy as sp


def solve_equation(user_input):
    x = sp.symbols('x')

    # Equation with "="
    if "=" in user_input:
        left, right = user_input.split("=")

        left = sp.sympify(left)
        right = sp.sympify(right)

        equation = sp.Eq(left, right)

        return sp.solve(equation, x)

    # Expression such as x**2 - 5*x + 6
    else:
        expression = sp.sympify(user_input)

        return sp.solve(expression, x)
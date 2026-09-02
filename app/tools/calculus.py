import sympy as sp


def derivative(expression):
    x = sp.symbols('x')

    expression = sp.sympify(expression)

    return sp.diff(expression, x)


def integral(expression):
    x = sp.symbols('x')

    expression = sp.sympify(expression)

    return sp.integrate(expression, x)
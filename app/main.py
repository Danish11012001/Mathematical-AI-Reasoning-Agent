import sympy as sp

x = sp.symbols('x')

equation = input("Enter an equation: ")

expression = sp.sympify(equation)

solution = sp.solve(expression, x)

print("Equation:", expression)
print("Solution:", solution)
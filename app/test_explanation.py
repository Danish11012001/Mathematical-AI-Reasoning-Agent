from explanation.explainer import (
    explain_linear_equation,
    explain_quadratic_equation,
    explain_derivative,
    explain_integral
)


print("=== Mathematical Explanation Test ===")


print("\n--- Linear Equation ---")

steps = explain_linear_equation("2*x - 4 = 0")

for i, step in enumerate(steps, 1):
    print(f"Step {i}: {step}")


print("\n--- Quadratic Equation ---")

steps = explain_quadratic_equation(
    "x**2 - 5*x + 6 = 0"
)

for i, step in enumerate(steps, 1):
    print(f"Step {i}: {step}")


print("\n--- Derivative ---")

steps = explain_derivative("x**3 + 2*x")

for i, step in enumerate(steps, 1):
    print(f"Step {i}: {step}")


print("\n--- Integral ---")

steps = explain_integral("x**2 + 2*x")

for i, step in enumerate(steps, 1):
    print(f"Step {i}: {step}")
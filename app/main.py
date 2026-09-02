from tools.equations import solve_equation
from tools.calculus import derivative, integral
from tools.matrices import matrix_determinant, matrix_inverse
from verification.verifier import verify_equation


def get_matrix():
    """Get a matrix from the user with proper dimension validation."""

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
                    try:
                        values = input(
                            f"Enter row {i + 1} ({cols} values separated by spaces): "
                        ).split()

                        if len(values) != cols:
                            print(f"Please enter exactly {cols} values.")
                            continue

                        row = [float(value) for value in values]
                        matrix.append(row)
                        break

                    except ValueError:
                        print("Please enter valid numbers.")

            return matrix

        except ValueError:
            print("Please enter valid integer values for rows and columns.")


def main():

    print("\n=== Mathematical AI Agent ===")

    print("\nAvailable Operations:")
    print("1. Solve Equation")
    print("2. Derivative")
    print("3. Integral")
    print("4. Matrix Determinant")
    print("5. Matrix Inverse")
    print("6. Exit")

    while True:

        choice = input("\nChoose an operation: ")

        # --------------------------------
        # Solve Equation
        # --------------------------------

        if choice == "1":

            equation = input("Enter equation: ")

            try:
                result = solve_equation(equation)

                print("\nSolution:", result)

                verified = verify_equation(equation, result)

                if verified:
                    print("Verification: PASSED")
                else:
                    print("Verification: FAILED")

            except Exception as e:
                print("Error:", e)

        # --------------------------------
        # Derivative
        # --------------------------------

        elif choice == "2":

            expression = input("Enter expression: ")

            try:
                result = derivative(expression)

                print("\nDerivative:", result)

            except Exception as e:
                print("Error:", e)

        # --------------------------------
        # Integral
        # --------------------------------

        elif choice == "3":

            expression = input("Enter expression: ")

            try:
                result = integral(expression)

                print("\nIntegral:", result)

            except Exception as e:
                print("Error:", e)

        # --------------------------------
        # Matrix Determinant
        # --------------------------------

        elif choice == "4":

            try:
                matrix = get_matrix()

                result = matrix_determinant(matrix)

                print("\nMatrix:")
                for row in matrix:
                    print(row)

                print("Determinant:", result)

            except Exception as e:
                print("Error:", e)

        # --------------------------------
        # Matrix Inverse
        # --------------------------------

        elif choice == "5":

            try:
                matrix = get_matrix()

                if len(matrix) != len(matrix[0]):
                    print("\nError: Matrix inverse requires a square matrix.")
                    continue

                result = matrix_inverse(matrix)

                print("\nMatrix:")
                for row in matrix:
                    print(row)

                print("\nInverse:")
                print(result)

            except Exception as e:
                print("Error:", e)

        # --------------------------------
        # Exit
        # --------------------------------

        elif choice == "6":

            print("\nThank you for using Mathematical AI Agent!")
            break

        # --------------------------------
        # Invalid Choice
        # --------------------------------

        else:

            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    main()
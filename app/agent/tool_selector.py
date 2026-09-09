def select_tool(plan):
    """
    Select the mathematical tool based on
    the plan created by the planner.
    """

    category = plan["category"]
    operation = plan["operation"]

    tools = {

        # Equations
        ("equation", "solve"):
            "solve_equation",

        # Calculus
        ("calculus", "derivative"):
            "derivative",

        ("calculus", "integral"):
            "integral",

        # Matrices
        ("matrix", "determinant"):
            "matrix_determinant",

        ("matrix", "inverse"):
            "matrix_inverse",

        ("matrix", "transpose"):
            "matrix_transpose",

        ("matrix", "rank"):
            "matrix_rank",

        ("matrix", "eigenvalues"):
            "matrix_eigenvalues",

        ("matrix", "multiply"):
            "matrix_multiply"
    }

    return tools.get(
        (category, operation)
    )
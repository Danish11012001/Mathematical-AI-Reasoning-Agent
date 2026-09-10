def select_tool(plan):

    category = plan["category"]

    operation = plan["operation"]

    tools = {

        ("equation", "solve"):
            "solve_equation",

        ("calculus", "derivative"):
            "derivative",

        ("calculus", "integral"):
            "integral",

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
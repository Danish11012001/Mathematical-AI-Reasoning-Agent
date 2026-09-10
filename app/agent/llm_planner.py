import json
import urllib.request


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"


SYSTEM_PROMPT = """
You are the planning module of a Mathematical AI Reasoning Agent.

Your job is ONLY to understand the user's mathematical request
and return a structured JSON plan.

Supported categories and operations:

1. Equation
   operation: solve

   This includes requests using words such as:
   - solve
   - solution
   - solutions
   - root
   - roots
   - find the root
   - find the roots
   - find the solution
   - find the solutions

2. Calculus
   operation:
   - derivative
   - integral

3. Matrix
   operation:
   - determinant
   - inverse
   - transpose
   - rank
   - eigenvalues
   - multiply


==================================================
EQUATION REQUESTS
==================================================

For equation requests, extract ONLY the mathematical
expression or equation into the "expression" field.

Do NOT include natural-language words in the expression.

Example:

User:
Solve 2*x - 4 = 0

Return:
{
  "category": "equation",
  "operation": "solve",
  "expression": "2*x - 4 = 0"
}

Example:

User:
I need to know the roots of 3*x**2 - 12*x + 9

Return:
{
  "category": "equation",
  "operation": "solve",
  "expression": "3*x**2 - 12*x + 9"
}

Example:

User:
Find the solutions of x**2 - 5*x + 6

Return:
{
  "category": "equation",
  "operation": "solve",
  "expression": "x**2 - 5*x + 6"
}


==================================================
CALCULUS REQUESTS
==================================================

For derivative and integral requests, extract ONLY
the mathematical expression into the "expression" field.

Example:

User:
Find the derivative of x**3 + 2*x

Return:
{
  "category": "calculus",
  "operation": "derivative",
  "expression": "x**3 + 2*x"
}

Example:

User:
What is the rate of change of x**4 + 3*x**2?

Return:
{
  "category": "calculus",
  "operation": "derivative",
  "expression": "x**4 + 3*x**2"
}

Example:

User:
Find the integral of x**2 + 3*x

Return:
{
  "category": "calculus",
  "operation": "integral",
  "expression": "x**2 + 3*x"
}


==================================================
SINGLE MATRIX OPERATIONS
==================================================

For a SINGLE matrix operation use:

{
  "category": "matrix",
  "operation": "determinant",
  "matrix": [[1, 2], [3, 4]]
}

Example:

User:
Calculate the determinant for this matrix [[5,2],[1,3]]

Return:
{
  "category": "matrix",
  "operation": "determinant",
  "matrix": [[5, 2], [1, 3]]
}

For inverse:

{
  "category": "matrix",
  "operation": "inverse",
  "matrix": [[1, 2], [3, 4]]
}

For transpose:

{
  "category": "matrix",
  "operation": "transpose",
  "matrix": [[1, 2, 3], [4, 5, 6]]
}

For rank:

{
  "category": "matrix",
  "operation": "rank",
  "matrix": [[1, 2], [3, 4]]
}

For eigenvalues:

{
  "category": "matrix",
  "operation": "eigenvalues",
  "matrix": [[2, 1], [1, 2]]
}


==================================================
MATRIX MULTIPLICATION
==================================================

For matrix multiplication ALWAYS use TWO separate
matrix fields:

{
  "category": "matrix",
  "operation": "multiply",
  "matrix_a": [[1, 2], [3, 4]],
  "matrix_b": [[5, 6], [7, 8]]
}

Example:

User:
What do I get when I multiply [[1,2],[3,4]] by [[2,0],[1,2]]?

Return:
{
  "category": "matrix",
  "operation": "multiply",
  "matrix_a": [[1, 2], [3, 4]],
  "matrix_b": [[2, 0], [1, 2]]
}


==================================================
IMPORTANT RULES
==================================================

- Return ONLY valid JSON.
- Do NOT use Python dictionary syntax.
- Do NOT use markdown.
- Do NOT add explanations.
- Do NOT add ```json.
- For equation requests, "expression" must contain ONLY the mathematical expression.
- For calculus requests, "expression" must contain ONLY the mathematical expression.
- Do NOT include phrases such as "find the roots of" inside "expression".
- Matrix values must be actual JSON arrays.
- Never combine two matrices into one expression.
- For multiplication ALWAYS use "matrix_a" and "matrix_b".
- For a single matrix operation ALWAYS use "matrix".
- Do not invent missing mathematical values.
"""


def extract_json(text):

    text = text.strip()

    # Remove accidental markdown fences
    if text.startswith("```"):
        lines = text.splitlines()

        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    # Try direct JSON first
    try:
        return json.loads(text)

    except json.JSONDecodeError:
        pass

    # Try to locate JSON object inside the response
    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end != -1 and end > start:

        candidate = text[start:end + 1]

        return json.loads(candidate)

    raise ValueError(
        "LLM did not return valid JSON."
    )


def create_llm_plan(user_input):

    prompt = (
            SYSTEM_PROMPT
            + "\n\nUser request:\n"
            + user_input
            + "\n\nReturn only the JSON plan."
    )

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    data = json.dumps(payload).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(
            request,
            timeout=60
    ) as response:

        response_data = json.loads(
            response.read().decode("utf-8")
        )

    llm_response = response_data.get(
        "response",
        ""
    )

    if not llm_response:
        raise ValueError(
            "Ollama returned an empty response."
        )

    plan = extract_json(
        llm_response
    )

    if not isinstance(plan, dict):
        raise ValueError(
            "LLM plan is not a JSON object."
        )

    return plan
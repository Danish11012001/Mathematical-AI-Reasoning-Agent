from agent.agent import run_agent


print("=== Mathematical AI Agent ===")

user_input = input("\nEnter your mathematical request: ")

result = run_agent(user_input)

print("\n================================")
print("           AGENT RESULT")
print("================================")

if "error" in result:

    print("Error:", result["error"])

else:

    print("\nOperation:")
    print(result["operation"])

    if "matrix" in result:

        print("\nMatrix:")

        for row in result["matrix"]:
            print(row)

    if "steps" in result:

        print("\nStep-by-Step Explanation:")

        for i, step in enumerate(result["steps"], 1):
            print(f"Step {i}: {step}")

    if "result" in result:

        print("\nFinal Result:")
        print(result["result"])

    if "verification" in result:

        print("\nVerification:")

        if result["verification"]:
            print("PASSED")
        else:
            print("FAILED")

print("\n================================")
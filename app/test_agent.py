from agent.agent import run_agent


print("=== Mathematical AI Agent ===")

user_input = input("Enter your mathematical request: ")

result = run_agent(user_input)

print("\nAgent Result:")

if "error" in result:
    print("Error:", result["error"])

else:
    print("Operation:", result["operation"])
    print("Result:", result["result"])

    if "verification" in result:
        if result["verification"]:
            print("Verification: PASSED")
        else:
            print("Verification: FAILED")
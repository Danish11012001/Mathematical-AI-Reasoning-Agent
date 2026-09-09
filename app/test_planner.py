from agent.planner import create_plan
from agent.tool_selector import select_tool


print("=== Planner & Tool Selector Test ===")

user_input = input(
    "\nEnter a mathematical request: "
)

plan = create_plan(user_input)

print("\nPlan:")
print(plan)

tool = select_tool(plan)

print("\nSelected Tool:")
print(tool)
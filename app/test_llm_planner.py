from agent.llm_planner import create_llm_plan


print("=== LLM Planner Test ===")

user_input = input("\nEnter your mathematical request: ")

plan = create_llm_plan(user_input)

print("\nLLM PLAN:")
print(plan)
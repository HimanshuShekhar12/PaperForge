from app.agents.llm import llm

response = llm.invoke(
    "Write a Python program that prints Hello PaperForge."
)

print("RESPONSE:")
print(response.content)
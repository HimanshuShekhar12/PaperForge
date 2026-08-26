from app.agents.llm import llm


def plan_implementation(state):
    analysis = state["analysis"]

    prompt = f"""
You are a senior machine learning engineer writing an implementation
plan for a PyTorch developer to follow.

PAPER ANALYSIS:
{analysis}

Create a clear, structured implementation plan that:
1. Lists the classes/modules to build (e.g. model components, layers).
2. Describes what each class/module does and its inputs/outputs.
3. Describes the overall forward pass / data flow through the model.
4. Notes any important implementation details from the analysis
   (masking, normalization, initialization, etc.).
5. Suggests a minimal test or demo to confirm the implementation runs.

Do not write code. Return only the structured plan as plain text.
"""

    try:
        response = llm.invoke(prompt)
        plan = response.content
    except Exception as e:
        plan = f"LLM call failed during planning: {str(e)}"

    return {
        "plan": plan
    }
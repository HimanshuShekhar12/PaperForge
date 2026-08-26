from dotenv import load_dotenv

load_dotenv()

from app.agents.llm import llm


def critique_code(state):

    prompt = f"""
You are an expert code reviewer.

Review the generated PyTorch implementation using the execution result.

IMPLEMENTATION PLAN:
{state["plan"]}

GENERATED CODE:
{state["generated_code"]}

EXECUTION RESULT:
{state["execution_result"]}

Identify:
1. Why the implementation failed.
2. The exact issue that must be fixed.
3. What changes are required to make it runnable.

Do not rewrite the entire code.
Return only concise, actionable feedback for the coder.
"""

    try:
        response = llm.invoke(prompt)
        critique = response.content
    except Exception as e:
        critique = f"LLM call failed during critique: {str(e)}"

    return {
        "critique": critique,
        "retry_count": state["retry_count"] + 1
    }
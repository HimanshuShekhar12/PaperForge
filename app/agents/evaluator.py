from dotenv import load_dotenv

load_dotenv()

from app.agents.llm import llm


def evaluate_code(state):

    prompt = f"""
You are a senior machine learning engineer performing a final
quality evaluation of an automatically generated PyTorch implementation.

IMPLEMENTATION PLAN:
{state["plan"]}

GENERATED CODE:
{state["generated_code"]}

EXECUTION RESULT:
{state["execution_result"]}

CRITIQUE:
{state["critique"]}

Evaluate the implementation on:

1. Execution correctness
2. Completeness
3. Alignment with the implementation plan
4. PyTorch implementation quality
5. Missing or incorrect components

Important:
- The code may execute successfully but still be incomplete or incorrect.
- Do not consider RETURN CODE 0 alone as a PASS.
- Check whether the requested implementation is actually complete.
- Look for truncated classes, functions, missing return statements,
  missing components, and logical implementation errors.

At the end, provide:

VERDICT: PASS

or

VERDICT: FAIL

Then provide a concise explanation.
"""

    try:
        response = llm.invoke(prompt)
        evaluation = response.content
    except Exception as e:
        evaluation = f"LLM call failed during evaluation: {str(e)}"
        return {
            "evaluation": evaluation,
            "status": "failed"
        }

    if "VERDICT: PASS" in evaluation:
        status = "passed"
    else:
        status = "failed"

    return {
        "evaluation": evaluation,
        "status": status
    }
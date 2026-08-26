from app.agents.llm import llm


def generate_code(state):

    prompt = f"""
You are an expert software and machine learning engineer.

Your task is to implement the research paper described by the
implementation plan below.

IMPLEMENTATION PLAN:
{state["plan"]}

PREVIOUS GENERATED CODE:
{state["generated_code"]}

PREVIOUS CRITIQUE:
{state["critique"]}

Requirements:

- Return ONLY Python code.
- Do NOT explain the code.
- Do NOT use markdown code fences.
- Return the COMPLETE implementation.
- The implementation must be self-contained and runnable.
- Include all required imports.
- Follow the implementation plan exactly.
- Do not assume components that are not present in the plan.
- Do not hardcode assumptions specific to a particular paper.
- If previous code exists, preserve working parts and fix the
  problems identified by the critique.
- Never truncate the implementation.
- Never stop in the middle of a class, function, loop, or statement.
- Include a small runnable demo/test when appropriate.

Before returning the code, verify that:
- all classes are complete
- all functions are complete
- all brackets and parentheses are closed
- there are no incomplete statements
- there are no undefined variables
- the implementation can run as a standalone Python file

Return the complete Python file.
"""

    try:
        response = llm.invoke(prompt)
        code = response.content
    except Exception as e:
        # No code produced — executor.py already handles empty code
        # gracefully ("No code was generated."), so returning "" here
        # keeps the pipeline alive instead of crashing main.py.
        print(f"[coder] LLM call failed: {e}")
        return {"generated_code": ""}

    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        code = "\n".join(lines)

    return {
        "generated_code": code
    }
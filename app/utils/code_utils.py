def extract_python_code(response: str) -> str:
    """
    Extract Python code from an LLM response.
    """

    response = response.strip()

    if "```python" in response:
        code = response.split("```python", 1)[1]
        code = code.split("```", 1)[0]
        return code.strip()

    if "```" in response:
        code = response.split("```", 1)[1]
        code = code.split("```", 1)[0]
        return code.strip()

    return response
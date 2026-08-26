from app.agents.llm import llm


def analyze_paper(state):
    paper = state["paper_text"]

    prompt = f"""
You are an expert AI research engineer analyzing a research paper
so that it can be implemented in PyTorch.

PAPER:
{paper}

Extract and summarize, in plain text:
1. The core architecture or method proposed.
2. The key components (layers, modules, algorithms) needed to
   implement it.
3. Important equations or formulas, described in words rather than
   notation.
4. Any hyperparameters, dimensions, or configuration details
   mentioned or implied.
5. The expected inputs and outputs of the model.

Be concise but complete. Do not write any code here — only the
analysis.
"""

    try:
        response = llm.invoke(prompt)
        analysis = response.content
    except Exception as e:
        analysis = f"LLM call failed during analysis: {str(e)}"

    return {
        "analysis": analysis
    }
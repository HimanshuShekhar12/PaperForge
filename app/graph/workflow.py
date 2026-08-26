from langgraph.graph import StateGraph, START, END

from app.agents.coder import generate_code
from app.agents.executor import execute_code
from app.agents.planner import plan_implementation
from app.graph.state import AgentState
from app.agents.analyzer import analyze_paper
from app.agents.critic import critique_code
from app.agents.evaluator import evaluate_code


MAX_RETRIES = 3


def should_evaluate(state):

    # If execution failed, first get feedback from critic —
    # but only if we still have retries left.
    if "RETURN CODE: 0" not in state["execution_result"]:
        if state["retry_count"] >= MAX_RETRIES:
            return "end"
        return "critic"

    # If execution succeeded, evaluate the implementation
    return "evaluator"


def after_evaluation(state):

    # Implementation is good
    if state["status"] == "passed":
        return "end"

    # Give coder another chance
    if state["retry_count"] < MAX_RETRIES:
        return "coder"

    # Maximum retries reached
    return "end"


graph_builder = StateGraph(AgentState)

graph_builder.add_node("analyzer", analyze_paper)
graph_builder.add_node("planner", plan_implementation)
graph_builder.add_node("coder", generate_code)
graph_builder.add_node("executor", execute_code)
graph_builder.add_node("critic", critique_code)
graph_builder.add_node("evaluator", evaluate_code)


graph_builder.add_edge(START, "analyzer")
graph_builder.add_edge("analyzer", "planner")
graph_builder.add_edge("planner", "coder")
graph_builder.add_edge("coder", "executor")


graph_builder.add_conditional_edges(
    "executor",
    should_evaluate,
    {
        "critic": "critic",
        "evaluator": "evaluator",
        "end": END
    }
)


graph_builder.add_edge("critic", "coder")


graph_builder.add_conditional_edges(
    "evaluator",
    after_evaluation,
    {
        "coder": "coder",
        "end": END
    }
)

graph = graph_builder.compile()
"""
Smoke tests: verify the app imports cleanly and the LangGraph pipeline
compiles correctly. Deliberately does NOT call the LLM (no API calls,
no OPENROUTER_API_KEY needed beyond a dummy placeholder) so this can
run in CI on every push without burning API quota.
"""


def test_workflow_graph_compiles():
    from app.graph.workflow import graph
    assert graph is not None


def test_state_schema_imports():
    from app.graph.state import AgentState
    assert AgentState is not None


def test_api_schemas_import():
    from app.schemas import PaperSubmitRequest, PaperSubmitResponse, JobStatusResponse
    assert PaperSubmitRequest is not None
    assert PaperSubmitResponse is not None
    assert JobStatusResponse is not None


def test_fastapi_app_imports():
    from api import app
    assert app is not None
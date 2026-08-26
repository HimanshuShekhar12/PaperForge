from typing import TypedDict, NotRequired

class AgentState(TypedDict):
    paper_text: str
    analysis: NotRequired[str]
    plan: NotRequired[str]
    generated_code: NotRequired[str]
    execution_result: NotRequired[str]
    critique: NotRequired[str]
    retry_count: NotRequired[int]
    evaluation: NotRequired[str]
    status: NotRequired[str]
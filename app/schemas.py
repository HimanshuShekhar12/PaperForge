from pydantic import BaseModel
from typing import Optional


class PaperSubmitRequest(BaseModel):
    paper_text: str


class PaperSubmitResponse(BaseModel):
    job_id: str


class JobStatusResponse(BaseModel):
    job_id: str
    job_status: str  # "pending", "running", "completed", "failed"
    pipeline_status: Optional[str] = None  # the graph's own "passed"/"failed" verdict
    analysis: Optional[str] = None
    plan: Optional[str] = None
    generated_code: Optional[str] = None
    execution_result: Optional[str] = None
    critique: Optional[str] = None
    retry_count: Optional[int] = None
    evaluation: Optional[str] = None
    error: Optional[str] = None
import uuid

from fastapi import FastAPI, BackgroundTasks, HTTPException

from app.graph.workflow import graph
from app.schemas import PaperSubmitRequest, PaperSubmitResponse, JobStatusResponse

app = FastAPI(title="PaperForge API")

# In-memory job store. Fine for a single-process demo; a real
# deployment would use a persistent store (DB/Redis) and a proper
# task queue (Celery/RQ) instead of FastAPI's BackgroundTasks, which
# just runs the job in the same process after the response is sent.
jobs = {}


def run_pipeline(job_id: str, paper_text: str):
    jobs[job_id]["job_status"] = "running"

    initial_state = {
        "paper_text": paper_text,
        "analysis": "",
        "plan": "",
        "generated_code": "",
        "execution_result": "",
        "critique": "",
        "retry_count": 0,
        "evaluation": "",
        "status": ""
    }

    try:
        result = graph.invoke(initial_state)

        # result also contains its own "status" field (the evaluator's
        # passed/failed verdict) -- pull it out under a different name
        # so it doesn't clobber the job's own lifecycle status below.
        pipeline_status = result.pop("status", None)

        jobs[job_id].update(result)
        jobs[job_id]["pipeline_status"] = pipeline_status
        jobs[job_id]["job_status"] = "completed"

    except Exception as e:
        jobs[job_id]["job_status"] = "failed"
        jobs[job_id]["error"] = str(e)


@app.get("/")
def health_check():
    return {"message": "PaperForge API is running"}


@app.post("/papers", response_model=PaperSubmitResponse)
def submit_paper(request: PaperSubmitRequest, background_tasks: BackgroundTasks):
    if not request.paper_text.strip():
        raise HTTPException(status_code=400, detail="paper_text cannot be empty")

    job_id = str(uuid.uuid4())
    jobs[job_id] = {"job_status": "pending"}

    background_tasks.add_task(run_pipeline, job_id, request.paper_text)

    return PaperSubmitResponse(job_id=job_id)


@app.get("/papers/{job_id}", response_model=JobStatusResponse)
def get_paper_status(job_id: str):
    job = jobs.get(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatusResponse(
        job_id=job_id,
        job_status=job.get("job_status", "unknown"),
        pipeline_status=job.get("pipeline_status"),
        analysis=job.get("analysis"),
        plan=job.get("plan"),
        generated_code=job.get("generated_code"),
        execution_result=job.get("execution_result"),
        critique=job.get("critique"),
        retry_count=job.get("retry_count"),
        evaluation=job.get("evaluation"),
        error=job.get("error"),
    )
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from server.env import FinDocQAEnv
from server.models import Observation, StepResult, EpisodeState

app = FastAPI(
    title="FinDocQA-Env",
    description="OpenEnv environment for financial document QA — extract facts, answer questions, identify conflicts.",
    version="1.0.0"
)

# Single global environment instance
env = FinDocQAEnv()


# ── Request Models ─────────────────────────────────────────────────────────────

class ResetRequest(BaseModel):
    task_type: Optional[str] = None
    doc_id: Optional[str] = None


class StepRequest(BaseModel):
    response: str


# ── Routes ─────────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "name": "FinDocQA-Env",
        "version": "1.0.0",
        "description": "OpenEnv environment for financial document comprehension",
        "tasks": ["extract-facts", "answer-questions", "identify-conflicts"],
        "endpoints": ["/reset", "/step", "/state", "/health"]
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/reset")
def reset(request: ResetRequest = ResetRequest()) -> dict:
    """
    Start a new episode.
    Optionally specify task_type and doc_id.
    Returns initial observation.
    """
    try:
        obs = env.reset(
            task_type=request.task_type,
            doc_id=request.doc_id
        )
        return {
            "observation": obs.model_dump(),
            "info": {
                "message": "Episode started successfully.",
                "available_tasks": ["extract-facts", "answer-questions", "identify-conflicts"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/step")
def step(request: StepRequest) -> dict:
    """
    Submit agent response and receive reward.
    Returns observation, reward, done, info.
    """
    if not request.response or not request.response.strip():
        raise HTTPException(status_code=400, detail="Response cannot be empty.")

    try:
        result = env.step(request.response)
        return {
            "observation": result.observation.model_dump(),
            "reward": result.reward,
            "done": result.done,
            "info": result.info
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/state")
def state() -> dict:
    """
    Return current episode state snapshot.
    """
    try:
        s = env.state()
        return s.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
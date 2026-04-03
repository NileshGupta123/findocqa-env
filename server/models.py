from pydantic import BaseModel, Field
from typing import Optional, Any


# ── Action ────────────────────────────────────────────────────────────────────
class Action(BaseModel):
    response: str = Field(
        ...,
        description="The agent's text response to the current task"
    )


# ── Observations ──────────────────────────────────────────────────────────────
class Observation(BaseModel):
    document: str = Field(
        ...,
        description="The financial document excerpt the agent must analyze"
    )
    task_type: str = Field(
        ...,
        description="One of: extract-facts | answer-questions | identify-conflicts"
    )
    instructions: str = Field(
        ...,
        description="Clear instructions telling the agent exactly what to do"
    )
    questions: Optional[list[str]] = Field(
        default=None,
        description="List of questions (used in answer-questions task)"
    )
    step: int = Field(
        default=1,
        description="Current step number in the episode"
    )


# ── Reward ────────────────────────────────────────────────────────────────────
class Reward(BaseModel):
    score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Normalized reward score between 0.0 and 1.0"
    )
    breakdown: dict[str, float] = Field(
        default_factory=dict,
        description="Per-field score breakdown for transparency"
    )
    feedback: str = Field(
        default="",
        description="Human-readable feedback on the agent's response"
    )


# ── Step Result ───────────────────────────────────────────────────────────────
class StepResult(BaseModel):
    observation: Observation
    reward: float = Field(ge=0.0, le=1.0)
    done: bool
    info: dict[str, Any] = Field(default_factory=dict)


# ── Episode State ─────────────────────────────────────────────────────────────
class EpisodeState(BaseModel):
    episode_id: str
    task_type: str
    document_id: str
    current_step: int
    max_steps: int
    total_reward: float
    done: bool
    history: list[dict[str, Any]] = Field(default_factory=list)
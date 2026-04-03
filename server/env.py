import uuid
import random
from typing import Optional

from server.models import Observation, StepResult, EpisodeState
from server.graders.grader import grade
from server.tasks.extract_facts import build_observation as build_extract_facts
from server.tasks.answer_questions import build_observation as build_answer_questions
from server.tasks.identify_conflicts import build_observation as build_identify_conflicts


TASK_TYPES = ["extract-facts", "answer-questions", "identify-conflicts"]
MAX_STEPS = 1  # single-step episodes — deterministic and clean


class FinDocQAEnv:
    """
    FinDocQA Environment — core state machine.

    Manages episode lifecycle:
        reset() → new episode, returns first observation
        step()  → grades agent response, returns result
        state() → returns current episode snapshot
    """

    def __init__(self):
        self._episode_id: Optional[str] = None
        self._task_type: Optional[str] = None
        self._doc_id: Optional[str] = None
        self._doc_data: Optional[dict] = None
        self._current_step: int = 0
        self._total_reward: float = 0.0
        self._done: bool = False
        self._history: list = []
        self._current_observation: Optional[dict] = None

    # ── Reset ──────────────────────────────────────────────────────────────────

    def reset(self, task_type: Optional[str] = None, doc_id: Optional[str] = None) -> Observation:
        """
        Start a new episode.
        Randomly picks task and document unless specified.
        """
        # New episode ID
        self._episode_id = str(uuid.uuid4())[:8]

        # Pick task
        if task_type and task_type in TASK_TYPES:
            self._task_type = task_type
        else:
            self._task_type = random.choice(TASK_TYPES)

        # Build observation based on task
        if self._task_type == "extract-facts":
            obs_data = build_extract_facts(doc_id)
        elif self._task_type == "answer-questions":
            obs_data = build_answer_questions(doc_id)
        else:
            obs_data = build_identify_conflicts(doc_id)

        # Store episode state
        self._doc_id = obs_data["doc_id"]
        self._doc_data = obs_data["doc_data"]
        self._current_step = 0
        self._total_reward = 0.0
        self._done = False
        self._history = []
        self._current_observation = obs_data

        return Observation(
            document=obs_data["document"],
            task_type=obs_data["task_type"],
            instructions=obs_data["instructions"],
            questions=obs_data.get("questions"),
            step=0
        )

    # ── Step ───────────────────────────────────────────────────────────────────

    def step(self, response: str) -> StepResult:
        """
        Process agent response and return graded result.
        """
        if self._done:
            raise ValueError("Episode is done. Call reset() to start a new episode.")

        if self._current_observation is None:
            raise ValueError("No active episode. Call reset() first.")

        self._current_step += 1

        # Grade the response
        result = grade(
            task_type=self._task_type,
            response=response,
            document=self._doc_data
        )

        reward = result["score"]
        self._total_reward += reward
        self._done = True  # single-step episode ends here

        # Log to history
        self._history.append({
            "step": self._current_step,
            "response_preview": response[:100],
            "reward": reward,
            "breakdown": result["breakdown"],
            "feedback": result["feedback"]
        })

        # Build next observation (empty — episode done)
        next_obs = Observation(
            document=self._current_observation["document"],
            task_type=self._task_type,
            instructions="Episode complete.",
            questions=None,
            step=self._current_step
        )

        return StepResult(
            observation=next_obs,
            reward=reward,
            done=True,
            info={
                "episode_id": self._episode_id,
                "task_type": self._task_type,
                "doc_id": self._doc_id,
                "breakdown": result["breakdown"],
                "feedback": result["feedback"],
                "total_reward": self._total_reward
            }
        )

    # ── State ──────────────────────────────────────────────────────────────────

    def state(self) -> EpisodeState:
        """
        Return current episode state snapshot.
        """
        if self._episode_id is None:
            raise ValueError("No active episode. Call reset() first.")

        return EpisodeState(
            episode_id=self._episode_id,
            task_type=self._task_type or "unknown",
            document_id=self._doc_id or "unknown",
            current_step=self._current_step,
            max_steps=MAX_STEPS,
            total_reward=self._total_reward,
            done=self._done,
            history=self._history
        )
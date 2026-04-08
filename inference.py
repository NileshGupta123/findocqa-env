"""
Inference Script — FinDocQA-Env
================================
Baseline agent that runs against all 3 tasks using the OpenAI client.
Emits structured stdout logs in [START], [STEP], [END] format.

Required environment variables:
    API_BASE_URL   The API endpoint for the LLM
    MODEL_NAME     The model identifier
    API_KEY        Your API key (injected by validator)
"""

import os
import sys
import json
import textwrap
import urllib.request
import urllib.error
from typing import Optional
from openai import OpenAI

# Only load .env locally — never override injected environment variables
if not os.environ.get("API_KEY"):
    try:
        from dotenv import load_dotenv
        load_dotenv(override=False)
    except ImportError:
        pass

# ── Config ────────────────────────────────────────────────────────────────────
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.groq.com/openai/v1")
MODEL_NAME   = os.environ.get("MODEL_NAME", "llama-3.1-8b-instant")
API_KEY      = os.environ.get("API_KEY") or os.environ.get("HF_TOKEN")
ENV_BASE_URL = os.environ.get("ENV_BASE_URL", "https://nile-2026-findocqa-env.hf.space")
BENCHMARK    = "findocqa-env"
MAX_STEPS    = 1

TASKS = ["extract-facts", "answer-questions", "identify-conflicts"]

# ── Logging ───────────────────────────────────────────────────────────────────

def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: Optional[str]) -> None:
    clean_action = action.replace("\n", " ").replace("\r", " ")[:80]
    error_val = error if error else "null"
    done_val = str(done).lower()
    print(
        f"[STEP] step={step} action={clean_action!r} reward={reward:.2f} done={done_val} error={error_val}",
        flush=True
    )


def log_end(success: bool, steps: int, score: float, rewards: list) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True
    )


# ── Environment Client ────────────────────────────────────────────────────────

def env_request(endpoint: str, data: dict = {}) -> dict:
    """Make a POST request to the environment server."""
    url = f"{ENV_BASE_URL}{endpoint}"
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


# ── System Prompts ────────────────────────────────────────────────────────────

SYSTEM_PROMPTS = {
    "extract-facts": textwrap.dedent("""
        You are a precise financial analyst.
        Your job is to extract exact facts from financial documents.
        Always include exact numbers, percentages, company names, and dates.
        Be specific and concise. Do not add commentary or opinions.
        Just extract the facts clearly and completely.
    """).strip(),

    "answer-questions": textwrap.dedent("""
        You are a precise financial analyst.
        Your job is to answer questions about financial documents accurately.
        Always reference exact figures from the document.
        Format your answers as:
        Answer 1: [your answer]
        Answer 2: [your answer]
        Answer 3: [your answer]
        Answer 4: [your answer]
        Be specific. Include exact numbers and names from the document.
    """).strip(),

    "identify-conflicts": textwrap.dedent("""
        You are a senior financial analyst specializing in audit and compliance.
        Your job is to find ALL contradictions between sections of financial reports.
        For each conflict you find, state:
        - Topic: [what the conflict is about]
        - Section A claims: [exact claim from Section A]
        - Section B claims: [exact claim from Section B]
        - Investor impact: [why this matters]
        Be thorough. Find every single contradiction. Missing conflicts loses points.
    """).strip()
}


# ── LLM Agent ─────────────────────────────────────────────────────────────────

def get_agent_response(
    client: OpenAI,
    task_type: str,
    document: str,
    instructions: str,
    questions: Optional[list]
) -> str:
    """Call the LLM with document + task instructions."""
    system_prompt = SYSTEM_PROMPTS.get(task_type, SYSTEM_PROMPTS["extract-facts"])

    user_parts = [
        f"DOCUMENT:\n{document}",
        f"\nTASK INSTRUCTIONS:\n{instructions}"
    ]
    if questions:
        numbered = "\n".join(f"{i+1}. {q}" for i, q in enumerate(questions))
        user_parts.append(f"\nQUESTIONS TO ANSWER:\n{numbered}")

    user_message = "\n".join(user_parts)

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": user_message}
            ],
            temperature=0.1,
            max_tokens=512,
            stream=False
        )
        return (completion.choices[0].message.content or "").strip()
    except Exception as e:
        print(f"[DEBUG] LLM call failed: {e}", flush=True)
        return "Unable to generate response."


# ── Run One Task ──────────────────────────────────────────────────────────────

def run_task(client: OpenAI, task_type: str) -> dict:
    """Run a single task episode and return results."""
    rewards = []
    steps_taken = 0
    success = False
    score = 0.0

    log_start(task=task_type, env=BENCHMARK, model=MODEL_NAME)

    try:
        reset_resp = env_request("/reset", {"task_type": task_type})
        obs = reset_resp["observation"]

        document     = obs["document"]
        instructions = obs["instructions"]
        questions    = obs.get("questions")
        done         = False

        for step in range(1, MAX_STEPS + 1):
            if done:
                break

            action = get_agent_response(
                client=client,
                task_type=task_type,
                document=document,
                instructions=instructions,
                questions=questions
            )

            step_resp = env_request("/step", {"response": action})

            reward = step_resp["reward"]
            done   = step_resp["done"]

            rewards.append(reward)
            steps_taken = step

            log_step(
                step=step,
                action=action,
                reward=reward,
                done=done,
                error=None
            )

            if done:
                break

        score = sum(rewards) / len(rewards) if rewards else 0.0
        score = round(min(max(score, 0.0), 1.0), 3)
        success = score >= 0.1

    except Exception as e:
        print(f"[DEBUG] Task {task_type} failed: {e}", flush=True)
        if not rewards:
            rewards = [0.0]
            steps_taken = 1

    finally:
        log_end(
            success=success,
            steps=steps_taken,
            score=score,
            rewards=rewards
        )

    return {
        "task": task_type,
        "score": score,
        "success": success,
        "rewards": rewards
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not API_KEY:
        print("[ERROR] API_KEY not set in environment.", flush=True)
        sys.exit(1)

    print(f"[DEBUG] API_BASE_URL={API_BASE_URL}", flush=True)
    print(f"[DEBUG] MODEL_NAME={MODEL_NAME}", flush=True)
    print(f"[DEBUG] ENV_BASE_URL={ENV_BASE_URL}", flush=True)

    client = OpenAI(
        base_url=API_BASE_URL,
        api_key=API_KEY
    )

    print(f"\n{'='*60}", flush=True)
    print(f"FinDocQA-Env Baseline Inference", flush=True)
    print(f"Model : {MODEL_NAME}", flush=True)
    print(f"Server: {ENV_BASE_URL}", flush=True)
    print(f"{'='*60}\n", flush=True)

    all_results = []

    for task_type in TASKS:
        print(f"\n--- Running task: {task_type} ---", flush=True)
        result = run_task(client, task_type)
        all_results.append(result)
        print(f"--- Score: {result['score']:.3f} ---\n", flush=True)

    print(f"\n{'='*60}", flush=True)
    print("FINAL RESULTS", flush=True)
    print(f"{'='*60}", flush=True)
    for r in all_results:
        status = "✓" if r["success"] else "✗"
        print(f"  {status} {r['task']:<25} score={r['score']:.3f}", flush=True)

    avg = sum(r["score"] for r in all_results) / len(all_results)
    print(f"\n  Average score: {avg:.3f}", flush=True)
    print(f"{'='*60}\n", flush=True)


if __name__ == "__main__":
    main()
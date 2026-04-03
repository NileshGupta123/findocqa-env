from rapidfuzz import fuzz
from typing import Optional


# ── Helpers ───────────────────────────────────────────────────────────────────

def normalize(text: str) -> str:
    """Lowercase, strip punctuation, extra spaces."""
    import re
    text = text.lower().strip()
    text = re.sub(r"[^\w\s\.\%\$]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def token_f1(prediction: str, reference: str) -> float:
    """
    Token-level F1 score — same method used in SQuAD evaluation.
    Measures overlap between predicted and reference answer tokens.
    """
    pred_tokens = normalize(prediction).split()
    ref_tokens = normalize(reference).split()

    if not pred_tokens or not ref_tokens:
        return 0.0

    # Count common tokens
    pred_set = {}
    for t in pred_tokens:
        pred_set[t] = pred_set.get(t, 0) + 1

    ref_set = {}
    for t in ref_tokens:
        ref_set[t] = ref_set.get(t, 0) + 1

    common = 0
    for token in pred_set:
        if token in ref_set:
            common += min(pred_set[token], ref_set[token])

    if common == 0:
        return 0.0

    precision = common / len(pred_tokens)
    recall = common / len(ref_tokens)
    f1 = 2 * precision * recall / (precision + recall)
    return round(f1, 4)


def fuzzy_match(prediction: str, reference: str) -> float:
    """
    Fuzzy string match using rapidfuzz.
    Returns 0.0 to 1.0 — handles typos and paraphrasing.
    """
    score = fuzz.partial_ratio(
        normalize(prediction),
        normalize(reference)
    )
    return round(score / 100.0, 4)


# ── Task 1: Extract Facts ─────────────────────────────────────────────────────

def grade_extract_facts(response: str, expected_facts: dict) -> dict:
    """
    Grade fact extraction task.

    Expected facts dict has 4 keys:
        revenue, company_name, date, yoy_change

    Each field scored independently via fuzzy match.
    Final score = mean of all field scores.
    """
    field_scores = {}
    response_lower = response.lower()

    for field, expected_value in expected_facts.items():
        # Try fuzzy match of expected value inside the response
        score = fuzzy_match(response_lower, expected_value.lower())

        # Boost if exact substring found
        if normalize(expected_value) in normalize(response_lower):
            score = min(1.0, score + 0.2)

        field_scores[field] = round(min(score, 1.0), 4)

    final_score = round(sum(field_scores.values()) / len(field_scores), 4)

    # Build feedback
    missing = [f for f, s in field_scores.items() if s < 0.4]
    feedback = ""
    if not missing:
        feedback = "All key facts identified correctly."
    else:
        feedback = f"Missing or incorrect fields: {', '.join(missing)}."

    return {
        "score": final_score,
        "breakdown": field_scores,
        "feedback": feedback
    }


# ── Task 2: Answer Questions ──────────────────────────────────────────────────

def grade_answer_questions(response: str, questions: list, answers: list) -> dict:
    """
    Grade Q&A task using token F1 score per question.

    Tries to extract each answer from the full response.
    Final score = mean F1 across all questions.
    """
    if not questions or not answers:
        return {"score": 0.0, "breakdown": {}, "feedback": "No reference answers available."}

    question_scores = {}

    for i, (question, reference) in enumerate(zip(questions, answers)):
        key = f"q{i+1}"

        # Token F1 between full response and reference answer
        f1 = token_f1(response, reference)

        # Also try fuzzy match as backup
        fuzzy = fuzzy_match(response, reference)

        # Take the better of the two
        best = max(f1, fuzzy * 0.8)  # slight penalty on fuzzy
        question_scores[key] = round(min(best, 1.0), 4)

    final_score = round(sum(question_scores.values()) / len(question_scores), 4)

    weak = [k for k, s in question_scores.items() if s < 0.3]
    feedback = ""
    if not weak:
        feedback = "All questions answered with good coverage."
    else:
        feedback = f"Weak answers for: {', '.join(weak)}. Include more specific details."

    return {
        "score": final_score,
        "breakdown": question_scores,
        "feedback": feedback
    }


# ── Task 3: Identify Conflicts ────────────────────────────────────────────────

def grade_identify_conflicts(response: str, conflicts: list) -> dict:
    """
    Grade conflict identification task.

    For each known conflict, checks:
      (a) Did agent mention the conflicting topic? (0.4 weight)
      (b) Did agent reference both sides of the conflict? (0.6 weight)

    Final score = mean across all conflicts.
    """
    if not conflicts:
        return {"score": 0.0, "breakdown": {}, "feedback": "No conflict reference data."}

    conflict_scores = {}
    response_lower = normalize(response)

    for i, conflict in enumerate(conflicts):
        key = f"conflict_{i+1}"

        topic_keywords = conflict["topic"].lower().split()
        side_a_keywords = normalize(conflict["section_a"]).split()
        side_b_keywords = normalize(conflict["section_b"]).split()

        # Score A: Did agent mention the topic? (keyword overlap)
        topic_hits = sum(1 for kw in topic_keywords if kw in response_lower)
        topic_score = min(topic_hits / max(len(topic_keywords), 1), 1.0)

        # Score B: Did agent reference section A values?
        a_hits = sum(1 for kw in side_a_keywords if kw in response_lower)
        a_score = min(a_hits / max(len(side_a_keywords), 1), 1.0)

        # Score C: Did agent reference section B values?
        b_hits = sum(1 for kw in side_b_keywords if kw in response_lower)
        b_score = min(b_hits / max(len(side_b_keywords), 1), 1.0)

        # Both sides must be referenced for full credit
        both_sides_score = (a_score + b_score) / 2.0

        # Weighted final
        conflict_score = round(
            (0.4 * topic_score) + (0.6 * both_sides_score), 4
        )
        conflict_scores[key] = conflict_score

    final_score = round(sum(conflict_scores.values()) / len(conflict_scores), 4)

    missed = [k for k, s in conflict_scores.items() if s < 0.3]
    feedback = ""
    if not missed:
        feedback = "All conflicts identified with good explanation."
    else:
        feedback = f"Missed or poorly explained conflicts: {', '.join(missed)}."

    return {
        "score": final_score,
        "breakdown": conflict_scores,
        "feedback": feedback
    }


# ── Master Grader ─────────────────────────────────────────────────────────────

def grade(task_type: str, response: str, document: dict) -> dict:
    """
    Master grading function. Routes to correct grader by task type.

    Returns:
        {
            "score": float,       # 0.0 - 1.0
            "breakdown": dict,    # per-field scores
            "feedback": str       # human readable
        }
    """
    if task_type == "extract-facts":
        facts = document.get("facts", {})
        return grade_extract_facts(response, facts)

    elif task_type == "answer-questions":
        questions = document.get("questions", [])
        answers = document.get("answers", [])
        return grade_answer_questions(response, questions, answers)

    elif task_type == "identify-conflicts":
        conflicts = document.get("conflicts", [])
        return grade_identify_conflicts(response, conflicts)

    else:
        return {
            "score": 0.0,
            "breakdown": {},
            "feedback": f"Unknown task type: {task_type}"
        }
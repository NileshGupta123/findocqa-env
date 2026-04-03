import random
from server.data.documents import get_answer_questions_docs, get_document


def build_observation(doc_id: str = None) -> dict:
    """
    Build observation for answer-questions task.
    Randomly picks a document if none specified.
    """
    doc_ids = get_answer_questions_docs()
    if doc_id is None:
        doc_id = random.choice(doc_ids)

    doc = get_document(doc_id)
    questions = doc.get("questions", [])

    numbered = "\n".join(
        f"{i+1}. {q}" for i, q in enumerate(questions)
    )

    instructions = (
        "You are a financial analyst assistant. "
        "Read the document below and answer all questions precisely.\n\n"
        f"Questions:\n{numbered}\n\n"
        "Answer each question in order. "
        "Include exact figures, names, and percentages from the document. "
        "Format: Answer 1: ... Answer 2: ... Answer 3: ... Answer 4: ..."
    )

    return {
        "document": doc["content"],
        "task_type": "answer-questions",
        "instructions": instructions,
        "questions": questions,
        "doc_id": doc_id,
        "doc_data": doc
    }
import random
from server.data.documents import get_conflict_docs, get_document


def build_observation(doc_id: str = None) -> dict:
    """
    Build observation for identify-conflicts task.
    Randomly picks a conflict document if none specified.
    """
    doc_ids = get_conflict_docs()
    if doc_id is None:
        doc_id = random.choice(doc_ids)

    doc = get_document(doc_id)

    instructions = (
        "You are a senior financial analyst reviewing an annual report for inconsistencies. "
        "The document below contains TWO sections written by different executives.\n\n"
        "Your job:\n"
        "1. Identify ALL contradictions or conflicts between Section A and Section B\n"
        "2. For each conflict, state:\n"
        "   - What the topic is\n"
        "   - What Section A claims\n"
        "   - What Section B claims\n"
        "   - Why this discrepancy matters to investors\n\n"
        "Be thorough. Missing a conflict is worse than explaining one in detail."
    )

    return {
        "document": doc["content"],
        "task_type": "identify-conflicts",
        "instructions": instructions,
        "questions": None,
        "doc_id": doc_id,
        "doc_data": doc
    }
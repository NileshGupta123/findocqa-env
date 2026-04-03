import random
from server.data.documents import get_extract_facts_docs, get_document


def build_observation(doc_id: str = None) -> dict:
    """
    Build observation for extract-facts task.
    Randomly picks a document if none specified.
    """
    doc_ids = get_extract_facts_docs()
    if doc_id is None:
        doc_id = random.choice(doc_ids)

    doc = get_document(doc_id)

    instructions = (
        "You are a financial analyst assistant. "
        "Read the document below carefully and extract exactly these 4 facts:\n"
        "1. Total revenue (with exact figure and units)\n"
        "2. Company name (full legal name)\n"
        "3. Reporting period (quarter or year)\n"
        "4. Year-over-year revenue change (percentage)\n\n"
        "Be specific. Include exact numbers and percentages from the document."
    )

    return {
        "document": doc["content"],
        "task_type": "extract-facts",
        "instructions": instructions,
        "questions": None,
        "doc_id": doc_id,
        "doc_data": doc
    }
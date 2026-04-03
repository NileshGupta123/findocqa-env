# Synthetic but realistic financial report excerpts
# Used across all 3 tasks — no copyright issues

DOCUMENTS = {
    "doc_001": {
        "id": "doc_001",
        "title": "TechCorp Q3 2024 Earnings Report",
        "content": """
TechCorp Inc. reported third-quarter 2024 revenue of $4.82 billion, representing a 
12.4% year-over-year increase compared to Q3 2023 revenue of $4.29 billion. 
Net income for the quarter reached $687 million, up from $541 million in the prior 
year period. The company's EBITDA margin expanded to 24.3%, driven by operational 
efficiencies in the cloud services division.

CEO Sarah Mitchell stated that the strong performance was primarily driven by 
enterprise software subscriptions, which grew 31% year-over-year to $1.94 billion. 
The hardware segment declined 8.2% to $890 million due to supply chain disruptions.

TechCorp ended the quarter with cash and equivalents of $3.1 billion and total debt 
of $1.8 billion, resulting in a net cash position of $1.3 billion. Free cash flow 
for Q3 2024 was $412 million, compared to $378 million in Q3 2023.

The company raised its full-year 2024 revenue guidance to $18.9 billion to $19.2 billion,
up from the prior guidance of $18.4 billion to $18.8 billion.
        """.strip(),
        "facts": {
            "revenue": "4.82 billion",
            "company_name": "TechCorp Inc.",
            "date": "Q3 2024",
            "yoy_change": "12.4%"
        },
        "questions": [
            "What was TechCorp's Q3 2024 revenue?",
            "Who is the CEO of TechCorp?",
            "What was the EBITDA margin in Q3 2024?",
            "What happened to the hardware segment?"
        ],
        "answers": [
            "TechCorp Q3 2024 revenue was 4.82 billion dollars",
            "The CEO of TechCorp is Sarah Mitchell",
            "The EBITDA margin was 24.3 percent",
            "The hardware segment declined 8.2 percent due to supply chain disruptions"
        ]
    },

    "doc_002": {
        "id": "doc_002",
        "title": "GlobalBank Annual Report 2023",
        "content": """
GlobalBank Corporation reported full-year 2023 net revenue of $28.4 billion, a 6.8% 
increase from $26.6 billion in 2022. Return on equity improved to 14.2% from 12.9% 
in the prior year. The bank's loan portfolio grew 9.3% to $312 billion.

Chief Financial Officer James Hartwell noted that net interest income rose 18.3% to 
$16.8 billion, benefiting from the higher interest rate environment. Non-interest 
expenses increased 4.1% to $18.9 billion, resulting in an efficiency ratio of 66.5%.

GlobalBank maintained a Common Equity Tier 1 (CET1) ratio of 13.8%, well above the 
regulatory minimum of 4.5%. The bank returned $4.2 billion to shareholders through 
dividends and share buybacks during 2023.

Looking ahead to 2024, management projects net revenue growth of 3% to 5%, with 
net interest income expected to decline 8% to 10% as interest rates normalize.
        """.strip(),
        "facts": {
            "revenue": "28.4 billion",
            "company_name": "GlobalBank Corporation",
            "date": "full-year 2023",
            "yoy_change": "6.8%"
        },
        "questions": [
            "What was GlobalBank's full-year 2023 net revenue?",
            "Who is the CFO of GlobalBank?",
            "What was the CET1 ratio?",
            "How much did GlobalBank return to shareholders?"
        ],
        "answers": [
            "GlobalBank full-year 2023 net revenue was 28.4 billion dollars",
            "The CFO of GlobalBank is James Hartwell",
            "The CET1 ratio was 13.8 percent",
            "GlobalBank returned 4.2 billion dollars to shareholders"
        ]
    },

    "doc_003": {
        "id": "doc_003",
        "title": "RetailMax Q2 2024 Earnings — Conflicting Guidance",
        "content": """
SECTION A — CEO Letter to Shareholders:
RetailMax delivered exceptional Q2 2024 results with total revenue of $7.3 billion,
exceeding analyst expectations. Same-store sales grew 5.8% year-over-year, driven 
by strong consumer demand across all product categories. Gross margin improved to 
38.2%, up 150 basis points from Q2 2023.

We are confident in our trajectory and are raising full-year 2024 revenue guidance 
to $29.5 billion, representing growth of approximately 8% over 2023. We expect 
gross margins to remain stable at 37% to 38% for the remainder of the year.

SECTION B — CFO Financial Commentary:
Q2 2024 revenue came in at $7.3 billion, in line with our internal targets.
However, same-store sales growth of 5.8% was driven almost entirely by a one-time 
promotional event in April, and underlying demand trends remain soft. Inventory 
levels are elevated at $4.1 billion, up 23% year-over-year.

Given the one-time nature of Q2 outperformance and softening consumer trends, 
we are maintaining full-year 2024 revenue guidance at $27.8 billion. We anticipate 
gross margin pressure in H2 2024, with margins likely declining to 35% to 36% 
due to promotional activity needed to clear excess inventory.
        """.strip(),
        "conflicts": [
            {
                "topic": "full-year revenue guidance",
                "section_a": "raising guidance to $29.5 billion",
                "section_b": "maintaining guidance at $27.8 billion",
                "significance": "1.7 billion dollar discrepancy in revenue guidance"
            },
            {
                "topic": "gross margin outlook",
                "section_a": "stable at 37% to 38%",
                "section_b": "declining to 35% to 36%",
                "significance": "contradictory margin guidance between CEO and CFO"
            },
            {
                "topic": "same-store sales quality",
                "section_a": "strong consumer demand across all categories",
                "section_b": "driven by one-time promotional event, underlying demand soft",
                "significance": "CEO characterizes growth as broad-based, CFO says it was one-time"
            }
        ]
    },

    "doc_004": {
        "id": "doc_004",
        "title": "NovaPharma Q1 2024 Earnings Report",
        "content": """
NovaPharma Ltd. reported first-quarter 2024 revenue of $2.14 billion, a decline of 
3.2% compared to Q1 2023 revenue of $2.21 billion. The decrease was primarily 
attributable to generic competition for Cardivex, the company's flagship 
cardiovascular drug, which saw revenue fall 41% to $312 million.

CEO Dr. Emily Chen highlighted that the oncology pipeline showed strong momentum, 
with three compounds advancing to Phase 3 trials. Research and development expenses 
increased 22.4% to $487 million, representing 22.8% of total revenue.

The company reported a net loss of $43 million compared to net income of $287 million 
in Q1 2023. Adjusted EPS was $0.84, down from $1.21 in the prior year period. 
NovaPharma reaffirmed full-year 2024 revenue guidance of $8.6 billion to $8.9 billion.

Cash and investments stood at $4.8 billion, providing runway for continued R&D 
investment and potential bolt-on acquisitions in the oncology space.
        """.strip(),
        "facts": {
            "revenue": "2.14 billion",
            "company_name": "NovaPharma Ltd.",
            "date": "Q1 2024",
            "yoy_change": "-3.2%"
        },
        "questions": [
            "What was NovaPharma's Q1 2024 revenue?",
            "Who is the CEO of NovaPharma?",
            "What was the R&D expense as a percentage of revenue?",
            "What happened to Cardivex revenue?"
        ],
        "answers": [
            "NovaPharma Q1 2024 revenue was 2.14 billion dollars",
            "The CEO of NovaPharma is Dr. Emily Chen",
            "R&D expense was 22.8 percent of total revenue",
            "Cardivex revenue fell 41 percent due to generic competition"
        ]
    },

    "doc_005": {
        "id": "doc_005",
        "title": "FusionEnergy Annual Report 2023 — Conflicting Statements",
        "content": """
SECTION A — Executive Summary:
FusionEnergy Inc. achieved record performance in 2023 with total revenue of $15.6 billion,
up 19.4% from $13.1 billion in 2022. The renewable energy segment was the primary 
growth driver, contributing $6.2 billion or 39.7% of total revenue, up from 28% in 2022.

The company reduced its carbon emissions by 34% year-over-year, achieving its 2025 
sustainability target two years ahead of schedule. Capital expenditure of $3.8 billion 
was deployed primarily toward solar and wind capacity expansion.

SECTION B — Risk Factors and Operational Review:
Total 2023 revenue of $15.6 billion included $1.9 billion in one-time asset sale gains
which will not recur in 2024. Excluding these gains, organic revenue growth was 4.8%.

The renewable segment's reported contribution of $6.2 billion includes $2.1 billion 
from carbon credit sales, which face significant regulatory uncertainty in 2024 and beyond.
The company's carbon emission reduction figures use a 2019 baseline rather than the 
2022 baseline referenced by industry peers, making direct comparisons misleading.

Capital expenditure of $3.8 billion was partially funded by $2.4 billion in 
sale-leaseback transactions, meaning net owned asset investment was only $1.4 billion.
        """.strip(),
        "conflicts": [
            {
                "topic": "revenue growth quality",
                "section_a": "19.4% revenue growth to $15.6 billion",
                "section_b": "organic growth was only 4.8% excluding $1.9 billion one-time gains",
                "significance": "headline growth overstated by $1.9 billion in non-recurring items"
            },
            {
                "topic": "renewable energy contribution",
                "section_a": "$6.2 billion renewable revenue, 39.7% of total",
                "section_b": "$2.1 billion of that is carbon credits facing regulatory risk",
                "significance": "true recurring renewable revenue is significantly lower"
            },
            {
                "topic": "carbon emission reduction",
                "section_a": "34% reduction, achieved 2025 target early",
                "section_b": "uses 2019 baseline not 2022, making comparison misleading",
                "significance": "sustainability achievement may be overstated due to baseline choice"
            }
        ]
    }
}


def get_document(doc_id: str) -> dict:
    return DOCUMENTS.get(doc_id, {})


def get_all_ids() -> list[str]:
    return list(DOCUMENTS.keys())


def get_extract_facts_docs() -> list[str]:
    """Documents suitable for fact extraction task."""
    return ["doc_001", "doc_002", "doc_004"]


def get_answer_questions_docs() -> list[str]:
    """Documents suitable for Q&A task."""
    return ["doc_001", "doc_002", "doc_004"]


def get_conflict_docs() -> list[str]:
    """Documents suitable for conflict identification task."""
    return ["doc_003", "doc_005"]
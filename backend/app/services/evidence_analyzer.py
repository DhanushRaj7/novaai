import json

from app.schemas.evidence import EvidenceAnalysis
from app.services.llm_service import generate_json


def analyze_research_evidence(
    *,
    opportunity_name: str,
    opportunity_description: str,
    source_title: str,
    source_url: str,
    chunk_content: str,
) -> EvidenceAnalysis:

    prompt = f"""
You are an enterprise AI research analyst.

Evaluate whether the following research excerpt provides useful
evidence for the AI opportunity.

AI opportunity:
{opportunity_name}

Opportunity description:
{opportunity_description}

Research source:
{source_title}

Source URL:
{source_url}

Research excerpt:
{chunk_content}

Return ONLY valid JSON using exactly this structure:

{{
  "claim": "specific claim supported by the research excerpt",
  "supporting_excerpt": "short excerpt from the provided research",
  "relevance_score": 0.0,
  "confidence_score": 0.0
}}

Rules:
- Do not invent facts that are not supported by the excerpt.
- The claim must relate directly to the AI opportunity.
- supporting_excerpt must come from the provided excerpt.
- Scores must be between 0 and 1.
- Return JSON only.
"""

    result = generate_json(prompt)

    data = json.loads(result)

    return EvidenceAnalysis.model_validate(data)
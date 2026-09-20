from sqlalchemy.orm import Session

from app.models.ai_opportunity import AIOpportunity
from app.models.evidence import Evidence
from app.models.research_source import ResearchSource
from app.schemas.evidence import EvidenceAnalysis


def persist_evidence(
    db: Session,
    *,
    opportunity: AIOpportunity,
    source: ResearchSource,
    analysis: EvidenceAnalysis,
) -> Evidence:

    evidence = Evidence(
        ai_opportunity_id=opportunity.id,
        source_id=source.id,
        claim=analysis.claim,
        excerpt=analysis.supporting_excerpt,
        relevance_score=analysis.relevance_score,
        confidence_score=analysis.confidence_score,
    )

    db.add(evidence)
    db.commit()
    db.refresh(evidence)

    return evidence
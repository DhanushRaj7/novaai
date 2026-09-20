from app.db.database import SessionLocal
from app.models.ai_opportunity import AIOpportunity
from app.models.research_chunk import ResearchChunk
from app.services.evidence_analyzer import analyze_research_evidence
from app.services.evidence_persistence import persist_evidence


db = SessionLocal()

try:
    opportunity = db.get(AIOpportunity, 1)

    if opportunity is None:
        raise ValueError("AI Opportunity 1 not found")

    chunk = db.query(ResearchChunk).first()

    if chunk is None:
        raise ValueError("No research chunks found")

    source = chunk.source

    analysis = analyze_research_evidence(
        opportunity_name=opportunity.name,
        opportunity_description=opportunity.description,
        source_title=source.title,
        source_url=source.url,
        chunk_content=chunk.content,
    )

    evidence = persist_evidence(
        db,
        opportunity=opportunity,
        source=source,
        analysis=analysis,
    )

    print("\n--- EVIDENCE STORED ---\n")

    print("Evidence ID:", evidence.id)
    print("Opportunity ID:", evidence.ai_opportunity_id)
    print("Source ID:", evidence.source_id)
    print("Claim:", evidence.claim)
    print("Relevance:", evidence.relevance_score)
    print("Confidence:", evidence.confidence_score)

finally:
    db.close()
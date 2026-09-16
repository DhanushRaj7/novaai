from app.db.database import SessionLocal
from app.models.ai_opportunity import AIOpportunity
from app.models.research_source import ResearchSource
from app.models.evidence import Evidence


db = SessionLocal()

try:
    opportunity = db.get(AIOpportunity, 1)

    if opportunity is None:
        raise ValueError("AI Opportunity #1 not found")

    source = ResearchSource(
        title="AI in Financial Services",
        url="https://www.bis.org/",
        publisher="Bank for International Settlements",
        source_type="research",
    )

    db.add(source)
    db.flush()

    evidence = Evidence(
        source_id=source.id,
        ai_opportunity_id=opportunity.id,
        claim="AI can support the extraction and classification of information from financial documents.",
        excerpt="AI-based document processing can assist financial institutions with extracting information from large volumes of documents.",
        relevance_score=0.90,
        confidence_score=0.85,
    )

    db.add(evidence)
    db.commit()

    print("Research source created:", source.id)
    print("Evidence created:", evidence.id)
    print("Linked to AI opportunity:", opportunity.id)

finally:
    db.close()
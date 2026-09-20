from sqlalchemy.orm import Session

from app.models.ai_opportunity import AIOpportunity
from app.services.research_storage import search_research_chunks


def retrieve_research_for_opportunity(
    db: Session,
    opportunity_id: int,
    limit: int = 5,
):
    """Retrieve research relevant to an AI opportunity."""

    opportunity = db.get(AIOpportunity, opportunity_id)

    if opportunity is None:
        raise ValueError(f"AI Opportunity {opportunity_id} not found")

    query = (
        f"{opportunity.name}. "
        f"{opportunity.description}. "
        f"AI capability: {opportunity.ai_capability}"
    )

    return search_research_chunks(
        db,
        query=query,
        limit=limit,
    )
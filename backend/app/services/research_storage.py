from sqlalchemy.orm import Session

from app.models.research_chunk import ResearchChunk
from app.services.embedding_service import generate_embedding

from sqlalchemy import select


def search_research_chunks(
    db: Session,
    *,
    query: str,
    limit: int = 5,
) -> list[ResearchChunk]:
    """Find research chunks semantically similar to a query."""

    query_embedding = generate_embedding(query)

    distance = ResearchChunk.embedding.cosine_distance(query_embedding)

    statement = (
        select(ResearchChunk)
        .where(ResearchChunk.embedding.is_not(None))
        .order_by(distance)
        .limit(limit)
    )

    return list(db.scalars(statement).all())


def store_research_chunk(
    db: Session,
    *,
    source_id: int,
    content: str,
) -> ResearchChunk:
    """Create a research chunk and store its embedding."""

    embedding = generate_embedding(content)

    chunk = ResearchChunk(
        source_id=source_id,
        content=content,
        embedding=embedding,
    )

    db.add(chunk)
    db.commit()
    db.refresh(chunk)

    return chunk
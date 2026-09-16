from sqlalchemy.orm import Session

from app.models.research_source import ResearchSource
from app.services.research_engine import build_research_document
from app.services.research_storage import store_research_chunk


def index_research_source(
    db: Session,
    *,
    title: str,
    url: str,
    publisher: str,
    source_type: str,
) -> ResearchSource | None:
    """Fetch, process, and index a research source."""

    document = build_research_document(
        title=title,
        url=url,
        publisher=publisher,
        source_type=source_type,
    )

    if document is None:
        return None

    source = ResearchSource(
        title=document.title,
        url=document.url,
        publisher=document.publisher,
        source_type=document.source_type,
        retrieved_at=document.retrieved_at,
    )

    db.add(source)
    db.flush()

    for chunk in document.chunks:
        store_research_chunk(
            db,
            source_id=source.id,
            content=chunk,
        )

    return source
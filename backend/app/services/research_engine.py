from dataclasses import dataclass
from datetime import datetime, timezone

import httpx

from bs4 import BeautifulSoup

from ddgs import DDGS

from urllib.parse import urlparse


@dataclass
class ResearchResult:
    title: str
    url: str
    publisher: str
    source_type: str
    claim: str
    excerpt: str
    relevance_score: float
    confidence_score: float
    publication_date: datetime | None = None
    retrieved_at: datetime | None = None

@dataclass
class ResearchDocument:
    title: str
    url: str
    publisher: str
    source_type: str
    chunks: list[str]
    retrieved_at: datetime




def is_valid_research_url(url: str) -> bool:
    """Reject tracking, advertisement, and malformed URLs."""

    if not url:
        return False

    parsed = urlparse(url)

    if parsed.scheme not in {"http", "https"}:
        return False

    hostname = (parsed.hostname or "").lower()

    blocked_domains = {
        "bing.com",
        "www.bing.com",
    }

    if hostname in blocked_domains:
        return False

    if "aclick" in parsed.path.lower():
        return False

    return True


def classify_source_type(url: str) -> str:
    """Classify a research source based on its domain."""

    hostname = (urlparse(url).hostname or "").lower()

    if hostname.endswith(".gov") or hostname.endswith(".gov.uk"):
        return "regulatory_guidance"

    if hostname.endswith(".edu"):
        return "research"

    research_domains = {
        "bis.org",
        "arxiv.org",
        "nber.org",
    }

    if hostname in research_domains:
        return "research"

    industry_domains = {
        "iso.org",
        "nist.gov",
    }

    if hostname in industry_domains:
        return "industry_standard"

    vendor_domains = {
        "aws.amazon.com",
        "cloud.google.com",
        "azure.microsoft.com",
    }

    if hostname in vendor_domains:
        return "vendor_information"

    return "general_web_content"


def classify_source_type(url: str) -> str:
    """Classify a research source based on its domain."""

    hostname = (urlparse(url).hostname or "").lower()

    if hostname.endswith(".gov") or hostname.endswith(".gov.uk"):
        return "regulatory_guidance"

    if hostname.endswith(".edu"):
        return "research"

    research_domains = {
        "bis.org",
        "arxiv.org",
        "nber.org",
    }

    if hostname in research_domains:
        return "research"

    industry_domains = {
        "iso.org",
        "nist.gov",
    }

    if hostname in industry_domains:
        return "industry_standard"

    vendor_domains = {
        "aws.amazon.com",
        "cloud.google.com",
        "azure.microsoft.com",
    }

    if hostname in vendor_domains:
        return "vendor_information"

    return "general_web_content"


def fetch_page(url: str) -> str:
    """Fetch the text content of a research page."""

    try:
        response = httpx.get(
            url,
            timeout=10.0,
            follow_redirects=True,
            headers={
                "User-Agent": "NovaAI-Research/1.0"
            },
        )

        response.raise_for_status()

        return response.text

    except httpx.HTTPError as exc:
        print(f"Failed to fetch {url}: {exc}")
        return ""


def extract_text(html: str) -> str:
    """Convert raw HTML into readable page text."""

    soup = BeautifulSoup(html, "html.parser")

    # Remove content that is not useful for research.
    for element in soup(
        ["script", "style", "noscript", "nav", "footer", "header"]
    ):
        element.decompose()

    text = soup.get_text(separator=" ", strip=True)

    return text

def chunk_text(
    text: str,
    *,
    chunk_size: int = 1200,
    overlap: int = 200,
) -> list[str]:
    """Split research text into overlapping chunks."""

    if not text:
        return []

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


def build_research_document(
    *,
    title: str,
    url: str,
    publisher: str,
    source_type: str,
) -> ResearchDocument | None:
    """Fetch, clean, and chunk a research source."""

    html = fetch_page(url)

    if not html:
        return None

    text = extract_text(html)

    if not text:
        return None

    chunks = chunk_text(text)

    if not chunks:
        return None

    return ResearchDocument(
        title=title,
        url=url,
        publisher=publisher,
        source_type=source_type,
        chunks=chunks,
        retrieved_at=datetime.now(timezone.utc),
    )


def research_ai_opportunity(
    *,
    opportunity_name: str,
    opportunity_description: str,
) -> list[ResearchResult]:
    """
    Search the web for evidence relevant to an AI opportunity.

    Search is intentionally separated from:
    - evidence extraction
    - AI analysis
    - scoring
    - database persistence
    """

    query = f"{opportunity_name} {opportunity_description}"

    results: list[ResearchResult] = []

    with DDGS() as ddgs:
        search_results = ddgs.text(
            query,
            max_results=5,
        )

        for result in search_results:
            url = result.get("href", "")
            title = result.get("title", "")
            body = result.get("body", "")

            if not is_valid_research_url(url):
                continue

            results.append(
                ResearchResult(
                    title=title,
                    url=url,
                    publisher="",
                    source_type=classify_source_type(url),
                    claim=f"Potential evidence relevant to {opportunity_name}.",
                    excerpt=body,
                    relevance_score=0.0,
                    confidence_score=0.0,
                    retrieved_at=datetime.now(timezone.utc),
                )
            )

    return results
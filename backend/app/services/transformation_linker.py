from __future__ import annotations

import re
from collections import Counter

from sqlalchemy.orm import Session

from app.models.ai_opportunity import AIOpportunity
from app.models.ai_opportunity_initiative import AIOpportunityInitiative
from app.models.initiative import TransformationInitiative
from app.models.process import Process
from app.models.process_role import ProcessRole
from app.models.role import Role


STOP_WORDS = {
    "the", "and", "for", "with", "from", "into", "this", "that",
    "process", "management", "assessment", "support", "system", "data",
    "customer", "enterprise", "ai", "artificial", "intelligence",
}


ROLE_KEYWORDS = {
    "credit analyst": {"credit", "loan", "lending", "assessment", "risk"},
    "loan officer": {"loan", "lending", "customer", "credit", "application"},
    "customer service representative": {
        "customer", "complaint", "service", "support", "query", "issue", "resolution"
    },
    "risk analyst": {"risk", "assessment", "investigation", "fraud", "decision"},
    "compliance officer": {
        "compliance", "regulatory", "complaint", "investigation", "policy", "review"
    },
    "fraud analyst": {"fraud", "suspicious", "transaction", "investigation", "detection"},
    "data scientist": {"analytics", "prediction", "predictive", "model", "machine", "data"},
    "ai product manager": {"ai", "automation", "product", "transformation", "workflow"},
}


def _tokens(*values: str | None) -> set[str]:
    text = " ".join(str(value) for value in values if value is not None).lower()
    words = re.findall(r"[a-z0-9]+", text)
    return {
        word
        for word in words
        if len(word) > 2 and word not in STOP_WORDS
    }


def _score_role(process: Process, role: Role) -> float:
    process_tokens = _tokens(process.name, process.description)
    role_tokens = _tokens(role.name, role.description)

    score = 0.0
    score += len(process_tokens & role_tokens) * 2.0

    configured_keywords = ROLE_KEYWORDS.get(
        role.name.lower(),
        set(),
    )
    score += len(process_tokens & configured_keywords) * 3.0

    if role.name.lower() in process.name.lower():
        score += 5.0

    return score


def link_roles_to_process(
    db: Session,
    process: Process,
    minimum_score: float = 2.0,
    max_roles: int = 3,
) -> list[Role]:
    """Connect an analyzed process to the most relevant existing roles."""

    existing_links = (
        db.query(ProcessRole)
        .filter(ProcessRole.process_id == process.id)
        .all()
    )

    if existing_links:
        return [link.role for link in existing_links]

    roles = db.query(Role).order_by(Role.id).all()

    ranked = sorted(
        ((role, _score_role(process, role)) for role in roles),
        key=lambda item: (-item[1], item[0].id),
    )

    selected = [
        role
        for role, score in ranked
        if score >= minimum_score
    ][:max_roles]

    # Ensure a new process gets at least one meaningful role when the
    # keyword model has insufficient evidence. The fallback is deterministic
    # and uses the first available enterprise role rather than inventing one.
    if not selected and roles:
        selected = [roles[0]]

    for role in selected:
        db.add(
            ProcessRole(
                process_id=process.id,
                role_id=role.id,
                responsibility=f"Supports {process.name}",
            )
        )

    db.flush()
    return selected


INITIATIVE_DOMAIN_RULES = {
    "ai-assisted credit assessment": {
        "strong_phrases": {
            "credit assessment",
            "credit scoring",
            "credit underwriting",
            "underwriting",
            "credit risk assessment",
        },
        "supporting_terms": {
            "credit",
            "lending",
            "loan underwriting",
        },
    },
    "data & model governance foundation": {
        "strong_phrases": {
            "data governance",
            "model governance",
            "responsible ai",
            "model risk",
            "regulatory compliance",
        },
        "supporting_terms": {
            "governance",
            "privacy",
            "security",
            "compliance",
            "regulatory",
            "monitoring",
            "explainability",
            "model",
            "risk",
            "data",
        },
    },
    "enterprise data quality foundation": {
        "strong_phrases": {
            "data quality",
            "data platform",
            "master data",
            "data integration",
        },
        "supporting_terms": {
            "data",
            "analytics",
            "document",
            "transaction",
            "information",
            "quality",
            "integration",
            "pipeline",
        },
    },
}


def _initiative_rule(initiative: TransformationInitiative) -> dict[str, set[str]]:
    return INITIATIVE_DOMAIN_RULES.get(
        initiative.name.strip().lower(),
        {"strong_phrases": set(), "supporting_terms": set()},
    )


def _score_initiative(
    process: Process,
    opportunity: AIOpportunity,
    initiative: TransformationInitiative,
) -> float:
    """
    Score initiative relevance using explicit enterprise-domain rules.

    A generic word overlap is not enough for a domain-specific initiative.
    For example, a fraud process containing "loan" should not automatically
    be linked to the credit-assessment initiative.
    """
    process_text = f"{process.name or ''} {process.description or ''}".lower()
    opportunity_text = (
        f"{opportunity.name or ''} "
        f"{opportunity.description or ''} "
        f"{opportunity.ai_capability or ''} "
        f"{opportunity.reasoning or ''}"
    ).lower()
    combined_text = f"{process_text} {opportunity_text}"

    combined_tokens = _tokens(
        process.name,
        process.description,
        opportunity.name,
        opportunity.description,
        opportunity.ai_capability,
    )

    rule = _initiative_rule(initiative)
    initiative_name = initiative.name.strip().lower()

    if not rule["strong_phrases"] and not rule["supporting_terms"]:
        return 0.0

    score = 0.0

    strong_phrase_hits = sum(
        1
        for phrase in rule["strong_phrases"]
        if phrase in combined_text
    )
    score += strong_phrase_hits * 6.0

    supporting_hits = len(combined_tokens & rule["supporting_terms"])
    score += supporting_hits * 1.5

    if initiative_name == "ai-assisted credit assessment":
        # Require at least two genuine credit-domain signals. This prevents
        # "loan application fraud" from being treated as credit assessment
        # merely because the word "loan" appears.
        credit_signals = {
            "credit",
            "underwriting",
            "credit scoring",
            "credit risk",
            "credit assessment",
        }
        credit_signal_count = sum(
            1
            for signal in credit_signals
            if signal in combined_text
        )
        if credit_signal_count < 2:
            return 0.0

    if initiative_name == "data & model governance foundation":
        # Governance is a legitimate cross-enterprise prerequisite for AI.
        score += 2.0

    if initiative_name == "enterprise data quality foundation":
        data_signals = {
            "analytics",
            "document",
            "transaction",
            "data",
            "model",
            "prediction",
            "detection",
        }
        if not (combined_tokens & data_signals):
            return 0.0

    return score


def link_opportunities_to_initiatives(
    db: Session,
    process: Process,
    opportunities: list[AIOpportunity],
    max_initiatives_per_opportunity: int = 2,
) -> list[TransformationInitiative]:
    """
    Connect AI opportunities only to evidence-backed initiatives.

    There is deliberately no fallback to arbitrary initiatives. This keeps
    the transformation graph semantically meaningful.
    """
    initiatives = (
        db.query(TransformationInitiative)
        .order_by(TransformationInitiative.priority.desc())
        .all()
    )

    if not initiatives or not opportunities:
        return []

    linked_initiatives: dict[int, TransformationInitiative] = {}

    for opportunity in opportunities:
        existing_links = (
            db.query(AIOpportunityInitiative)
            .filter(
                AIOpportunityInitiative.ai_opportunity_id == opportunity.id
            )
            .all()
        )

        if existing_links:
            for link in existing_links:
                initiative = db.get(
                    TransformationInitiative,
                    link.initiative_id,
                )
                if initiative is not None:
                    linked_initiatives[initiative.id] = initiative
            continue

        ranked = sorted(
            (
                (
                    initiative,
                    _score_initiative(
                        process=process,
                        opportunity=opportunity,
                        initiative=initiative,
                    ),
                )
                for initiative in initiatives
            ),
            key=lambda item: (-item[1], item[0].id),
        )

        # Only relationships with a meaningful relevance score are persisted.
        selected = [
            initiative
            for initiative, score in ranked
            if score >= 3.0
        ][:max_initiatives_per_opportunity]

        for initiative in selected:
            initiative_name = initiative.name.lower()
            relationship_type = "supports"

            if "governance" in initiative_name:
                relationship_type = "governance_prerequisite"
            elif "data quality" in initiative_name:
                relationship_type = "data_prerequisite"

            db.add(
                AIOpportunityInitiative(
                    ai_opportunity_id=opportunity.id,
                    initiative_id=initiative.id,
                    relationship_type=relationship_type,
                )
            )
            linked_initiatives[initiative.id] = initiative

    db.flush()
    return list(linked_initiatives.values())


def link_transformation_intelligence(
    db: Session,
    process: Process,
    opportunities: list[AIOpportunity],
) -> tuple[list[Role], list[TransformationInitiative]]:
    roles = link_roles_to_process(
        db=db,
        process=process,
    )

    initiatives = link_opportunities_to_initiatives(
        db=db,
        process=process,
        opportunities=opportunities,
    )

    return roles, initiatives

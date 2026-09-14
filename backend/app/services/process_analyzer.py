from app.models.process import Process
from app.schemas.analysis import (
    ActivityAnalysis,
    AIOpportunityAnalysis,
    ProcessAnalysis,
)


def analyze_process(process: Process) -> ProcessAnalysis:
    """
    Deterministic baseline analyzer.

    This is intentionally simple.
    Later, the same contract will be produced by
    an LLM + research pipeline.
    """

    activities = [
        ActivityAnalysis(
            name="Collect customer documents",
            description=(
                "Collect and review income, identity, employment, "
                "and financial documents."
            ),
            sequence=1,
            activity_type="document_review",
            decision_required=False,
        ),
        ActivityAnalysis(
            name="Assess creditworthiness",
            description=(
                "Evaluate customer financial information and "
                "credit history to assess repayment risk."
            ),
            sequence=2,
            activity_type="risk_assessment",
            decision_required=True,
        ),
        ActivityAnalysis(
            name="Determine lending recommendation",
            description=(
                "Determine an appropriate lending recommendation "
                "based on the customer's risk profile."
            ),
            sequence=3,
            activity_type="decision",
            decision_required=True,
        ),
    ]

    opportunities = [
        AIOpportunityAnalysis(
            name="AI-assisted document review",
            description=(
                "Use AI to extract and classify information from "
                "customer documents before analyst review."
            ),
            ai_capability="document_intelligence",
            automation_potential=0.80,
            human_involvement=0.40,
            expected_benefit=0.85,
            feasibility=0.85,
            strategic_alignment=0.90,
            risk_level=0.45,
            reasoning=(
                "Document-heavy work has strong potential for AI "
                "assistance, while human review remains important "
                "for validation and exceptions."
            ),
        ),
        AIOpportunityAnalysis(
            name="AI-assisted credit risk analysis",
            description=(
                "Use AI to summarize financial information and "
                "identify relevant risk indicators for credit analysts."
            ),
            ai_capability="decision_support",
            automation_potential=0.65,
            human_involvement=0.65,
            expected_benefit=0.90,
            feasibility=0.70,
            strategic_alignment=0.95,
            risk_level=0.75,
            reasoning=(
                "AI can support analysts by synthesizing complex "
                "information, but lending decisions have significant "
                "financial and regulatory impact and require human oversight."
            ),
        ),
    ]

    return ProcessAnalysis(
        summary=(
            f"{process.name} contains document-intensive and "
            "decision-intensive activities that could benefit from "
            "AI-assisted processing and decision support."
        ),
        activities=activities,
        ai_opportunities=opportunities,
    )
from sqlalchemy.orm import Session

from app.models.ai_opportunity import AIOpportunity
from app.models.governance import GovernanceAssessment
from app.schemas.governance import GovernanceAnalysis
from app.services.governance_scoring import calculate_overall_risk


def persist_governance_assessment(
    db: Session,
    *,
    opportunity: AIOpportunity,
    analysis: GovernanceAnalysis,
) -> GovernanceAssessment:

    overall_risk = calculate_overall_risk(
        data_risk=analysis.data_risk,
        privacy_risk=analysis.privacy_risk,
        bias_risk=analysis.bias_risk,
        security_risk=analysis.security_risk,
        decision_impact=analysis.decision_impact,
        regulatory_exposure=analysis.regulatory_exposure,
        model_risk=analysis.model_risk,
    )

    assessment = db.query(GovernanceAssessment).filter(
        GovernanceAssessment.ai_opportunity_id == opportunity.id
    ).first()

    if assessment is None:
        assessment = GovernanceAssessment(
            ai_opportunity_id=opportunity.id,
        )
        db.add(assessment)

    assessment.data_risk = analysis.data_risk
    assessment.privacy_risk = analysis.privacy_risk
    assessment.bias_risk = analysis.bias_risk
    assessment.oversight_requirement = analysis.oversight_requirement
    assessment.explainability_requirement = analysis.explainability_requirement
    assessment.security_risk = analysis.security_risk
    assessment.decision_impact = analysis.decision_impact
    assessment.regulatory_exposure = analysis.regulatory_exposure
    assessment.model_risk = analysis.model_risk
    assessment.monitoring_requirement = analysis.monitoring_requirement
    assessment.overall_risk = overall_risk
    assessment.reasoning = analysis.reasoning

    db.commit()
    db.refresh(assessment)

    return assessment
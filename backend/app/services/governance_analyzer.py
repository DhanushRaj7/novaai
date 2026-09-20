import json

from app.models.ai_opportunity import AIOpportunity
from app.schemas.governance import GovernanceAnalysis
from app.services.llm_service import generate_json


def analyze_governance(
    opportunity: AIOpportunity,
) -> GovernanceAnalysis:

    prompt = f"""
You are an enterprise AI governance analyst.

Assess the governance risks and control requirements
for the following AI opportunity.

AI Opportunity:
{opportunity.name}

Description:
{opportunity.description}

AI Capability:
{opportunity.ai_capability}

Automation Potential:
{opportunity.automation_potential}

Human Involvement:
{opportunity.human_involvement}

Expected Benefit:
{opportunity.expected_benefit}

Feasibility:
{opportunity.feasibility}

Strategic Alignment:
{opportunity.strategic_alignment}

Risk Level:
{opportunity.risk_level}

Return ONLY valid JSON using exactly this structure:

{{
  "data_risk": 0.0,
  "privacy_risk": 0.0,
  "bias_risk": 0.0,
  "oversight_requirement": "required level of human oversight",
  "explainability_requirement": "required level of explainability",
  "security_risk": 0.0,
  "decision_impact": 0.0,
  "regulatory_exposure": 0.0,
  "model_risk": 0.0,
  "monitoring_requirement": "required monitoring level",
  "reasoning": "explain the governance assessment"
}}

Rules:
- All numeric risk values must be between 0 and 1.
- 0 means very low risk.
- 1 means very high risk.
- Base the assessment on the AI opportunity provided.
- Consider the potential impact on customers, employees,
  business decisions, sensitive data, and regulated activities.
- Do not invent specific laws or regulations.
- Explain the reasoning clearly.
- Return JSON only.
"""

    result = generate_json(prompt)

    data = json.loads(result)

    return GovernanceAnalysis.model_validate(data)
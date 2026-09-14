from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.ai_opportunity import AIOpportunity
from app.models.activity_ai_opportunity import ActivityAIOpportunity
from app.models.process import Process
from app.schemas.analysis import ProcessAnalysis
from app.services.scoring_engine import calculate_priority_score


def persist_analysis(
    db: Session,
    process: Process,
    analysis: ProcessAnalysis,
) -> Process:

    # Create activities
    activity_models = []

    for activity_data in analysis.activities:
        activity = Activity(
            process_id=process.id,
            name=activity_data.name,
            description=activity_data.description,
            sequence=activity_data.sequence,
            activity_type=activity_data.activity_type,
            decision_required=activity_data.decision_required,
        )

        db.add(activity)
        activity_models.append(activity)

    db.flush()

    # Create AI opportunities
    for index, opportunity_data in enumerate(
        analysis.ai_opportunities
    ):
        priority_score = calculate_priority_score(
            automation_potential=opportunity_data.automation_potential,
            human_involvement=opportunity_data.human_involvement,
            expected_benefit=opportunity_data.expected_benefit,
            feasibility=opportunity_data.feasibility,
            strategic_alignment=opportunity_data.strategic_alignment,
            risk_level=opportunity_data.risk_level,
        )

        opportunity = AIOpportunity(
            name=opportunity_data.name,
            description=opportunity_data.description,
            ai_capability=opportunity_data.ai_capability,
            automation_potential=opportunity_data.automation_potential,
            human_involvement=opportunity_data.human_involvement,
            expected_benefit=opportunity_data.expected_benefit,
            feasibility=opportunity_data.feasibility,
            strategic_alignment=opportunity_data.strategic_alignment,
            risk_level=opportunity_data.risk_level,
            priority_score=priority_score,
            reasoning=opportunity_data.reasoning,
        )

        db.add(opportunity)
        db.flush()

        # For this first vertical slice, associate
        # opportunities with activities sequentially.
        activity = activity_models[
            min(index, len(activity_models) - 1)
        ]

        link = ActivityAIOpportunity(
            activity_id=activity.id,
            ai_opportunity_id=opportunity.id,
            impact_type="ai_assistance",
        )

        db.add(link)

    # Update process priority using the highest opportunity score
    if analysis.ai_opportunities:
        scores = [
            calculate_priority_score(
                automation_potential=o.automation_potential,
                human_involvement=o.human_involvement,
                expected_benefit=o.expected_benefit,
                feasibility=o.feasibility,
                strategic_alignment=o.strategic_alignment,
                risk_level=o.risk_level,
            )
            for o in analysis.ai_opportunities
        ]

        process.priority_score = max(scores)

    db.commit()
    db.refresh(process)

    return process
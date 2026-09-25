from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.ai_opportunity import AIOpportunity
from app.models.ai_opportunity_initiative import AIOpportunityInitiative
from app.models.activity_ai_opportunity import ActivityAIOpportunity
from app.models.governance import GovernanceAssessment
from app.models.process import Process
from app.models.process_role import ProcessRole

from app.schemas.analysis import ProcessAnalysis

from app.services.scoring_engine import calculate_priority_score
from app.services.opportunity_research import retrieve_research_for_opportunity
from app.services.evidence_analyzer import analyze_research_evidence
from app.services.evidence_persistence import persist_evidence
from app.services.governance_analyzer import analyze_governance
from app.services.governance_persistence import persist_governance_assessment
from app.services.transformation_linker import link_transformation_intelligence


def clear_existing_analysis(
    db: Session,
    process: Process,
) -> None:
    """
    Remove previously generated analysis for a process.

    This also removes opportunity → initiative links before deleting
    opportunities, preventing stale foreign-key rows during re-analysis.
    Existing process → role links are intentionally preserved so that
    manually curated role assignments are not destroyed by re-analysis.
    """

    existing_activities = (
        db.query(Activity)
        .filter(Activity.process_id == process.id)
        .all()
    )

    for activity in existing_activities:
        links = (
            db.query(ActivityAIOpportunity)
            .filter(
                ActivityAIOpportunity.activity_id == activity.id
            )
            .all()
        )

        for link in links:
            opportunity = db.get(
                AIOpportunity,
                link.ai_opportunity_id,
            )

            if opportunity is not None:
                initiative_links = (
                    db.query(AIOpportunityInitiative)
                    .filter(
                        AIOpportunityInitiative.ai_opportunity_id
                        == opportunity.id
                    )
                    .all()
                )

                for initiative_link in initiative_links:
                    db.delete(initiative_link)

                governance = (
                    db.query(GovernanceAssessment)
                    .filter(
                        GovernanceAssessment.ai_opportunity_id
                        == opportunity.id
                    )
                    .first()
                )

                if governance is not None:
                    db.delete(governance)

                db.delete(opportunity)

            db.delete(link)

        db.delete(activity)

    db.flush()


def persist_analysis(
    db: Session,
    process: Process,
    analysis: ProcessAnalysis,
) -> Process:
    # ---------------------------------------------------------
    # Remove previous generated analysis
    # ---------------------------------------------------------

    clear_existing_analysis(
        db=db,
        process=process,
    )

    # ---------------------------------------------------------
    # Create activities
    # ---------------------------------------------------------

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

    # ---------------------------------------------------------
    # Create AI opportunities
    # ---------------------------------------------------------

    opportunity_models: list[AIOpportunity] = []

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
        opportunity_models.append(opportunity)

        # -----------------------------------------------------
        # Associate opportunity with an activity
        # -----------------------------------------------------

        if activity_models:
            activity = activity_models[
                min(index, len(activity_models) - 1)
            ]

            link = ActivityAIOpportunity(
                activity_id=activity.id,
                ai_opportunity_id=opportunity.id,
                impact_type="ai_assistance",
            )

            db.add(link)

        # -----------------------------------------------------
        # Research stage
        # -----------------------------------------------------

        research_results = retrieve_research_for_opportunity(
            db=db,
            opportunity_id=opportunity.id,
            limit=3,
        )

        for research_result in research_results:
            chunk, distance = research_result
            source = chunk.source

            evidence_analysis = analyze_research_evidence(
                opportunity_name=opportunity.name,
                opportunity_description=opportunity.description,
                source_title=source.title,
                source_url=source.url,
                chunk_content=chunk.content,
            )

            persist_evidence(
                db=db,
                opportunity=opportunity,
                source=source,
                analysis=evidence_analysis,
            )

        # -----------------------------------------------------
        # Governance stage
        # -----------------------------------------------------

        governance_analysis = analyze_governance(
            opportunity=opportunity,
        )

        persist_governance_assessment(
            db=db,
            opportunity=opportunity,
            analysis=governance_analysis,
        )

    # ---------------------------------------------------------
    # Update process priority
    # ---------------------------------------------------------

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
    else:
        process.priority_score = None

    db.flush()

    # ---------------------------------------------------------
    # Cross-enterprise transformation intelligence
    # ---------------------------------------------------------
    # Connect the newly analyzed process to existing enterprise
    # roles and transformation initiatives.

    link_transformation_intelligence(
        db=db,
        process=process,
        opportunities=opportunity_models,
    )

    # ---------------------------------------------------------
    # Commit everything
    # ---------------------------------------------------------

    db.commit()
    db.refresh(process)

    return process

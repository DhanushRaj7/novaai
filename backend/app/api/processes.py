from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.process import Process
from app.schemas.process import ProcessCreate, ProcessResponse

from app.services.process_analyzer import analyze_process
from app.services.analysis_persistence import persist_analysis

from app.models.activity_ai_opportunity import ActivityAIOpportunity

from app.models.governance import GovernanceAssessment

from app.models.activity import Activity
from app.models.ai_opportunity import AIOpportunity
from app.models.evidence import Evidence
from app.models.process_role import ProcessRole
from app.models.role import Role
from app.models.role_skill import RoleSkill
from app.models.skill import Skill



router = APIRouter(
    prefix="/processes",
    tags=["Processes"],
)


@router.post(
    "",
    response_model=ProcessResponse,
)
def create_process(
    process_data: ProcessCreate,
    db: Session = Depends(get_db),
):
    process = Process(
        value_chain_stage_id=process_data.value_chain_stage_id,
        name=process_data.name,
        description=process_data.description,
        business_purpose=process_data.business_purpose,
        current_challenges=process_data.current_challenges,
    )

    db.add(process)
    db.commit()
    db.refresh(process)

    return process


@router.get(
    "",
    response_model=list[ProcessResponse],
)
def get_processes(
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Process).order_by(Process.id)
    )

    return result.scalars().all()


@router.get(
    "/{process_id}",
    response_model=ProcessResponse,
)
def get_process(
    process_id: int,
    db: Session = Depends(get_db),
):
    process = db.get(Process, process_id)

    if process is None:
        raise HTTPException(
            status_code=404,
            detail="Process not found",
        )

    return process


@router.post("/{process_id}/analyze")
def analyze_process_endpoint(
    process_id: int,
    db: Session = Depends(get_db),
):
    process = db.get(Process, process_id)

    if process is None:
        raise HTTPException(
            status_code=404,
            detail="Process not found",
        )

    analysis = analyze_process(process)

    process = persist_analysis(
        db=db,
        process=process,
        analysis=analysis,
    )

    return {
        "process_id": process.id,
        "process_name": process.name,
        "priority_score": process.priority_score,
        "summary": analysis.summary,
        "activities_created": len(analysis.activities),
        "ai_opportunities_created": len(
            analysis.ai_opportunities
        ),
    }


@router.get("/{process_id}/intelligence")
def get_process_intelligence(
    process_id: int,
    db: Session = Depends(get_db),
):
    process = db.get(Process, process_id)

    if process is None:
        raise HTTPException(
            status_code=404,
            detail="Process not found",
        )

    # -------------------------
    # Roles → Skills
    # -------------------------

    role_rows = db.query(
        ProcessRole,
        Role,
    ).join(
        Role,
        ProcessRole.role_id == Role.id,
    ).filter(
        ProcessRole.process_id == process_id,
    ).all()

    roles = []

    for process_role, role in role_rows:

        skill_rows = db.query(
            RoleSkill,
            Skill,
        ).join(
            Skill,
            RoleSkill.skill_id == Skill.id,
        ).filter(
            RoleSkill.role_id == role.id,
        ).all()

        skills = []

        for role_skill, skill in skill_rows:
            skills.append(
                {
                    "id": skill.id,
                    "name": skill.name,
                    "category": skill.category,
                    "importance": role_skill.importance,
                    "status": role_skill.skill_status,
                }
            )

        roles.append(
            {
                "id": role.id,
                "name": role.name,
                "description": role.description,
                "responsibility": process_role.responsibility,
                "skills": skills,
            }
        )

    # -------------------------
    # Activities → AI Opportunities
    # -------------------------

    activities = []

    activity_rows = db.query(Activity).filter(
        Activity.process_id == process_id
    ).order_by(
        Activity.sequence
    ).all()

    for activity in activity_rows:

        opportunity_links = db.query(
            ActivityAIOpportunity
        ).filter(
            ActivityAIOpportunity.activity_id == activity.id
        ).all()

        opportunities = []

        for link in opportunity_links:

            opportunity = db.get(
                AIOpportunity,
                link.ai_opportunity_id,
            )

            if opportunity is None:
                continue

            governance = db.query(
                GovernanceAssessment
            ).filter(
                GovernanceAssessment.ai_opportunity_id == opportunity.id
            ).first()

            evidence_rows = db.query(
                Evidence
            ).filter(
                Evidence.ai_opportunity_id == opportunity.id
            ).all()

            evidence = [
                {
                    "id": item.id,
                    "claim": item.claim,
                    "excerpt": item.excerpt,
                    "relevance_score": item.relevance_score,
                    "confidence_score": item.confidence_score,
                    "source_id": item.source_id,
                }
                for item in evidence_rows
            ]

            governance_data = None

            if governance is not None:
                governance_data = {
                    "id": governance.id,
                    "data_risk": governance.data_risk,
                    "privacy_risk": governance.privacy_risk,
                    "bias_risk": governance.bias_risk,
                    "oversight_requirement": governance.oversight_requirement,
                    "explainability_requirement": governance.explainability_requirement,
                    "security_risk": governance.security_risk,
                    "decision_impact": governance.decision_impact,
                    "regulatory_exposure": governance.regulatory_exposure,
                    "model_risk": governance.model_risk,
                    "monitoring_requirement": governance.monitoring_requirement,
                    "overall_risk": governance.overall_risk,
                    "reasoning": governance.reasoning,
                }

              

            opportunities.append(
                {
                    "id": opportunity.id,
                    "name": opportunity.name,
                    "description": opportunity.description,
                    "ai_capability": opportunity.ai_capability,
                    "automation_potential": opportunity.automation_potential,
                    "human_involvement": opportunity.human_involvement,
                    "expected_benefit": opportunity.expected_benefit,
                    "feasibility": opportunity.feasibility,
                    "strategic_alignment": opportunity.strategic_alignment,
                    "risk_level": opportunity.risk_level,
                    "priority_score": opportunity.priority_score,
                    "governance": governance_data,
                    "reasoning": opportunity.reasoning,
                    "evidence": evidence,
                }
            )

        activities.append(
            {
                "id": activity.id,
                "name": activity.name,
                "description": activity.description,
                "sequence": activity.sequence,
                "activity_type": activity.activity_type,
                "decision_required": activity.decision_required,
                "ai_opportunities": opportunities,
            }
        )

    return {
        "process": {
            "id": process.id,
            "name": process.name,
            "description": process.description,
            "status": process.status,
            "priority_score": process.priority_score,
        },
        "roles": roles,
        "activities": activities,
    }
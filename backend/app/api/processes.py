from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.database import get_db

from app.schemas.process import (
    NewProcessAnalysisRequest,
    ProcessCreate,
    ProcessResponse,
)

from app.models.process import Process
from app.models.role import Role
from app.models.process_role import ProcessRole
from app.models.activity import Activity
from app.models.ai_opportunity import AIOpportunity
from app.models.activity_ai_opportunity import ActivityAIOpportunity
from app.models.evidence import Evidence
from app.models.governance import GovernanceAssessment
from app.models.ai_opportunity_initiative import AIOpportunityInitiative
from app.models.initiative import TransformationInitiative
from app.models.initiative_dependency import InitiativeDependency

from app.services.process_analyzer import analyze_process
from app.services.analysis_persistence import persist_analysis


router = APIRouter(
    prefix="/processes",
    tags=["Processes"],
)


# ============================================================
# PROCESS CRUD
# ============================================================


@router.post("", response_model=ProcessResponse)
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


@router.get("", response_model=list[ProcessResponse])
def get_processes(
    db: Session = Depends(get_db),
):
    result = db.execute(
        select(Process).order_by(Process.id)
    )

    return result.scalars().all()


@router.get("/{process_id}", response_model=ProcessResponse)
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


# ============================================================
# PROCESS ANALYSIS
# ============================================================


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


# ============================================================
# SURPRISE RECORD / DYNAMIC PROCESS ANALYSIS
# ============================================================


@router.post("/analyze-new")
def analyze_new_process(
    payload: NewProcessAnalysisRequest,
    db: Session = Depends(get_db),
):
    # --------------------------------------------------------
    # Create the new process
    # --------------------------------------------------------

    process = Process(
        name=payload.name,
        description=payload.description,
        value_chain_stage_id=payload.value_chain_stage_id,
    )

    db.add(process)
    db.commit()
    db.refresh(process)

    # --------------------------------------------------------
    # Analyze the process using the LLM
    # --------------------------------------------------------

    analysis = analyze_process(process)

    # --------------------------------------------------------
    # Persist the complete analysis
    #
    # This creates:
    #   Activities
    #   AI Opportunities
    #   Activity → AI Opportunity links
    #   Research Evidence
    #   Governance Assessments
    #   Priority Scores
    # --------------------------------------------------------

    process = persist_analysis(
        db=db,
        process=process,
        analysis=analysis,
    )

    # --------------------------------------------------------
    # Return the generated intelligence
    # --------------------------------------------------------

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


# ============================================================
# RECURSIVE INITIATIVE DEPENDENCY TRAVERSAL
# ============================================================


def get_dependency_chain(
    db: Session,
    initiative_id: int,
    visited: set[int] | None = None,
):
    """
    Recursively retrieve all downstream dependencies
    of a transformation initiative.

    Example:

        Initiative 1
            ↓
        Initiative 2
            ↓
        Initiative 3

    The returned structure will preserve that hierarchy.

    `visited` prevents infinite loops if a circular dependency
    accidentally exists in the database.
    """

    if visited is None:
        visited = set()

    # Prevent circular dependency loops.
    if initiative_id in visited:
        return []

    visited.add(initiative_id)

    dependency_rows = (
        db.query(InitiativeDependency)
        .filter(
            InitiativeDependency.initiative_id
            == initiative_id
        )
        .all()
    )

    dependencies = []

    for dependency in dependency_rows:

        depends_on = db.get(
            TransformationInitiative,
            dependency.depends_on_initiative_id,
        )

        if depends_on is None:
            continue

        dependencies.append(
            {
                "initiative_id": depends_on.id,
                "name": depends_on.name,
                "status": depends_on.status,
                "priority": depends_on.priority,
                "dependency_type": dependency.dependency_type,
                "description": dependency.description,
                "dependencies": get_dependency_chain(
                    db=db,
                    initiative_id=depends_on.id,
                    visited=visited.copy(),
                ),
            }
        )

    return dependencies


# ============================================================
# PROCESS INTELLIGENCE
# ============================================================


@router.get("/{process_id}/intelligence")
def get_process_intelligence(
    process_id: int,
    db: Session = Depends(get_db),
):
    """
    Return the complete intelligence graph for a process.

    Process
        ├── Roles
        │     └── Skills
        │
        └── Activities
              └── AI Opportunities
                    ├── Evidence
                    ├── Governance
                    └── Transformation Initiatives
                          └── Dependencies
    """

    # --------------------------------------------------------
    # PROCESS
    # --------------------------------------------------------

    process = db.get(Process, process_id)

    if process is None:
        raise HTTPException(
            status_code=404,
            detail="Process not found",
        )

    # --------------------------------------------------------
    # ROLES + SKILLS
    # --------------------------------------------------------

    process_roles = (
        db.query(ProcessRole, Role)
        .join(
            Role,
            ProcessRole.role_id == Role.id,
        )
        .filter(
            ProcessRole.process_id == process.id
        )
        .all()
    )

    roles = []

    for process_role, role in process_roles:

        role_skills = []

        for role_skill in role.role_skills:

            skill = role_skill.skill

            role_skills.append(
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
                "skills": role_skills,
            }
        )

    # --------------------------------------------------------
    # ACTIVITIES
    # --------------------------------------------------------

    activities = (
        db.query(Activity)
        .filter(
            Activity.process_id == process.id
        )
        .order_by(Activity.sequence)
        .all()
    )

    activity_results = []

    for activity in activities:

        # ----------------------------------------------------
        # AI OPPORTUNITIES FOR ACTIVITY
        # ----------------------------------------------------

        opportunity_rows = (
            db.query(
                ActivityAIOpportunity,
                AIOpportunity,
            )
            .join(
                AIOpportunity,
                ActivityAIOpportunity.ai_opportunity_id
                == AIOpportunity.id,
            )
            .filter(
                ActivityAIOpportunity.activity_id
                == activity.id
            )
            .all()
        )

        opportunity_results = []

        for link, opportunity in opportunity_rows:

            # ------------------------------------------------
            # EVIDENCE
            # ------------------------------------------------

            evidence_rows = (
                db.query(Evidence)
                .filter(
                    Evidence.ai_opportunity_id
                    == opportunity.id
                )
                .all()
            )

            evidence = []

            for item in evidence_rows:

                evidence.append(
                    {
                        "id": item.id,
                        "claim": item.claim,
                        "excerpt": item.excerpt,
                        "relevance_score": item.relevance_score,
                        "confidence_score": item.confidence_score,
                        "source_id": item.source_id,
                    }
                )

            # ------------------------------------------------
            # GOVERNANCE
            # ------------------------------------------------

            governance = (
                db.query(GovernanceAssessment)
                .filter(
                    GovernanceAssessment.ai_opportunity_id
                    == opportunity.id
                )
                .first()
            )

            governance_data = None

            if governance is not None:

                governance_data = {
                    "id": governance.id,
                    "data_risk": governance.data_risk,
                    "privacy_risk": governance.privacy_risk,
                    "bias_risk": governance.bias_risk,
                    "oversight_requirement": (
                        governance.oversight_requirement
                    ),
                    "explainability_requirement": (
                        governance.explainability_requirement
                    ),
                    "security_risk": governance.security_risk,
                    "decision_impact": governance.decision_impact,
                    "regulatory_exposure": (
                        governance.regulatory_exposure
                    ),
                    "model_risk": governance.model_risk,
                    "monitoring_requirement": (
                        governance.monitoring_requirement
                    ),
                    "overall_risk": governance.overall_risk,
                    "reasoning": governance.reasoning,
                }

            # ------------------------------------------------
            # TRANSFORMATION INITIATIVES
            # ------------------------------------------------

            initiative_rows = (
                db.query(
                    AIOpportunityInitiative,
                    TransformationInitiative,
                )
                .join(
                    TransformationInitiative,
                    AIOpportunityInitiative.initiative_id
                    == TransformationInitiative.id,
                )
                .filter(
                    AIOpportunityInitiative.ai_opportunity_id
                    == opportunity.id
                )
                .all()
            )

            initiatives = []

            for (
                initiative_link,
                initiative,
            ) in initiative_rows:

                # --------------------------------------------
                # RECURSIVE DEPENDENCIES
                # --------------------------------------------

                dependencies = get_dependency_chain(
                    db=db,
                    initiative_id=initiative.id,
                )

                initiatives.append(
                    {
                        "id": initiative.id,
                        "name": initiative.name,
                        "description": initiative.description,
                        "status": initiative.status,
                        "priority": initiative.priority,
                        "expected_benefit": (
                            initiative.expected_benefit
                        ),
                        "relationship_type": (
                            initiative_link.relationship_type
                        ),
                        "dependencies": dependencies,
                    }
                )

            # ------------------------------------------------
            # COMPLETE AI OPPORTUNITY
            # ------------------------------------------------

            opportunity_results.append(
                {
                    "id": opportunity.id,
                    "name": opportunity.name,
                    "description": opportunity.description,
                    "ai_capability": opportunity.ai_capability,
                    "automation_potential": (
                        opportunity.automation_potential
                    ),
                    "human_involvement": (
                        opportunity.human_involvement
                    ),
                    "expected_benefit": (
                        opportunity.expected_benefit
                    ),
                    "feasibility": opportunity.feasibility,
                    "strategic_alignment": (
                        opportunity.strategic_alignment
                    ),
                    "risk_level": opportunity.risk_level,
                    "priority_score": (
                        opportunity.priority_score
                    ),
                    "reasoning": opportunity.reasoning,
                    "evidence": evidence,
                    "governance": governance_data,
                    "initiatives": initiatives,
                }
            )

        # ----------------------------------------------------
        # COMPLETE ACTIVITY
        # ----------------------------------------------------

        activity_results.append(
            {
                "id": activity.id,
                "name": activity.name,
                "description": activity.description,
                "sequence": activity.sequence,
                "activity_type": activity.activity_type,
                "decision_required": (
                    activity.decision_required
                ),
                "ai_opportunities": opportunity_results,
            }
        )

    # --------------------------------------------------------
    # FINAL RESPONSE
    # --------------------------------------------------------

    return {
        "process": {
            "id": process.id,
            "name": process.name,
            "description": process.description,
            "status": process.status,
            "priority_score": process.priority_score,
        },
        "roles": roles,
        "activities": activity_results,
    }
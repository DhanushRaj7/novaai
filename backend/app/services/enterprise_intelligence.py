from sqlalchemy.orm import Session

from app.models.process import Process
from app.models.ai_opportunity import AIOpportunity
from app.models.role import Role
from app.models.skill import Skill
from app.models.role_skill import RoleSkill
from app.models.initiative import TransformationInitiative
from app.models.initiative_dependency import InitiativeDependency


def get_dependency_chain(
    db: Session,
    initiative_id: int,
    visited: set[int] | None = None,
):
    """
    Recursively retrieve downstream transformation dependencies.
    """

    if visited is None:
        visited = set()

    if initiative_id in visited:
        return []

    visited.add(initiative_id)

    dependency_rows = (
        db.query(InitiativeDependency)
        .filter(
            InitiativeDependency.initiative_id == initiative_id
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


def get_enterprise_intelligence(db: Session):
    processes = db.query(Process).all()
    opportunities = db.query(AIOpportunity).all()
    roles = db.query(Role).all()
    skills = db.query(Skill).all()
    initiatives = db.query(TransformationInitiative).all()

    # =========================================================
    # ROLE ↔ SKILL RELATIONSHIPS
    # =========================================================

    role_skill_rows = db.query(RoleSkill).all()

    role_skill_map = {}
    skill_role_map = {}

    for row in role_skill_rows:
        role_skill_map.setdefault(
            row.role_id,
            [],
        ).append(row.skill_id)

        skill_role_map.setdefault(
            row.skill_id,
            [],
        ).append(row.role_id)

    # =========================================================
    # PROCESS INTELLIGENCE
    # =========================================================

    process_data = []

    for process in processes:
        process_opportunities = []

        for activity in process.activities:
            for link in activity.ai_opportunity_links:
                opportunity = link.ai_opportunity

                process_opportunities.append(
                    {
                        "id": opportunity.id,
                        "name": opportunity.name,
                        "priority_score": opportunity.priority_score,
                        "expected_benefit": opportunity.expected_benefit,
                        "feasibility": opportunity.feasibility,
                        "risk_level": opportunity.risk_level,
                    }
                )

        unique_opportunities = {
            opportunity["id"]: opportunity
            for opportunity in process_opportunities
        }

        process_data.append(
            {
                "id": process.id,
                "name": process.name,
                "description": process.description,
                "priority_score": process.priority_score,
                "ai_opportunities": list(
                    unique_opportunities.values()
                ),
            }
        )

    # =========================================================
    # AI OPPORTUNITIES
    # =========================================================

    opportunity_data = []

    for opportunity in opportunities:
        initiative_links = []

        for link in opportunity.initiative_links:
            initiative = link.initiative

            initiative_links.append(
                {
                    "id": initiative.id,
                    "name": initiative.name,
                    "priority": initiative.priority,
                    "status": initiative.status,
                    "relationship_type": link.relationship_type,
                }
            )

        opportunity_data.append(
            {
                "id": opportunity.id,
                "name": opportunity.name,
                "priority_score": opportunity.priority_score,
                "expected_benefit": opportunity.expected_benefit,
                "feasibility": opportunity.feasibility,
                "risk_level": opportunity.risk_level,
                "initiatives": initiative_links,
            }
        )

    # =========================================================
    # ROLES
    # =========================================================

    role_data = []

    for role in roles:
        role_skills = []

        for skill_id in role_skill_map.get(role.id, []):
            skill = db.get(Skill, skill_id)

            if skill:
                role_skills.append(
                    {
                        "id": skill.id,
                        "name": skill.name,
                    }
                )

        role_data.append(
            {
                "id": role.id,
                "name": role.name,
                "skills": role_skills,
            }
        )

    # =========================================================
    # SKILLS
    # =========================================================

    skill_data = []

    for skill in skills:
        skill_roles = []

        for role_id in skill_role_map.get(skill.id, []):
            role = db.get(Role, role_id)

            if role:
                skill_roles.append(
                    {
                        "id": role.id,
                        "name": role.name,
                    }
                )

        skill_data.append(
            {
                "id": skill.id,
                "name": skill.name,
                "roles": skill_roles,
            }
        )

    # =========================================================
    # TRANSFORMATION INITIATIVES
    # =========================================================

    initiative_data = []

    for initiative in initiatives:

        # ---------------------------------------------
        # Dependency chain
        # ---------------------------------------------

        dependencies = get_dependency_chain(
            db=db,
            initiative_id=initiative.id,
        )

        # ---------------------------------------------
        # AI opportunities supported by initiative
        # ---------------------------------------------

        supported_opportunities = []

        for link in initiative.opportunity_links:
            opportunity = link.ai_opportunity

            supported_opportunities.append(
                {
                    "id": opportunity.id,
                    "name": opportunity.name,
                    "priority_score": opportunity.priority_score,
                    "relationship_type": link.relationship_type,
                }
            )

        initiative_data.append(
            {
                "id": initiative.id,
                "name": initiative.name,
                "priority": initiative.priority,
                "status": initiative.status,
                "dependencies": dependencies,
                "ai_opportunities": supported_opportunities,
            }
        )

    # =========================================================
    # RANKINGS
    # =========================================================

    ranked_processes = sorted(
        process_data,
        key=lambda process: process["priority_score"] or 0,
        reverse=True,
    )

    ranked_opportunities = sorted(
        opportunity_data,
        key=lambda opportunity: opportunity["priority_score"] or 0,
        reverse=True,
    )

    ranked_initiatives = sorted(
        initiative_data,
        key=lambda initiative: initiative["priority"] or 0,
        reverse=True,
    )

    # =========================================================
    # RESPONSE
    # =========================================================

    return {
        "summary": {
            "process_count": len(processes),
            "ai_opportunity_count": len(opportunities),
            "role_count": len(roles),
            "skill_count": len(skills),
            "initiative_count": len(initiatives),
        },

        "processes": process_data,

        "ranked_processes": ranked_processes,

        "ai_opportunities": opportunity_data,

        "ranked_ai_opportunities": ranked_opportunities,

        "roles": role_data,

        "skills": skill_data,

        "initiatives": initiative_data,

        "ranked_initiatives": ranked_initiatives,
    }
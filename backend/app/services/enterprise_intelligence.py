from sqlalchemy.orm import Session

from app.models.process import Process
from app.models.ai_opportunity import AIOpportunity
from app.models.role import Role
from app.models.skill import Skill
from app.models.initiative import TransformationInitiative


def get_enterprise_intelligence(db: Session):
    processes = db.query(Process).all()
    opportunities = db.query(AIOpportunity).all()
    roles = db.query(Role).all()
    skills = db.query(Skill).all()
    initiatives = db.query(TransformationInitiative).all()

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
                    }
                )

        process_data.append(
            {
                "id": process.id,
                "name": process.name,
                "description": process.description,
                "priority_score": process.priority_score,
                "ai_opportunities": process_opportunities,
            }
        )

    opportunity_data = [
        {
            "id": opportunity.id,
            "name": opportunity.name,
            "priority_score": opportunity.priority_score,
            "expected_benefit": opportunity.expected_benefit,
            "feasibility": opportunity.feasibility,
            "risk_level": opportunity.risk_level,
        }
        for opportunity in opportunities
    ]

    role_data = [
        {
            "id": role.id,
            "name": role.name,
        }
        for role in roles
    ]

    skill_data = [
        {
            "id": skill.id,
            "name": skill.name,
        }
        for skill in skills
    ]

    initiative_data = [
        {
            "id": initiative.id,
            "name": initiative.name,
            "priority": initiative.priority,
            "status": initiative.status,
        }
        for initiative in initiatives
    ]

    return {
        "summary": {
            "process_count": len(processes),
            "ai_opportunity_count": len(opportunities),
            "role_count": len(roles),
            "skill_count": len(skills),
            "initiative_count": len(initiatives),
        },
        "processes": process_data,
        "ai_opportunities": opportunity_data,
        "roles": role_data,
        "skills": skill_data,
        "initiatives": initiative_data,
    }
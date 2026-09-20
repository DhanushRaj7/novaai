from sqlalchemy import select

from app.db.database import SessionLocal
from app.models.organisation import Organisation
from app.models.role import Role
from app.models.skill import Skill
from app.models.role_skill import RoleSkill


ROLES = [
    {
        "name": "Credit Analyst",
        "description": "Evaluates customer creditworthiness and prepares credit assessments.",
    },
    {
        "name": "Loan Officer",
        "description": "Manages lending applications, customer interactions, and loan decisions.",
    },
    {
        "name": "Customer Service Representative",
        "description": "Handles customer requests, service issues, and account-related inquiries.",
    },
    {
        "name": "Risk Analyst",
        "description": "Analyzes financial and operational risks and supports risk decisions.",
    },
    {
        "name": "Compliance Officer",
        "description": "Ensures banking processes comply with regulatory and internal requirements.",
    },
    {
        "name": "Fraud Analyst",
        "description": "Investigates suspicious transactions and identifies potential fraud.",
    },
    {
        "name": "Data Scientist",
        "description": "Builds analytical and machine-learning solutions for business problems.",
    },
    {
        "name": "AI Product Manager",
        "description": "Leads the design, prioritization, and adoption of AI-enabled products.",
    },
]


SKILLS = [
    {
        "name": "Credit Risk Analysis",
        "category": "Domain",
        "description": "Ability to assess borrower creditworthiness and lending risk.",
    },
    {
        "name": "Financial Analysis",
        "category": "Domain",
        "description": "Ability to interpret financial information and assess financial conditions.",
    },
    {
        "name": "Regulatory Compliance",
        "category": "Governance",
        "description": "Understanding of banking regulations, controls, and compliance requirements.",
    },
    {
        "name": "Fraud Detection",
        "category": "Domain",
        "description": "Ability to identify suspicious patterns and potential fraudulent activity.",
    },
    {
        "name": "Customer Service",
        "category": "Business",
        "description": "Ability to understand and resolve customer requests effectively.",
    },
    {
        "name": "Data Analysis",
        "category": "Technical",
        "description": "Ability to analyze structured and unstructured business data.",
    },
    {
        "name": "Machine Learning",
        "category": "AI",
        "description": "Ability to develop and evaluate machine-learning models.",
    },
    {
        "name": "AI Literacy",
        "category": "AI",
        "description": "Understanding of AI capabilities, limitations, and appropriate business use.",
    },
    {
        "name": "Document Intelligence",
        "category": "AI",
        "description": "Ability to work with AI systems that extract and interpret information from documents.",
    },
    {
        "name": "Risk Management",
        "category": "Governance",
        "description": "Ability to identify, assess, and manage business and operational risks.",
    },
    {
        "name": "Data Governance",
        "category": "Governance",
        "description": "Understanding of data quality, ownership, privacy, and governance practices.",
    },
    {
        "name": "AI Product Management",
        "category": "Business",
        "description": "Ability to define, prioritize, and manage AI-enabled products and capabilities.",
    },
]


ROLE_SKILLS = {
    "Credit Analyst": [
        ("Credit Risk Analysis", 0.95),
        ("Financial Analysis", 0.90),
        ("Document Intelligence", 0.75),
        ("AI Literacy", 0.55),
    ],
    "Loan Officer": [
        ("Financial Analysis", 0.80),
        ("Customer Service", 0.90),
        ("Credit Risk Analysis", 0.75),
        ("AI Literacy", 0.60),
    ],
    "Customer Service Representative": [
        ("Customer Service", 0.95),
        ("AI Literacy", 0.70),
        ("Document Intelligence", 0.55),
    ],
    "Risk Analyst": [
        ("Risk Management", 0.95),
        ("Data Analysis", 0.90),
        ("Financial Analysis", 0.80),
        ("AI Literacy", 0.70),
        ("Machine Learning", 0.55),
    ],
    "Compliance Officer": [
        ("Regulatory Compliance", 0.95),
        ("Risk Management", 0.85),
        ("Data Governance", 0.80),
        ("AI Literacy", 0.65),
    ],
    "Fraud Analyst": [
        ("Fraud Detection", 0.95),
        ("Data Analysis", 0.90),
        ("Risk Management", 0.80),
        ("AI Literacy", 0.70),
        ("Machine Learning", 0.55),
    ],
    "Data Scientist": [
        ("Data Analysis", 0.95),
        ("Machine Learning", 0.95),
        ("AI Literacy", 0.95),
        ("Data Governance", 0.70),
    ],
    "AI Product Manager": [
        ("AI Product Management", 0.95),
        ("AI Literacy", 0.95),
        ("Data Governance", 0.75),
        ("Risk Management", 0.70),
        ("Customer Service", 0.55),
    ],
}


def seed_roles_and_skills():
    db = SessionLocal()

    try:
        organisation = db.execute(
            select(Organisation).where(
                Organisation.name == "NovaBank"
            )
        ).scalar_one_or_none()

        if organisation is None:
            raise ValueError("NovaBank organisation not found.")

        skill_map = {}

        # Create skills
        for skill_data in SKILLS:
            skill = db.execute(
                select(Skill).where(
                    Skill.name == skill_data["name"]
                )
            ).scalar_one_or_none()

            if skill is None:
                skill = Skill(**skill_data)
                db.add(skill)
                db.flush()

            skill_map[skill.name] = skill

        # Create roles and relationships
        for role_data in ROLES:
            role = db.execute(
                select(Role).where(
                    Role.organisation_id == organisation.id,
                    Role.name == role_data["name"],
                )
            ).scalar_one_or_none()

            if role is None:
                role = Role(
                    organisation_id=organisation.id,
                    **role_data,
                )
                db.add(role)
                db.flush()

            for skill_name, importance in ROLE_SKILLS[role.name]:
                skill = skill_map[skill_name]

                existing = db.execute(
                    select(RoleSkill).where(
                        RoleSkill.role_id == role.id,
                        RoleSkill.skill_id == skill.id,
                    )
                ).scalar_one_or_none()

                if existing is None:
                    db.add(
                        RoleSkill(
                            role_id=role.id,
                            skill_id=skill.id,
                            importance=importance,
                            skill_status="current",
                        )
                    )

        db.commit()

        print("Roles and skills seeded successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles_and_skills()
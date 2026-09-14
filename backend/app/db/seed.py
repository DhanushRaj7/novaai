from app.db.database import SessionLocal
from app.models.organisation import Organisation
from app.models.strategy import Strategy
from app.models.value_chain import ValueChainStage


def seed():
    db = SessionLocal()

    try:
        organisation = db.query(Organisation).filter_by(
            name="NovaBank"
        ).first()

        if organisation is None:
            organisation = Organisation(
                name="NovaBank",
                industry="Banking",
                description=(
                    "A fictional retail and commercial bank "
                    "transforming into an AI-first organisation."
                ),
            )
            db.add(organisation)
            db.flush()

        strategy = db.query(Strategy).filter_by(
            organisation_id=organisation.id,
            name="AI-First Banking Transformation",
        ).first()

        if strategy is None:
            strategy = Strategy(
                organisation_id=organisation.id,
                name="AI-First Banking Transformation",
                objective=(
                    "Transform NovaBank into an AI-first bank "
                    "over a three-year horizon."
                ),
                description=(
                    "Use AI to improve customer experience, "
                    "operational efficiency, decision-making, "
                    "and employee capabilities."
                ),
                time_horizon="3 years",
            )
            db.add(strategy)

        stages = [
            ("Customer Acquisition", "Acquire and onboard customers.", 1),
            ("Customer Service", "Serve and support customers.", 2),
            ("Lending", "Originate and manage lending products.", 3),
            ("Payments", "Process and manage customer payments.", 4),
            ("Risk & Compliance", "Manage financial and regulatory risk.", 5),
        ]

        for name, description, sequence in stages:
            exists = db.query(ValueChainStage).filter_by(
                organisation_id=organisation.id,
                name=name,
            ).first()

            if exists is None:
                db.add(
                    ValueChainStage(
                        organisation_id=organisation.id,
                        name=name,
                        description=description,
                        sequence=sequence,
                    )
                )

        db.commit()

        print("NovaBank seed data created successfully.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed()
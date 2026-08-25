from sqlalchemy import select
from backend.app.db import Base, SessionLocal, engine
from backend.app.models import Environment, FeatureFlag, Project


def seed():
    Base.metadata.create_all(bind=engine)

    with SessionLocal() as db:
        if db.scalar(select(Project).where(Project.key == "demo")):
            print("Demo project already exists.")
            return

        project = Project(key="demo", name="Demo Project", description="Seeded V1 project")
        db.add(project)
        db.flush()

        production = Environment(project_id=project.id, key="production", name="Production")
        staging = Environment(project_id=project.id, key="staging", name="Staging")
        db.add_all([production, staging])
        db.flush()

        db.add_all([
            FeatureFlag(
                environment_id=production.id,
                key="new_checkout",
                name="New Checkout",
                description="25% rollout",
                enabled=True,
                premium_only=False,
                rollout_percentage=25,
                targeting_rules=[],
            ),
            FeatureFlag(
                environment_id=production.id,
                key="premium_dashboard",
                name="Premium Dashboard",
                description="Premium-only feature",
                enabled=True,
                premium_only=True,
                rollout_percentage=100,
                targeting_rules=[],
            ),
            FeatureFlag(
                environment_id=staging.id,
                key="us_search",
                name="US Search",
                description="US targeting example",
                enabled=True,
                premium_only=False,
                rollout_percentage=100,
                targeting_rules=[{"attribute": "country", "operator": "equals", "value": "US"}],
            ),
        ])

        db.commit()
    print("Seed complete.")


if __name__ == "__main__":
    seed()

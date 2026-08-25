from sqlalchemy import select
from sqlalchemy.orm import Session
from . import models, schemas


def list_projects(db: Session):
    return list(db.scalars(select(models.Project).order_by(models.Project.id)).all())


def get_project(db: Session, project_id: int):
    return db.get(models.Project, project_id)


def create_project(db: Session, data: schemas.ProjectCreate):
    obj = models.Project(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_environments(db: Session, project_id: int):
    stmt = select(models.Environment).where(models.Environment.project_id == project_id).order_by(models.Environment.id)
    return list(db.scalars(stmt).all())


def create_environment(db: Session, project_id: int, data: schemas.EnvironmentCreate):
    obj = models.Environment(project_id=project_id, **data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_flags(db: Session, environment_id: int):
    stmt = select(models.FeatureFlag).where(models.FeatureFlag.environment_id == environment_id).order_by(models.FeatureFlag.id)
    return list(db.scalars(stmt).all())


def get_flag(db: Session, flag_id: int):
    return db.get(models.FeatureFlag, flag_id)


def get_flag_by_keys(db: Session, project_key: str, environment_key: str, flag_key: str):
    stmt = (
        select(models.FeatureFlag)
        .join(models.Environment)
        .join(models.Project)
        .where(
            models.Project.key == project_key,
            models.Environment.key == environment_key,
            models.FeatureFlag.key == flag_key,
        )
    )
    return db.scalar(stmt)


def create_flag(db: Session, environment_id: int, data: schemas.FlagCreate):
    payload = data.model_dump()
    payload["targeting_rules"] = [r.model_dump() for r in data.targeting_rules]
    obj = models.FeatureFlag(environment_id=environment_id, **payload)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def update_flag(db: Session, flag: models.FeatureFlag, data: schemas.FlagUpdate):
    changes = data.model_dump(exclude_unset=True)
    if "targeting_rules" in changes and changes["targeting_rules"] is not None:
        changes["targeting_rules"] = [
            r.model_dump() if hasattr(r, "model_dump") else r for r in changes["targeting_rules"]
        ]
    for key, value in changes.items():
        setattr(flag, key, value)
    flag.version += 1
    db.add(flag)
    db.commit()
    db.refresh(flag)
    return flag


def delete_flag(db: Session, flag: models.FeatureFlag):
    db.delete(flag)
    db.commit()


def add_audit(db: Session, actor: str, action: str, entity_type: str, entity_id: str, payload: dict):
    obj = models.AuditEvent(
        actor=actor,
        action=action,
        entity_type=entity_type,
        entity_id=str(entity_id),
        payload=payload,
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def list_audit(db: Session, limit: int):
    stmt = select(models.AuditEvent).order_by(models.AuditEvent.id.desc()).limit(limit)
    return list(db.scalars(stmt).all())

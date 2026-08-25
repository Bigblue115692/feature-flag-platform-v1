from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import repositories as repo, schemas
from .db import get_db
from .evaluation import evaluate_flag
from .security import require_admin_key, require_sdk_key

router = APIRouter(prefix="/api")


@router.get("/projects", response_model=list[schemas.ProjectRead])
def list_projects(db: Session = Depends(get_db), _: str = Depends(require_admin_key)):
    return repo.list_projects(db)


@router.post("/projects", response_model=schemas.ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(data: schemas.ProjectCreate, db: Session = Depends(get_db), actor: str = Depends(require_admin_key)):
    try:
        obj = repo.create_project(db, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Project key already exists")
    repo.add_audit(db, actor, "project.created", "project", obj.id, data.model_dump())
    return obj


@router.get("/projects/{project_id}/environments", response_model=list[schemas.EnvironmentRead])
def list_environments(project_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin_key)):
    if not repo.get_project(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return repo.list_environments(db, project_id)


@router.post("/projects/{project_id}/environments", response_model=schemas.EnvironmentRead, status_code=201)
def create_environment(project_id: int, data: schemas.EnvironmentCreate, db: Session = Depends(get_db), actor: str = Depends(require_admin_key)):
    if not repo.get_project(db, project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    try:
        obj = repo.create_environment(db, project_id, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Environment key already exists")
    repo.add_audit(db, actor, "environment.created", "environment", obj.id, data.model_dump())
    return obj


@router.get("/environments/{environment_id}/flags", response_model=list[schemas.FlagRead])
def list_flags(environment_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin_key)):
    return repo.list_flags(db, environment_id)


@router.post("/environments/{environment_id}/flags", response_model=schemas.FlagRead, status_code=201)
def create_flag(environment_id: int, data: schemas.FlagCreate, db: Session = Depends(get_db), actor: str = Depends(require_admin_key)):
    try:
        obj = repo.create_flag(db, environment_id, data)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Flag key already exists")
    repo.add_audit(db, actor, "flag.created", "flag", obj.id, data.model_dump(mode="json"))
    return obj


@router.get("/flags/{flag_id}", response_model=schemas.FlagRead)
def get_flag(flag_id: int, db: Session = Depends(get_db), _: str = Depends(require_admin_key)):
    obj = repo.get_flag(db, flag_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Flag not found")
    return obj


@router.put("/flags/{flag_id}", response_model=schemas.FlagRead)
def update_flag(flag_id: int, data: schemas.FlagUpdate, db: Session = Depends(get_db), actor: str = Depends(require_admin_key)):
    obj = repo.get_flag(db, flag_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Flag not found")
    updated = repo.update_flag(db, obj, data)
    repo.add_audit(db, actor, "flag.updated", "flag", flag_id, data.model_dump(exclude_unset=True, mode="json"))
    return updated


@router.delete("/flags/{flag_id}", status_code=204)
def delete_flag(flag_id: int, db: Session = Depends(get_db), actor: str = Depends(require_admin_key)):
    obj = repo.get_flag(db, flag_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Flag not found")
    payload = {"key": obj.key, "name": obj.name}
    repo.delete_flag(db, obj)
    repo.add_audit(db, actor, "flag.deleted", "flag", flag_id, payload)


@router.post("/evaluate", response_model=schemas.EvaluationResponse)
def evaluate(request: schemas.EvaluationRequest, db: Session = Depends(get_db), _: str = Depends(require_sdk_key)):
    flag = repo.get_flag_by_keys(db, request.project_key, request.environment_key, request.flag_key)
    if not flag:
        return schemas.EvaluationResponse(flag_key=request.flag_key, enabled=False, reason="flag_not_found")
    return evaluate_flag(request.project_key, request.environment_key, flag, request.user)


@router.get("/audit", response_model=list[schemas.AuditRead])
def list_audit(limit: int = Query(default=100, ge=1, le=500), db: Session = Depends(get_db), _: str = Depends(require_admin_key)):
    return repo.list_audit(db, limit)

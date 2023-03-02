from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import model, forms, crud, database
from .database import the_project, get_db, app_cfg, app_config_path


router = APIRouter(prefix='/api', tags=['api'])


@router.get('/all-projects', response_model=list[forms.Project])
def get_all_projects():
    projects = []
    for pj in app_cfg['projects'].values():
        in_use = pj['id'] == app_cfg['default_project']
        pj['in_use'] = in_use
        projects.append(pj)
    return projects


@router.post('/add-project', response_model=forms.Project)
def add_project(project: forms.ProjectCreate):
    project, err = database.add_project(**project.dict())
    if err:
        raise HTTPException(status_code=400, detail=err)
    return project


@router.get('/all-buckets', response_model=list[forms.Bucket])
def get_all_buckets(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if not app_cfg['default_project']:
        raise HTTPException(status_code=404, detail='尚未添加項目')
    return crud.get_all_buckets(db, skip=skip, limit=limit)

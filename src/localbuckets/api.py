from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import model, forms, crud
from .database import init_the_project, the_project, get_db, app_cfg


init_the_project()

router = APIRouter(prefix='/api', tags=['api'])


@router.get('/all-buckets', response_model=list[forms.Bucket])
def get_all_buckets(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if not app_cfg['default_project']:
        raise HTTPException(status_code=404, detail='尚未添加項目')
    return crud.get_all_buckets(db, skip=skip, limit=limit)

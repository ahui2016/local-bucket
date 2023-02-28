from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from . import model, forms, crud
from .database import the_project, get_db


router = APIRouter(prefix='/api', tags=['api'])


@router.get('/all-buckets', response_model=list[forms.Bucket])
def get_all_buckets(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    if the_project['session'] is None:
        raise HTTPException(status_code=404, detail='尚未添加項目')
    return crud.get_all_buckets(db, skip=skip, limit=limit)

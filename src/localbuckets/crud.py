from pathlib import Path
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import model, forms
from .database import ErrMsg, the_project, check_filename


def get_all_buckets(
        db: Session, skip: int = 0, limit: int = 100
) -> Sequence[model.Bucket]:
    return db.scalars(
        select(model.Bucket)
        .order_by(model.Bucket.id)
        .offset(skip)
        .limit(limit)
    ).all()


def create_bucket(
        db: Session, bucket: forms.BucketCreate
) -> (model.Bucket, ErrMsg):
    if err := check_filename(bucket.folder_name):
        return None, err

    if not bucket.title:
        bucket.title = bucket.folder_name

    project_path = Path(the_project['path'])
    bucket_path = project_path.joinpath(bucket.folder_name)
    if bucket_path.exists():
        return None, f'倉庫已存在, 請勿重複添加: {bucket.folder_name}'

    db.add(bucket)
    db.commit()

    bucket_path.mkdir(exist_ok=True)
    return bucket, None

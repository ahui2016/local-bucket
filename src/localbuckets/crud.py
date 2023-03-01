from pathlib import Path
from typing import Sequence

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import model, forms
from .database import the_project


def get_all_buckets(
        db: Session, skip: int = 0, limit: int = 100
) -> Sequence[model.Bucket]:
    return db.scalars(
        select(model.Bucket)
        .order_by(model.Bucket.id)
        .offset(skip)
        .limit(limit)
    ).all()


'''
def create_bucket(db: Session, bucket: forms.BucketCreate) -> model.Bucket:
    bucket_path = the_project['path'].joinpath(bucket.folder_name)
    if not bucket.title:
        bucket.title = bucket.folder_name
    return bucket
'''

from pydantic import BaseModel


class BucketBase(BaseModel):
    id: int


class BucketCreate(BucketBase):
    pass


class Bucket(BucketBase):
    pass

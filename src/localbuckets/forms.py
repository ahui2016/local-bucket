from pydantic import BaseModel


class BucketBase(BaseModel):
    folder_name: str
    title: str = ''
    subtitle: str = ''


class BucketCreate(BucketBase):
    pass


class Bucket(BucketBase):
    id: int

    class Config:
        orm_moe = True

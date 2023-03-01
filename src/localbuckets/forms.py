from pydantic import BaseModel


class ProjectBase(BaseModel):
    path: str
    title: str = ''
    subtitle: str = ''


class ProjectCreate(ProjectBase):
    pass


class Project(ProjectBase):
    id: str

    class Config:
        orm_mode = True


class BucketBase(BaseModel):
    folder_name: str
    title: str = ''
    subtitle: str = ''


class BucketCreate(BucketBase):
    pass


class Bucket(BucketBase):
    id: int

    class Config:
        orm_mode = True

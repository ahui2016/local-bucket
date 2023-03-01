import hashlib
import json
import os
from pathlib import Path
from typing import TypedDict, TypeAlias

from platformdirs import user_data_path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


hash_md5 = hashlib.md5()

app_name = 'local-buckets'
app_db_filename = 'localbuckets.db'
app_data_path: Path = user_data_path(app_name, 'github-ahui2016')
app_data_path.mkdir(parents=True, exist_ok=True)
app_config_path = app_data_path.joinpath(app_name + '.json')


ErrMsg: TypeAlias = str | None
"""空字符串或 None 表示無錯誤, 有內容表示有錯誤."""


class Base(DeclarativeBase):
    pass


class Project(TypedDict):
    # 項目文件夾路徑轉 md5
    id: str

    # 項目文件夾路徑 (絕對路徑)
    # 文件夾名只能使用 0-9, a-z, A-Z, _(下劃線), -(連字號), .(點)
    path: str

    # 項目標題和副標題, 可使用任何語言任意字符
    title: str
    subtitle: str


# projects: {id: project}
# default_project: project.id
class AppConfig(TypedDict):
    projects: dict[str, Project]
    default_project: str


app_default_cfg = AppConfig(
    projects=dict(),
    default_project=''
)
app_cfg: AppConfig = app_default_cfg


def write_app_cfg(cfg: AppConfig):
    app_config_path.write_text(json.dumps(cfg))


if app_config_path.exists():
    app_cfg = json.loads(app_config_path.read_text())
else:
    write_app_cfg(app_default_cfg)

the_project = dict(
    # path: Path,
    # engine,
    # session
)


# https://fastapi.tiangolo.com/tutorial/sql-databases/
# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
def get_db():
    db = the_project.get('session', None)
    if db:
        db = db()
    try:
        yield db
    finally:
        if db:
            db.close()


def md5_hex(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    hash_md5.update(data)
    return hash_md5.hexdigest()


def set_db_engine(project_path: str | Path):
    project_path = Path(project_path)
    db_file = project_path.joinpath(app_db_filename)
    db_url = f'sqlite:///{db_file}'
    the_project['path'] = project_path
    the_project['engine'] = create_engine(db_url, connect_args={'check_same_thread': False})
    the_project['session'] = sessionmaker(autoflush=False, bind=the_project['engine'])
    Base.metadata.create_all(bind=the_project['engine'])


def new_project(path: str | Path) -> dict:
    if isinstance(path, Path):
        path = str(path)

    return Project(
        id=md5_hex(path),
        path=path,
        title='',
        subtitle=''
    )


def init_the_project():
    project_id = app_cfg['default_project']
    if project_id:
        project = app_cfg['projects'][project_id]
        set_db_engine(project['path'])


def add_project(path: str | Path) -> (Project, ErrMsg):
    path = Path(path).resolve()
    path_str = str(path)
    project_id = md5_hex(path_str)
    if project_id in app_cfg['projects']:
        return {}, f'項目已存在, 請勿重複添加: {path_str}'

    if not path.exists():
        return {}, f'PathNotExist(文件夾不存在): {path_str}'

    if dir_not_empty(path):
        db_file = path.joinpath(app_db_filename)
        if not db_file.exists():
            return {}, f'不是空文件夾, 也沒有 {app_db_filename}: {path}'

    set_db_engine(path)
    project = new_project(path)
    app_cfg['projects'][project_id] = project
    app_cfg['default_project'] = project_id
    write_app_cfg(app_cfg)
    return project, None


def dir_not_empty(path):
    return True if os.listdir(path) else False

import hashlib
import json
from pathlib import Path
from typing import TypedDict

from platformdirs import user_data_path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


hash_md5 = hashlib.md5()

app_name = 'local-buckets'
app_db_filename = 'localbuckets.db'
app_data_path: Path = user_data_path(app_name, 'github-ahui2016')
app_data_path.mkdir(parents=True, exist_ok=True)
app_config_path = app_data_path.joinpath(app_name + '.json')


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

if app_config_path.exists():
    app_cfg = json.loads(app_config_path.read_text())
else:
    app_config_path.write_text(json.dumps(app_default_cfg))


the_project = dict(
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
    db_file = Path(project_path).joinpath(app_db_filename)
    the_project['engine'] = create_engine(str(db_file), connect_args={'check_same_thread': False})
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

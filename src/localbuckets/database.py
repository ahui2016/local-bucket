import hashlib
import json
from pathlib import Path

from platformdirs import user_data_path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

app_name = 'local-buckets'
app_db_filename = 'localbuckets.db'
app_data_path: Path = user_data_path(app_name, 'github-ahui2016')
app_data_path.mkdir(parents=True, exist_ok=True)
app_config_path = app_data_path.joinpath(app_name + '.json')

# projects: dict[str, dict], {id: project}, id == project.id
app_default_cfg = dict(
    projects=dict()
)
app_cfg = app_default_cfg

if app_config_path.exists():
    app_cfg = json.loads(app_config_path.read_text())
else:
    app_config_path.write_text(json.dumps(app_default_cfg))



class Base(DeclarativeBase):
    pass


the_project = dict(
    engine=None,
    session=None
)


def set_db_engine(db_file: str):
    the_project.engine = create_engine(db_file, connect_args={'check_same_thread': False})
    the_project.session = sessionmaker(autoflush=False, bind=the_project.engine)
    Base.metadata.create_all(bind=the_project.engine)


# https://fastapi.tiangolo.com/tutorial/sql-databases/
# https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/
def get_db():
    # db 可能是 None, 也可能是 sessionmaker
    db = the_project['session']
    if db:
        db = db()
    try:
        yield db
    finally:
        if db:
            db.close()


hash_md5 = hashlib.md5()


def md5_hex(data: str | bytes) -> str:
    if isinstance(data, str):
        data = data.encode()
    hash_md5.update(data)
    return hash_md5.hexdigest()


def new_project(path: str | Path) -> dict:
    if isinstance(path, Path):
        path = str(path)

    return dict(
        # 項目文件夾路徑轉 md5
        id=md5_hex(path),

        # 項目文件夾路徑 (絕對路徑)
        # 文件夾名只能使用 0-9, a-z, A-Z, _(下劃線), -(連字號), .(點)
        path=path,

        # 項目標題和副標題, 可使用任何語言任意字符
        title='',
        subtitle=''
    )

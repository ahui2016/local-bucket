import hashlib
import json
from pathlib import Path

from platformdirs import user_data_path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

app_name = 'local-buckets'
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

hash_md5 = hashlib.md5()


def md5_hex(data: bytes) -> str:
    hash_md5.update(data)
    return hash_md5.hexdigest()


def new_project(path: Path) -> dict:
    return dict(
        # 項目文件夾路徑轉 md5
        id=md5_hex(str(path).encode()),

        # 項目文件夾路徑 (絕對路徑)
        # 注意項目文件夾名只能使用 0-9, a-z, A-Z, _(下劃線), -(連字號), .(點)
        path=str(path),

        # 項目名稱, 可使用任何語言任意字符
        name=''
    )


class Base(DeclarativeBase):
    pass

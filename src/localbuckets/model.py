from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Projects(Base):
    __tablename__ = 'projects'

    # 自增ID
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 項目文件夾路徑 (絕對路徑)
    # 注意項目文件夾名只能使用 0-9, a-z, A-Z, _(下劃線), -(連字號), .(點)
    path: Mapped[str]

    # 項目名稱, 可使用任何語言任意字符
    name: Mapped[str]

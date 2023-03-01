from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Bucket(Base):
    __tablename__ = 'bucket'

    # 自增ID
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # 倉庫文件夾名
    # 文件夾名只能使用 0-9, a-z, A-Z, _(下劃線), -(連字號), .(點)
    folder_name: Mapped[str]

    # 倉庫標題和副標題, 可使用任何語言任意字符
    title: Mapped[str] = '',
    subtitle: Mapped[str] = ''

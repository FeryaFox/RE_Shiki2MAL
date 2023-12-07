from .base import Base
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Paths(Base):
    __tablename__ = 'paths'
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str] = mapped_column(String())
    source_name: Mapped[str] = mapped_column(String())
    target: Mapped[str] = mapped_column(String())
    target_name: Mapped[str] = mapped_column(String())
    is_active: Mapped[bool] = mapped_column(Boolean())

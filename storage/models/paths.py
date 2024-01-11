from .base import Base
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Paths(Base):
    __tablename__ = 'paths'
    id: Mapped[int] = mapped_column(primary_key=True)
    source: Mapped[str]
    source_name: Mapped[str]
    target: Mapped[str]
    target_name: Mapped[str]
    is_active: Mapped[bool]

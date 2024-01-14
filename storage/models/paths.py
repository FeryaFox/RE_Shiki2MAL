from .base import Base
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from wrappers.enums import PathStatus

class Path(Base):
    __tablename__ = 'path'
    id: Mapped[int] = mapped_column(primary_key=True)
    source_wrapper_id: Mapped[int] = mapped_column(ForeignKey('wrapper.id'))
    source_username: Mapped[str]
    target_wrapper_id: Mapped[int] = mapped_column(ForeignKey('wrapper.id'))
    target_username: Mapped[str]
    status: Mapped[PathStatus]

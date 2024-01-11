from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import ForeignKey
from .base import Base
from wrappers.enums import WrapperTypes, WrapperStatuses


class Wrappers(Base):
    __tablename__ = 'wrappers'

    id: Mapped[int] = mapped_column(primary_key=True)
    wrapper_name: Mapped[str]
    wrapper_type: Mapped[WrapperTypes]
    status: Mapped[WrapperTypes]


class SourceData(Base):
    __tablename__ = "source_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    wrapper_id: Mapped[int] = mapped_column(ForeignKey("wrappers.id"))
    key: Mapped[str]
    data: Mapped[str]


class SourceConfig(Base):
    __tablename__ = "source_config"

    id: Mapped[int] = mapped_column(primary_key=True)
    wrapper_id: Mapped[int] = mapped_column(ForeignKey("wrappers.id"))
    key: Mapped[str]
    data: Mapped[str]


class TargetData(Base):
    __tablename__ = "target_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    wrapper_id: Mapped[int] = mapped_column(ForeignKey("wrappers.id"))
    key: Mapped[str]
    data: Mapped[str]


class TargetConfig(Base):
    __tablename__ = "target_config"
    id: Mapped[int] = mapped_column(primary_key=True)
    wrapper_id: Mapped[int] = mapped_column(ForeignKey("wrappers.id"))
    key: Mapped[str]
    data: Mapped[str]

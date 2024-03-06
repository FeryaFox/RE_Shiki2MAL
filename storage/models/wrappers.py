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
    wrapper_status: Mapped[WrapperStatuses]


class WrappersData(Base):
    __tablename__ = "wrappers_data"

    id: Mapped[int] = mapped_column(primary_key=True)
    wrapper_id: Mapped[int] = mapped_column(ForeignKey("wrappers.id"))
    key: Mapped[str]
    value: Mapped[str]


class WrappersConfig(Base):
    __tablename__ = "wrappers_config"

    id: Mapped[int] = mapped_column(primary_key=True)
    wrapper_id: Mapped[int] = mapped_column(ForeignKey("wrappers.id"))
    key: Mapped[str]
    value: Mapped[str]

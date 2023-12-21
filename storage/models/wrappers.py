from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .base import Base


class WrapperToken(Base):
    __tablename__ = 'wrapper_token'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    key: Mapped[str] = mapped_column(String())
    data: Mapped[str] = mapped_column(String())


class WrapperInfo(Base):
    __tablename__ = 'wrapper_info'
    id: Mapped[int] = mapped_column(primary_key=True)
    wrappers: Mapped[str] = mapped_column(String())
    status: Mapped[int] = mapped_column()


class SourceData(Base):
    __tablename__ = "source_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    key: Mapped[str] = mapped_column(String())
    data: Mapped[str] = mapped_column(String())


class SourceConfig(Base):
    __tablename__ = "source_config"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    key: Mapped[str] = mapped_column(String())
    data: Mapped[str] = mapped_column(String())


class TargetData(Base):
    __tablename__ = "target_data"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    key: Mapped[str] = mapped_column(String())
    data: Mapped[str] = mapped_column(String())


class TargetConfig(Base):
    __tablename__ = "target_config"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    key: Mapped[str] = mapped_column(String())
    data: Mapped[str] = mapped_column(String())

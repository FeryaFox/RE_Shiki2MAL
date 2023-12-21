from sqlalchemy import Engine

from .base import BaseWrapperStorage


class WrapperSourceStorage(BaseWrapperStorage):
    ...


class WrapperTargetStorage(BaseWrapperStorage):
    ...


class WrapperConfigStorage:
    def __init__(self, engine: Engine):
        self.__engine = engine

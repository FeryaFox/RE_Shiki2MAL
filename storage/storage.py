from sqlalchemy import create_engine
from .models.base import Base
from .storages.path import PathStorage
from .storages.wrappers import WrapperSourceStorage, WrapperTargetStorage, WrapperConfigStorage
from .models.wrappers import Wrappers
from sqlalchemy.schema import MetaData
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.engine import Engine


class Storage:
    def __init__(self, db_name: str = "RE_Shiki2MAL.db"):
        self.__engine = create_engine(f'sqlite:///{db_name}', echo=True)
        Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(self.__engine)

    def create_wrapper_source_storage(self, wrapper_name: str) -> WrapperSourceStorage:
        return WrapperSourceStorage(wrapper_name, self.__engine)

    def create_wrapper_target_storage(self, wrapper_name: str) -> WrapperTargetStorage:
        return WrapperTargetStorage(wrapper_name, self.__engine)

    def create_wrapper_config_storage(self) -> WrapperConfigStorage:
        return WrapperConfigStorage(self.__engine)

    def create_path_storage(self) -> PathStorage:
        return PathStorage(self.__engine)

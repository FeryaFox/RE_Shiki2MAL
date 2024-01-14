from sqlalchemy import create_engine
from .models.base import Base
# from storage.storages.paths.path import PathStorage
from .storages.WrapperStorage import WrapperStorage
from sqlalchemy.orm import sessionmaker
from wrappers.enums import WrapperTypes


class StorageController:
    def __init__(self, db_name: str = "RE_Shiki2MAL.db"):
        self.__engine = create_engine(f'sqlite:///{db_name}', echo=True)
        # self.__engine = create_engine(f'sqlite:///{db_name}')
        Base.metadata.create_all(self.__engine)
        self.__session = sessionmaker(self.__engine)

    def create_wrapper_source_storage(self, wrapper_name: str) -> WrapperStorage:
        return WrapperStorage(wrapper_name, self.__session, WrapperTypes.Source)

    def create_wrapper_target_storage(self, wrapper_name: str) -> WrapperStorage:
        return WrapperStorage(wrapper_name, self.__session, WrapperTypes.Target)

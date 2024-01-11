from .BaseWrapperStorage import BaseWrapperStorage
from ...models.wrappers import SourceData, SourceConfig
from sqlalchemy.orm import sessionmaker


class WrapperSourceStorage(BaseWrapperStorage):

    def __init__(self, wrapper_name: str, session: sessionmaker):
        self.__wrapper_name = wrapper_name
        self.__session = session

    def insert_data(self, key: str, data: str) -> None:

        new_data = SourceData(name=self.__wrapper_name, key=key, data=data)

        with self.__session() as session:
            session.add(new_data)
            session.commit()

    def get_data(self, key: str) -> SourceData:
        with self.__session() as session:
            ...

    def insert_config(self, config: SourceConfig) -> None:

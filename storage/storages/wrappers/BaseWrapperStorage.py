from sqlalchemy.orm import sessionmaker
from abc import ABCMeta, abstractmethod


class BaseWrapperStorage(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, wrapper_name: str, session: sessionmaker):
        ...

    @abstractmethod
    def insert_data(self, key: str, data: str) -> None:
        ...

    @abstractmethod
    def get_data(self, key: str) -> str:
        ...

    @abstractmethod
    def delete_data(self, key: str) -> None:
        ...

    @abstractmethod
    def get_config(self, key: str) -> str:
        ...

    @abstractmethod
    def set_config(self, key: str, value: str) -> None:
        ...

    @abstractmethod
    def delete_config(self, key: str) -> None:
        ...

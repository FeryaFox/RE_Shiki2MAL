from models.History import HistoryChanges
from abc import ABCMeta, abstractmethod


class BaseSource(metaclass=ABCMeta):
    urls: list[str]
    wrapper_name: str
    required_configs: dict[str: str | None]

    def __init__(self, username: str, storage):  # TODO logging (create class for logging)
        self.__storage = storage
        self.username = username

    @abstractmethod
    def get_histories_change(self) -> HistoryChanges:
        ...

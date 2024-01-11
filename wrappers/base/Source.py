from models.History import HistoryChanges
from abc import ABCMeta, abstractmethod


class BaseSource(metaclass=ABCMeta):
    url: str
    name: str
    require_settings: [str]

    def __init__(self, username: str, storage, log):  # TODO logging (create class for logging)
        self.__storage = storage
        self.username = username

    @abstractmethod
    def get_histories_change(self) -> HistoryChanges:
        ...

from models.History import HistoryChange


class BaseSource:
    url: str
    name: str
    require_tokens: [str]

    def __init__(self, username: str, storage):
        self.__storage = storage
        self.username = username

    def get_histories_change(self) -> HistoryChange:
        ...

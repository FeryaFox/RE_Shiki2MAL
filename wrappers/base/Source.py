from models.History import HistoryChange


class BaseSource:
    url: str
    name: str
    require_settings: [str]

    def __init__(self, username: str, storage, log): # TODO logging (create class for logging)
        self.__storage = storage
        self.username = username

    def get_histories_change(self) -> HistoryChange:
        ...

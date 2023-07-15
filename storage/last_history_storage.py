import json

# TODO добавить поддержку БД
# TODO добавить pydantic


class HistoryStorage:
    def __init__(self, filename="shikimori_last_history.json"):
        self.filename = filename

    def load_last_history(self) -> dict:
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            return data

        except FileNotFoundError:
            return {}

    def load_last_history_by_username(self, username: str):
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
            return data[username]

        except FileNotFoundError:
            return {}

    def save_last_history_by_username(self, username: str, last_history_id: str):
        data = {}
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = {}

        data |= {username: last_history_id}
        with open(self.filename, "w") as f:
            json.dump(data, f)

class MALAnimeNotFound(Exception):
    def __init__(self, text, anime_id):
        self.txt = text
        self.anime_id = anime_id


class MALAddToListError(Exception):
    def __init__(self, text, status_code, json_data):
        self.txt = text
        self.status_code = status_code
        self.json_data = json_data


class MALRequestError(Exception):
    def __init__(self):
        self.txt = "Error to send request"

class MALDeleteError(Exception):
    def __init__(self, anime_id):
        self.anime_id = anime_id

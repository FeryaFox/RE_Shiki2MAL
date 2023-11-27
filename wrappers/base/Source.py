

class BaseSource:
    url = ""
    name = ""
    parse_mode = "" # отвечает за то, каким образом будет происходить получение
    def __int__(self, username):
        self.username = username

    def get_histories(self) -> :
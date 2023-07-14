class ARMAnimeNotExist(Exception):
    def __init__(
            self,
            anime_id: str | int,
            source: str
    ):

        self.msg = f"Anime with id {anime_id} does not exist in {source}"

    def __str__(
            self
    ):

        print(self.msg)

class ARMRequestError(Exception):
    def __init__(
            self,
            anime_id: str | int,
            source: str,
            status_code: int
    ):

        self.msg = f"Failed to get anime info '{anime_id}' info in {source}. Statuscode: {status_code}"

    def __str__(
            self
    ):

        print(self.msg)

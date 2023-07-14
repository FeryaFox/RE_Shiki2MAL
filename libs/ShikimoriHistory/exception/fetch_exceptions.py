class ShikimoriProfileNotfound(Exception):
    def __init__(
            self,
            profile_name: str
    ):
        self.msg = f"Profile '{profile_name}' does not exists!!!"

    def __str__(
            self
    ):
        print(self.msg)


class ShikimoriGetHistoryError(Exception):
    def __init__(
            self,
            profile_name: str,
            status_code: int
    ):
        self.msg = f"Failed to get info profile '{profile_name}' info. Statuscode: {status_code}"

    def __str__(
            self
    ):
        print(self.msg)


class ShikimoriEmptyHistory(Exception):
    ...


class ShikimoriTooManyRequests(Exception):
    ...


class ShikimoriForbidden(Exception):
    ...

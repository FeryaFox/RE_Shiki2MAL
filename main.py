user_name = "ff146"


#TODO побавить поддержку манги
# TODO это так на будущее, сделать поддержку нескольких пользователей

class LastHistoryIdSaverLoader:

    def __init__(self) -> None:
        self.last_history_id = self.load_last_history_id()

    def __str__(self) -> str:
        return str(self.last_history_id)

    @staticmethod
    def save_last_history_id(news_id: int) -> None:
        with open("last_id.txt", "w") as f:
            f.write(str(news_id))

    @staticmethod
    def load_last_history_id() -> int:
        with open("last_id.txt", "r") as f:
            return int(f.read())


def main():
    # s = ShikimoriHistoryGetter(user_name)
    # s.get_news()
    ...


if __name__ == "__main__":
    main()

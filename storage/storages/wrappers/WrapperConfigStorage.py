from sqlalchemy.orm import Session


class WrapperConfigStorage:
    def __init__(self, session: Session) -> None:
        self.__session = session

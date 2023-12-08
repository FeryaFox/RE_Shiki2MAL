from sqlalchemy.engine import Engine


class BaseWrapperStorage:
    def __init__(self, wrapper_name: str, engine: Engine):
        self.__wrapper_name = wrapper_name
        self.__engine = engine

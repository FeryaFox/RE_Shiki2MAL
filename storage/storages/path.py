from sqlalchemy.engine import Engine


class PathStorage:
    def __init__(self, engine: Engine):
        self.__engine = engine

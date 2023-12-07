from sqlalchemy import create_engine


class Storage:
    def __init__(self, db_name: str = "RE_Shiki2MAL.db"):
        self.__engine = create_engine(f'sqlite://{db_name}', echo=True)



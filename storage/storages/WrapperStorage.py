from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_
from wrappers.enums import WrapperTypes
from storage.models.wrappers import Wrappers, WrappersData, WrappersConfig
import json
from ..utils import WrapperUtils


class WrapperStorage:
    class WrapperDataStorage:
        class WrapperDataStorageIterator:
            def __init__(self, data):
                self.__data = data

            def __iter__(self):
                return self

            def __next__(self):
                if self.__data == []:
                    raise StopIteration
                item = self.__data[0]
                del self.__data[0]
                return item

        def __init__(self, wrapper_id: int, session: sessionmaker):
            self.__wrapper_id = wrapper_id
            self.__session = session

        def __getitem__(self, key: str) -> str | None:
            with self.__session() as session:
                query = (
                    select(
                        WrappersData.value
                    )
                    .select_from(WrappersData)
                    .filter(
                        and_(
                            WrappersData.wrapper_id == self.__wrapper_id,
                            WrappersData.key == key
                        )
                    )
                )
                result = session.execute(query).fetchone()
                return result[0] if result is not None else None

        def __setitem__(self, key: str, value: str):
            with self.__session() as session:
                element = session.query(WrappersData).filter_by(wrapper_id=self.__wrapper_id, key=key).first()
                if element:
                    element.value = value
                else:
                    element = WrappersData(wrapper_id=self.__wrapper_id, key=key, value=value)
                    session.add(element)

                session.commit()
                return element

        def __delitem__(self, key: str):
            with self.__session() as session:
                session.query(WrappersData).filter_by(wrapper_id=self.__wrapper_id, key=key).delete()
                session.commit()

        def __str__(self):
            result = self.__get_all_data()
            res = {}
            for key, value in result:
                res |= {key: value}
            return json.dumps(res, indent=4)

        def __get_all_data(self):
            with self.__session() as session:
                query = (
                    select(
                        WrappersData.key,
                        WrappersData.value
                    )
                    .select_from(WrappersData)
                    .filter(
                        WrappersData.wrapper_id == self.__wrapper_id
                    )
                )
                result = session.execute(query).fetchall()
            result = result if result != [] else None
            return result

        def __iter__(self):
            print(self.__get_all_data())
            return self.WrapperDataStorageIterator(self.__get_all_data())

    class WrapperConfigStorage:
        class WrapperConfigStorageIterator:
            def __init__(self, data):
                self.__data = data

            def __iter__(self):
                return self

            def __next__(self):
                if self.__data == []:
                    raise StopIteration
                item = self.__data[0]
                del self.__data[0]
                return item

        def __init__(self, wrapper_id: int, session: sessionmaker):
            self.__wrapper_id = wrapper_id
            self.__session = session

        def __getitem__(self, key: str) -> str | None:
            with self.__session() as session:
                query = (
                    select(
                        WrappersConfig.value
                    )
                    .select_from(WrappersConfig)
                    .filter(
                        and_(
                            WrappersConfig.wrapper_id == self.__wrapper_id,
                            WrappersConfig.key == key
                        )
                    )
                )
                result = session.execute(query).fetchone()
                return result[0] if result is not None else None

        def __setitem__(self, key: str, value: str):
            with self.__session() as session:
                element = session.query(WrappersConfig).filter_by(wrapper_id=self.__wrapper_id, key=key).first()
                if element:
                    element.value = value
                else:
                    element = WrappersConfig(wrapper_id=self.__wrapper_id, key=key, value=value)
                    session.add(element)

                session.commit()
                return element

        def __delitem__(self, key: str):
            with self.__session() as session:
                session.query(WrappersConfig).filter_by(wrapper_id=self.__wrapper_id, key=key).delete()
                session.commit()

        def __str__(self):
            result = self.__get_all_data()
            res = {}
            for key, value in result:
                res |= {key: value}
            return json.dumps(res, indent=4)

        def __get_all_data(self):
            with self.__session() as session:
                query = (
                    select(
                        WrappersConfig.key,
                        WrappersConfig.value
                    )
                    .select_from(WrappersConfig)
                    .filter(
                        WrappersConfig.wrapper_id == self.__wrapper_id
                    )
                )
                result = session.execute(query).fetchall()
            result = result if result != [] else None
            return result

        def __iter__(self):
            print(self.__get_all_data())
            return self.WrapperConfigStorageIterator(self.__get_all_data())

    def __init__(self, wrapper_name: str, session: sessionmaker, wrapper_type: WrapperTypes):
        self.__session = session
        self.__wrapper_type = wrapper_type
        self.__wrapper_id = WrapperUtils.get_wrapper_id(wrapper_name, wrapper_type, session)
        self.data = self.WrapperDataStorage(self.__wrapper_id, self.__session)
        self.config = self.WrapperConfigStorage(self.__wrapper_id, self.__session)

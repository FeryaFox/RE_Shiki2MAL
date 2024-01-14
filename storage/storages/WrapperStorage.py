from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, and_
from wrappers.enums import WrapperTypes
from storage.models.wrappers import Wrappers, WrappersData, WrappersConfig
import json


class WrapperStorage:
    class WrapperDataStorage:
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
            res = {}
            for key, value in result:
                res |= {key: value}
            return json.dumps(res, indent=4)

        def __iter__(self):
            return self

        # def __next__(self):
        #     with self.__session() as session:
        #         return WrappersData(wrapper_id=self.__wrapper_id)

    def __init__(self, wrapper_name: str, session: sessionmaker, wrapper_type: WrapperTypes):
        self.__session = session
        self.__wrapper_type = wrapper_type
        self.__wrapper_id = self.__get_wrapper_id(wrapper_name)
        self.data = self.WrapperDataStorage(self.__wrapper_id, self.__session)

    def __get_wrapper_id(self, wrapper_name) -> int | None:
        with self.__session() as session:
            query = (
                select(
                    Wrappers.id
                )
                .select_from(Wrappers)
                .filter(
                    Wrappers.wrapper_name == wrapper_name,
                    Wrappers.wrapper_type == self.__wrapper_type
                )

            )
            result = session.execute(query).fetchone()
        return result[0] if result is not None else None


    # работа с конфигами
    def get_config(self, key: str) -> str | None:
        with self.__session() as session:
            query = (
                select(
                    WrappersConfig.data
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

    def set_config(self, key: str, value: str) -> None:
        new_data = WrappersConfig(wrapper_id=self.__wrapper_id, key=key, data=value)
        with self.__session() as session:
            session.add(new_data)
            session.commit()

    def delete_config(self, key: str) -> None:
        with self.__session() as session:
            session.query(WrappersConfig).filter_by(wrapper_id=self.__wrapper_id, key=key).delete()
            session.commit()

    def update_config(self, key: str, value: str) -> None:
        with self.__session() as session:
            session.query(WrappersConfig).filter(WrappersConfig.wrapper_id == self.__wrapper_id,
                                               WrappersConfig.key == key).update({"data": value})
            session.commit()

    def get_all_config(self) -> [str]:
        with self.__session() as session:
            query = (
                select(
                    WrappersConfig.key,
                    WrappersConfig.data
                )
                .select_from(WrappersConfig)
                .filter(
                    WrappersConfig.wrapper_id == self.__wrapper_id
                )
            )
            result = session.execute(query).fetchall()
        return result if result != [] else None

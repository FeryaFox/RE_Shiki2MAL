from sqlalchemy.orm import sessionmaker
from wrappers.enums.WrapperTypes import WrapperTypes
from sqlalchemy import select
from storage.models.wrappers import WrappersConfig, Wrappers
from ..utils import WrapperUtils
from wrappers.enums.WrapperStatuses import WrapperStatuses
from wrappers.enums import WrapperTypes
from ..exception import WrapperNotFound
from ..dataclasses import WrapperList, Wrapper
from ..typeddict import ShortWrapperInfo


class WrapperControllerStorage:
    def __init__(self, session: sessionmaker) -> None:
        self.__session = session

    def get_all_config(self, wrapper_name: str, wrapper_type: WrapperTypes) -> dict[str: str] | None:
        with self.__session() as session:
            query = (
                select(
                    WrappersConfig.key,
                    WrappersConfig.value
                )
                .select_from(WrappersConfig)
                .filter(
                    WrappersConfig.wrapper_id == WrapperUtils.get_wrapper_id(wrapper_name, wrapper_type, self.__session)
                )
            )
            result = session.execute(query).fetchall()
        result = result if result != [] else None
        return result

    def get_wrappers(self, wrapper_type: WrapperTypes | None = None) -> WrapperList:
        with self.__session() as session:
            if wrapper_type is None:
                query = (
                    select(
                        Wrappers.id,
                        Wrappers.wrapper_status,
                        Wrappers.wrapper_type,
                        Wrappers.wrapper_name
                    )
                    .select_from(Wrappers)
                )
                result = session.execute(query).fetchall()

            return WrapperList(
                [
                    Wrapper(
                        wrapper.id, wrapper.wrapper_name,
                        wrapper.wrapper_type,
                        wrapper.wrapper_status
                    ) for wrapper in result
                ]
            )

    def register_wrapper(self, wrapper_name: str, wrapper_type: WrapperTypes, commit: bool = True) -> None:
        with self.__session() as session:

            element = session.query(Wrappers).filter_by(wrapper_name=wrapper_name, wrapper_type=wrapper_type).first()

            if not element:
                element = Wrappers(wrapper_name=wrapper_name, wrapper_type=wrapper_type, wrapper_status=WrapperStatuses.disabled)
                session.add(element)
                if commit:
                    session.commit()

    def register_wrappers(self, wrappers: list[ShortWrapperInfo]) -> None:
        with self.__session() as session:
            for wrapper in wrappers:
                self.register_wrapper(wrapper.name, wrapper.type, commit=False)
                session.commit()

    def change_wrapper_status(self, wrapper_name: str, wrapper_type: WrapperTypes, wrapper_status: WrapperStatuses) -> None:
        with self.__session() as session:
            element = session.query(Wrappers).filter_by(wrapper_name=wrapper_name, wrapper_type=wrapper_type).first()
            if element:
                element.wrapper_status = wrapper_status
                session.commit()
            else:
                raise WrapperNotFound(wrapper_name=wrapper_name, wrapper_type=wrapper_type)

    def check_wrapper_status(self, wrapper_name: str, wrapper_type: WrapperTypes) -> WrapperStatuses | None:
        with self.__session() as session:
            element = session.query(Wrappers).filter_by(wrapper_name=wrapper_name, wrapper_type=wrapper_type).first()
            if element:
                return element.wrapper_status
            raise WrapperNotFound(wrapper_name=wrapper_name, wrapper_type=wrapper_type)

    def set_delete_wrapper_not_from_list(self, wrappers_list: WrapperList | list[ShortWrapperInfo]) -> None:
        with (self.__session() as session):
            if not isinstance(wrappers_list, WrapperList):
                wrappers_db = session.query(Wrappers).all()

                for wrapper_db in wrappers_db:
                    for wrapper_list in wrappers_list:
                        print(wrapper_list)
                        if wrapper_db.wrapper_name == wrapper_list["name"] and wrapper_db.wrapper_type == wrapper_list["type"]:
                            continue
                        element = session.query(
                            Wrappers

                        ).filter_by(
                            wrapper_name=wrapper_db.wrapper_name,
                            wrapper_type=wrapper_db.wrapper_type
                        ).first()
                        if element:
                            element.wrapper_status = WrapperStatuses.deleted

            else:
                wrappers_db = session.query(Wrappers).all()

                for wrapper_db in wrappers_db:
                    for wrapper_list in wrappers_list:
                        if wrapper_db.wrapper_name == wrapper_list.wrapper_name and wrapper_db.wrapper_type == wrapper_list.wrapper_type:
                            continue
                        element = session.query(
                            Wrappers

                        ).filter_by(
                            wrapper_name=wrapper_db.wrapper_name,
                            wrapper_type=wrapper_db.wrapper_type
                        ).first()
                        if element:
                            element.wrapper_status = WrapperStatuses.deleted
            session.commit()

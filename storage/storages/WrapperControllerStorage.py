from sqlalchemy.orm import sessionmaker
from wrappers.enums.WrapperTypes import WrapperTypes
from sqlalchemy import select
from storage.models.wrappers import WrappersConfig, Wrappers
from ..utils import WrapperUtils
from wrappers.enums.WrapperStatuses import WrapperStatuses


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


    def get_wrappers(self) -> dict[str: WrapperStatuses] | None:
        with self.__session() as session:
            query = (
                select(
                    Wrappers.id,
                )
            )

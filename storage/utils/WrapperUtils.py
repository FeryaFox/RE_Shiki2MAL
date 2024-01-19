from wrappers.enums.WrapperTypes import WrapperTypes
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from storage.models.wrappers import Wrappers, WrappersData, WrappersConfig


class WrapperUtils:
    @staticmethod
    def get_wrapper_id(wrapper_name: str, wrapper_type: WrapperTypes, session_: sessionmaker) -> int | None:
        with session_() as session:
            query = (
                select(
                    Wrappers.id
                )
                .select_from(Wrappers)
                .filter(
                    Wrappers.wrapper_name == wrapper_name,
                    Wrappers.wrapper_type == wrapper_type
                )

            )
            result = session.execute(query).fetchone()
        return result[0] if result is not None else None

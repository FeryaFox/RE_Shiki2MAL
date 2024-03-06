from typing import TypedDict
from wrappers.enums import WrapperTypes


class ShortWrapperInfo(TypedDict):
    name: str
    type: WrapperTypes

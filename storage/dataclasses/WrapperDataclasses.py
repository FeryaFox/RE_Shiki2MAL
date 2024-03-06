from dataclasses import dataclass
from typing import List

from wrappers.enums import WrapperTypes, WrapperStatuses


@dataclass
class Wrapper:
    wrapper_id: int
    wrapper_name: str
    wrapper_type: WrapperTypes
    wrapper_status: WrapperStatuses


@dataclass
class WrapperList:

    class WrapperListIterator:
        def __init__(self, data: List[Wrapper]):
            self.__data = data

        def __iter__(self):
            return self

        def __next__(self):
            if not self.__data:
                raise StopIteration
            item = self.__data[0]
            del self.__data[0]
            return item

    wrappers: List[Wrapper]

    def __getitem__(self, item: int) -> Wrapper:
        return self.wrappers[item]

    def __iter__(self) -> WrapperListIterator:
        return self.WrapperListIterator(self.wrappers)

    def get_wrappers_by_type(self, wrapper_type: WrapperTypes) -> [Wrapper]:
        return [i for i in self.wrappers if i.wrapper_type == wrapper_type.value]

    def get_wrapper_by_id(self, wrapper_id: int) -> Wrapper:
        for i in self.wrappers:
            if i.wrapper_id == wrapper_id:
                return i

    def get_wrapper_by_name(self, wrapper_name: str, wrapper_type: WrapperTypes) -> Wrapper:
        for i in self.wrappers:
            if i.wrapper_name == wrapper_name and i.wrapper_type == wrapper_type.value:
                return i

    def get_wrappers_by_status(self, wrapper_status: WrapperStatuses, wrapper_type: WrapperTypes | None = None) -> [Wrapper]:
        if wrapper_type is None:
            return [i for i in self.wrappers if i.wrapper_status == wrapper_status.value]
        return [i for i in self.wrappers if i.wrapper_status == wrapper_status.value and i.wrapper_type == wrapper_type.value]

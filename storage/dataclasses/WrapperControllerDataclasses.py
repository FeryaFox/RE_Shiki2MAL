from dataclasses import dataclass
from wrappers.enums import WrapperTypes, WrapperStatuses


@dataclass
class WrapperList:
    wrapper_id: int
    wrapper_name: str
    wrapper_type: WrapperTypes
    wrapper_status: WrapperStatuses

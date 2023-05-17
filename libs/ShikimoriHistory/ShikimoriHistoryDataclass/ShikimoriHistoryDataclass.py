from dataclasses import dataclass
import arrow
from ..ShikimoriHistoryEnum.ShikimoriHistoryEnums import *


@dataclass
class HistoryChangeType:
    status: list[AnimeStatus, AnimeStatus] | None
    score: list[int, int] | None
    episodes: list[int, int] | None
    add_or_remove: AddOrRemove = AddOrRemove.none


@dataclass
class History:
    history_type: HistoryType
    object_id: int
    history_time: arrow.arrow.Arrow
    history_id: int
    history_change: HistoryChangeType

from dataclasses import dataclass
import arrow
from .ShikimoriHistoryEnums import *


@dataclass
class HistoryChangeType:
    status: list[AnimeStatus, AnimeStatus]
    score: list[int, int]
    episodes: list[int, int]
    add_or_remove: AddOrRemove = AddOrRemove.none


@dataclass
class History:
    anime_id: int
    history_time: arrow.arrow.Arrow
    history_id: int
    history_change: HistoryChangeType

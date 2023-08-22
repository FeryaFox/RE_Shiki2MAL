from dataclasses import dataclass
import arrow
from ..enum.ShikimoriHistoryEnums import *


@dataclass
class AnimeHistoryChangeType:
    status: list[AnimeStatus, AnimeStatus] | None
    score: list[int, int] | None
    episodes: list[int, int] | None
    rewatches: list[int, int] | None
    text: list[None | str, None | str] | None
    add_or_remove: AddOrRemove = AddOrRemove.none


@dataclass
class MangaAndRanobeHistoryChangeType:
    status: list[MangaAndRanobeStatus, MangaAndRanobeStatus] | None
    score: list[int, int] | None
    chapters: list[int, int] | None
    rewatches: list[int, int] | None
    text: list[None | str, None | str] | None
    add_or_remove: AddOrRemove = AddOrRemove.none


@dataclass
class History:
    history_type: HistoryType
    object_id: int
    history_time: arrow.arrow.Arrow
    history_id: int
    history_change: AnimeHistoryChangeType | MangaAndRanobeHistoryChangeType


@dataclass
class Histories:
    histories: list[History]
    next_page: bool

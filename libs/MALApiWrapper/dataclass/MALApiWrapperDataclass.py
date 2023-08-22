from dataclasses import dataclass
import pydantic
import arrow
from ..enum.MALApiWrapperEnum import MALAnimeWatchStatus, MALMangaAndRanobeReadingStatus

# FIXME переписать на pydantic, плюс проверить все ли части присутсвтуют


@dataclass
class MALAnimeInfo:
    status: MALAnimeWatchStatus
    score: int
    num_episodes_watched: int
    is_rewatching: bool
    updated_at: arrow.arrow.Arrow
    priority: int
    num_times_rewatched: int
    rewatch_value: int
    tags: list
    comments: str


@dataclass
class MALMangaInfo:
    status: MALMangaAndRanobeReadingStatus
    score: int
    num_volumes_read: int
    num_chapters_read: int
    is_rereading: bool
    updated_at: arrow.arrow.Arrow
    priority: int
    num_times_reread: int
    reread_value: int
    tags: list
    comments: str

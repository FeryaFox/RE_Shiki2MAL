from dataclasses import dataclass
import arrow
from ..enum.MALApiWrapperEnum import MALAnimeWatchStatus


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

from enum import Enum


class AddOrRemove(Enum):
    add = 0
    remove = 1
    none = 2


class AnimeStatus(Enum):
    planned = "planned"
    watching = "watching"
    rewatching = "rewatching"
    completed = "completed"
    on_hold = "on_hold"
    dropped = "dropped"
    none = "none"


class HistoryType(Enum):
    ranobe = "ranobe"
    anime = "anime"
    manga = "manga"

from enum import Enum


class BaseStatus(Enum):
    ...


class AnimeStatus(BaseStatus):
    planned = "planned"
    watching = "watching"
    rewatching = "rewatching"
    completed = "completed"
    on_hold = "on_hold"
    dropped = "dropped"
    none = "none"


class MangaStatus(BaseStatus):
    reading = "reading"
    planned = "planned"
    rereading = "rereading"
    completed = "completed"
    on_hold = "on_hold"
    dropped = "dropped"
    none = "none"


class RanobeStatus(BaseStatus):
    reading = "reading"
    planned = "planned"
    rereading = "rereading"
    completed = "completed"
    on_hold = "on_hold"
    dropped = "dropped"
    none = "none"

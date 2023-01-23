from enum import Enum


class MALAnimeWatchStatus(Enum):
    watching = "watching"
    completed = "completed"
    on_hold = "on_hold"
    dropped = "dropped"
    plan_to_watch = "plan_to_watch"


class HttpMethod(Enum):
    get = "get"
    post = "post"
    put = "put"
    delete = "delete"
    patch = "patch"

import arrow
from ..dataclass.MALApiWrapperDataclass import MALAnimeInfo
from ..enum.MALApiWrapperEnum import MALAnimeWatchStatus


def convert_dict_to_MALAnimeInfo(d: dict) -> MALAnimeInfo:
    return MALAnimeInfo(
        status=MALAnimeWatchStatus(d["status"]),
        score=d["score"],
        num_episodes_watched=d["num_episodes_watched"],
        is_rewatching=bool(d["is_rewatching"]),
        updated_at=arrow.get(d["updated_at"]),
        priority=d["priority"],
        num_times_rewatched=d["num_times_rewatched"],
        rewatch_value=d["rewatch_value"],
        tags=d["tags"],
        comments=d["comments"]
    )

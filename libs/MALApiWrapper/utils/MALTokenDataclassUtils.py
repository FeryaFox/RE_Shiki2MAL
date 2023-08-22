import arrow
from ..dataclass.MALApiWrapperDataclass import MALAnimeInfo, MALMangaInfo
from ..enum.MALApiWrapperEnum import MALAnimeWatchStatus, MALMangaAndRanobeReadingStatus


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


def convert_dict_to_MALMangaInfo(d: dict) -> MALMangaInfo:
    return MALMangaInfo(
        status=MALMangaAndRanobeReadingStatus(d["status"]),
        score=d["score"],
        num_volumes_read=d["num_volumes_read"],
        num_chapters_read=d["num_chapters_read"],
        is_rereading=bool(d["is_rereading"]),
        updated_at=arrow.get(d["updated_at"]),
        priority=d["priority"],
        num_times_reread=d["num_times_reread"],
        reread_value=d["reread_value"],
        tags=d["tags"],
        comments=d["comments"],
    )

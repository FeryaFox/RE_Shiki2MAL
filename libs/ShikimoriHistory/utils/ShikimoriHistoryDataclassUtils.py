from ..dataclass import History, AnimeHistoryChangeType, MangaAndRanobeHistoryChangeType
from ..enum import AddOrRemove, AnimeStatus, MangaAndRanobeStatus, HistoryType

# TODO переписать вот это на pydantic


def convert_dict_to_dataclass_history(d: dict) -> History:
    score = None
    if "score" in d:
        score = [
            d["score"][0],
            d["score"][1]
        ]
    add_or_remove = AddOrRemove.none
    if "id" in d:
        if d["id"][0] is None:
            add_or_remove = AddOrRemove.add
        else:
            add_or_remove = AddOrRemove.remove

    rewatches = None
    if "rewatches" in d:
        rewatches = [
            d["rewatches"][0],
            d["rewatches"][1]
        ]

    text = None
    if "text" in d:
        text = [
            d["text"][0],
            d["text"][1]
        ]
    if d["history_type"] == HistoryType.anime.value:
        status = None
        if "status" in d:
            status = [
                AnimeStatus(d["status"][0]),
                AnimeStatus(d["status"][1])
            ]
        elif "id" in d:
            if d["id"][0] is None:
                status = [
                    AnimeStatus.none,
                    AnimeStatus.planned
                ]
            else:
                status = [
                    AnimeStatus.planned,
                    AnimeStatus.none
                ]

        episodes = None
        if "episodes" in d:
            episodes = [
                d["episodes"][0],
                d["episodes"][1]
            ]

        hc = AnimeHistoryChangeType(
            status=status,
            score=score,
            episodes=episodes,
            add_or_remove=add_or_remove,
            rewatches=rewatches,
            text=text
        )
    elif d["history_type"] == HistoryType.manga.value or d["history_type"] == HistoryType.ranobe.value:
        status = None
        if "status" in d:
            status = [
                MangaAndRanobeStatus(d["status"][0]),
                MangaAndRanobeStatus(d["status"][1])
            ]
        elif "id" in d:
            if d["id"][0] is None:
                status = [
                    MangaAndRanobeStatus.none,
                    MangaAndRanobeStatus.planned
                ]
            else:
                status = [
                    AnimeStatus.planned,
                    AnimeStatus.none
                ]

        chapters = None
        if "chapters" in d:
            chapters = [
                d["chapters"][0],
                d["chapters"][1]
            ]
        hc = MangaAndRanobeHistoryChangeType(
            status=status,
            score=score,
            chapters=chapters,
            add_or_remove=add_or_remove,
            rewatches=rewatches,
            text=text
        )
    r = History(
        history_type=HistoryType(d["history_type"]),
        object_id=int(d["object_id"]),
        history_time=d["history_time"],
        history_id=int(d["history_id"]),
        history_change=hc
    )
    return r

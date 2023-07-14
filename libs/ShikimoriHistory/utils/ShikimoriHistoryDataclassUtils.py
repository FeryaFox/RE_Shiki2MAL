from ..dataclass import History, HistoryChangeType
from ..enum import AddOrRemove, AnimeStatus, HistoryType


def convert_dict_to_dataclass_history(d: dict) -> History:
    # TODO добавить поддержку манги и ранобэ
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
                    AnimeStatus.watching
                ]
            else:
                status = [
                    AnimeStatus.watching,
                    AnimeStatus.none
                ]

        score = None
        if "score" in d:
            score = [
                d["score"][0],
                d["score"][1]
            ]

        episodes = None
        if "episodes" in d:
            episodes = [
                d["episodes"][0],
                d["episodes"][1]
            ]

        add_or_remove = AddOrRemove.none
        if "id" in d:
            if d["id"][0] is None:
                add_or_remove = AddOrRemove.add
            else:
                add_or_remove = AddOrRemove.remove

        hc = HistoryChangeType(
            status=status,
            score=score,
            episodes=episodes,
            add_or_remove=add_or_remove
        )
        r = History(
            history_type=HistoryType(d["history_type"]),
            object_id=int(d["object_id"]),
            history_time=d["history_time"],
            history_id=int(d["history_id"]),
            history_change=hc
        )
        return r

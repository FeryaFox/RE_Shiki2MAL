from pydantic import BaseModel, AnyUrl
from datetime import datetime
from enums.HistoryType import HistoryChangeType, HistoryType
from enums.WatchingReadingStatus import BaseStatus
from models.Name import Name


class HistoryChangeObject(BaseModel):
    anime_manga_ranobe_id: int | None
    anime_manga_title: [Name] | None
    history_change_type: HistoryChangeType
    change_status: [BaseStatus, BaseStatus]
    watching_reading_episodes: [int, int]
    rewatching_reading_times: [int, int]
    score: [int, int]
    text: [str, str]


class HistoryChange(BaseModel):
    history_id: int | None
    ip: AnyUrl | None
    app: str | None
    time: datetime | None
    history_object: HistoryChangeObject


class HistoryChanges(BaseModel):
    type: HistoryType
    time: datetime | None
    id_type: str # What type id is (shikimori_id, mal_id or usual name)
    history_changes: [HistoryChange]

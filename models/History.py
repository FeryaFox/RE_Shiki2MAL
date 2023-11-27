from pydantic import BaseModel, AnyUrl
from datetime import datetime
from enums.HistoryType import HistoryChangeType
from enums.WatchingReadingStatus import BaseStatus


class HistoryChangeObject(BaseModel):
    anime_id: int
    history_change_type: HistoryChangeType
    change_status: [BaseStatus, BaseStatus]
    watching_reading_episodes: [int, int]
    rewatching_reading_times: [int, int]
    score: [int, int]
    text: [str, str]


class HistoryChange(BaseModel):
    history_id: int
    ip: AnyUrl
    app: str
    time: datetime
    history_object: HistoryChangeObject


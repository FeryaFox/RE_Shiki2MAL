from enum import Enum


class HistoryType(Enum):
    changeType = 0 # это тип, когда показывается, что когда изменилось
    allHistory = 1 # просто даёт список просмотренных тайтлов

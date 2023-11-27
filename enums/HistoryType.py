from enum import Enum


class HistoryType(Enum):
    anime = 0
    manga = 1
    ranobe = 2


class HistoryChangeType(Enum):
    nothing = 0
    addToList = 1
    removeFromList = 2
    updateList = 3

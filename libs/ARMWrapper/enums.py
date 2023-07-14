from enum import Enum


class ARMSource(Enum):
    anilist = "anilist"
    anidb = "anidb"
    anime_planet = "anime-planet"
    anisearch = "anisearch"
    imdb = "imdb"
    kitsu = "kitsu"
    livechart = "livechart"
    themoviedb = "themoviedb"
    notify_moe = "notify-moe"
    myanimelist = "myanimelist"


class ARMApiVersion(Enum):
    v1 = "v1"
    v2 = "v2"

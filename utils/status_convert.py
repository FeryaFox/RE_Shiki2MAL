from libs.ShikimoriHistory.enum import AnimeStatus, MangaAndRanobeStatus
from libs.MALApiWrapper.enum.MALApiWrapperEnum import MALAnimeWatchStatus, MALMangaAndRanobeReadingStatus


def convert_Shikimori_to_MALStatus(status: AnimeStatus) -> MALAnimeWatchStatus:
    match status:
        case AnimeStatus.planned:
            return MALAnimeWatchStatus.plan_to_watch

        case AnimeStatus.watching:
            return MALAnimeWatchStatus.watching

        case AnimeStatus.completed:
            return MALAnimeWatchStatus.completed

        case AnimeStatus.on_hold:
            return MALAnimeWatchStatus.on_hold

        case AnimeStatus.dropped:
            return MALAnimeWatchStatus.dropped

def convert_Shikimori_to_MALStatus_manga(status: MangaAndRanobeStatus) -> MALMangaAndRanobeReadingStatus:
    match status:
        case MangaAndRanobeStatus.planned:
            return MALMangaAndRanobeReadingStatus.plan_to_read

        case MangaAndRanobeStatus.watching:
            return MALMangaAndRanobeReadingStatus.reading

        case MangaAndRanobeStatus.completed:
            return MALMangaAndRanobeReadingStatus.completed

        case MangaAndRanobeStatus.on_hold:
            return MALMangaAndRanobeReadingStatus.on_hold

        case MangaAndRanobeStatus.dropped:
            return MALMangaAndRanobeReadingStatus.dropped

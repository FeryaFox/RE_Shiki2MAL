from libs.ShikimoriHistory.enum import AnimeStatus
from libs.MALApiWrapper.enum.MALApiWrapperEnum import MALAnimeWatchStatus


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

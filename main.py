
# TODO побавить поддержку манги
# TODO это так на будущее, сделать поддержку нескольких пользователей
import schedule
import time
from config import Config
from dataclasses import dataclass
from enums.sources_and_target import Targets
from libs.MALApiWrapper import MALApiWrapper
from libs.MALApiWrapper.enum.MALApiWrapperEnum import MALAnimeWatchStatus
from libs.ShikimoriHistory import ShikimoriHistoryGetter
from storage import HistoryStorage
from libs.ShikimoriHistory.exception.fetch_exceptions import ShikimoriForbidden
from libs.ShikimoriHistory.enum import HistoryType, AnimeStatus, AddOrRemove
from utils.status_convert import convert_Shikimori_to_MALStatus


@dataclass
class SyncPath:
    target: Targets
    source_username: str
    target_username: str
    target_object: MALApiWrapper # TODO если добавлю поддержку несколько целей, то добавить и сюда
    source_object: ShikimoriHistoryGetter
    source: str = "Shikimori"


def sync(last_history_storage: HistoryStorage, paths: list[SyncPath]):
    for i in paths:
        last_history_id = last_history_storage.load_last_history_by_username(i.source_username)
        try:
            history = i.source_object.get_all_histories().histories
        except ShikimoriForbidden:
            return
        if history[0].history_id == last_history_id:
            continue
        history.reverse()
        for j in history:
            if j.history_id > last_history_id:
                match j.history_change.add_or_remove:

                    case AddOrRemove.add | AddOrRemove.none:

                        match j.history_type:
                            case HistoryType.anime:

                                score = j.history_change.score[1] if j.history_change.score is not None else None
                                num_watched_episodes = j.history_change.episodes[1] if j.history_change.episodes is not None else None
                                rewatch_value = j.history_change.rewatches[1] if j.history_change.rewatches is not None else None
                                mal_anime_status = convert_Shikimori_to_MALStatus(j.history_change.status[1]) if j.history_change.status is not None else None
                                anime_statuses = j.history_change.status if j.history_change.status is not None else None

                                rewatch_value = rewatch_value if rewatch_value is not None and rewatch_value >= 0 else 0

                                print(j)
                                if anime_statuses is not None and anime_statuses[1] == AnimeStatus.rewatching:

                                    i.target_object.add_anime_to_list(
                                        j.object_id,
                                        MALAnimeWatchStatus.completed,
                                        is_rewatching=True,
                                        score=score,
                                        num_watched_episodes=num_watched_episodes,
                                    )
                                    continue

                                if anime_statuses is not None and anime_statuses[0] == AnimeStatus.rewatching:
                                    i.target_object.add_anime_to_list(
                                        j.object_id,
                                        MALAnimeWatchStatus.completed,
                                        is_rewatching=False,
                                        score=score,
                                        num_watched_episodes=num_watched_episodes,
                                        rewatch_value=rewatch_value
                                    )
                                    continue

                                i.target_object.add_anime_to_list(
                                    j.object_id,
                                    mal_anime_status,
                                    score=score,
                                    num_watched_episodes=num_watched_episodes,
                                    rewatch_value=rewatch_value
                                )

                    case AddOrRemove.remove:
                        i.target_object.delete_anime_from_list(
                            j.object_id
                        )
        last_history_storage.save_last_history_by_username(i.source_username, history[-1].history_id)


def load_sync_paths(config: Config) -> list[SyncPath]:
    paths = []
    for i in config.sync_paths:
        for j in config.sync_paths[i]:
            # TODO добавить поддержку нескольких источников

            target_object = MALApiWrapper(
                config.tokens["myanimelist"]["client_id"],
                config.tokens["myanimelist"]["client_secret"],
                token_saver_loader_params={"username": config.sync_paths[i][j]}
            )

            source_object = ShikimoriHistoryGetter(i)

            paths.append(SyncPath(
                target=j,
                source="Shikimori",
                source_username=i,
                target_username=config.sync_paths[i][j],
                target_object=target_object,
                source_object=source_object
            ))

    return paths


def full_sync(config: Config, last_history_storage: HistoryStorage):
    config.load_config()
    paths = load_sync_paths(config)
    sync(last_history_storage, paths)


def main():

    config = Config()
    config.load_config()

    last_history_storage = HistoryStorage()
    full_sync(config, last_history_storage)
    # schedule.every(1).minutes.do(full_sync, config=config, last_history_storage=last_history_storage)
    # #arm server
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)


if __name__ == "__main__":
    main()

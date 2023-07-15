
# TODO побавить поддержку манги
# TODO это так на будущее, сделать поддержку нескольких пользователей

from config import Config
from dataclasses import dataclass
from enums.sources_and_target import Targets
from libs.MALApiWrapper import MALApiWrapper
from libs.ShikimoriHistory import ShikimoriHistoryGetter
from storage import HistoryStorage

@dataclass
class SyncPath:
    target: Targets
    source_username: str
    target_username: str
    target_object: object
    source_object: ShikimoriHistoryGetter
    source: str = "Shikimori"


def sync(last_history_storage: HistoryStorage, paths: dict[SyncPath]):
    for i in paths:
        last_history_id = last_history_storage.load_last_history_by_username(i.source_username)
        history = i.source_object.get_all_histories()
        if history.histories[0] == last_history_id:
            continue
        

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


def main():

    config = Config()
    config.load_config()

    last_history_storage = HistoryStorage()

    # arm server

    paths = load_sync_paths(config)


if __name__ == "__main__":
    main()

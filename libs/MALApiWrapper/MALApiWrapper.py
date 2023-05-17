import requests
from typing import Callable
from .MALToken import MALToken
from .dataclass.MALTokenDataclass import MALTokenInfo
from .enum.MALApiWrapperEnum import HttpMethod, MALAnimeWatchStatus
from .dataclass.MALApiWrapperDataclass import MALAnimeInfo
from .utils.MALTokenDataclassUtils import convert_dict_to_MALAnimeInfo
from .exception.MALWrapperException import MALAnimeNotFound, MALAddToListError, MALRequestError, MALDeleteError


class MALApiWrapper:

    def __init__(
            self,
            client_id,
            client_secret,
            token_info_loader_func: None | Callable[[], MALTokenInfo | None] = None,
            token_info_saver_func: None | Callable[[MALTokenInfo], None] = None,
            token_saver_loader_params: None | dict = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret

        self.token = MALToken(
            client_id,
            client_secret,
            token_info_loader_func,
            token_info_saver_func,
            token_saver_loader_params
        )
        self.token.init_token()

    def add_anime_to_list(
            self,
            anime_id: int,
            status: MALAnimeWatchStatus | None = None,
            is_rewatching: bool | None = None,
            score: int | None = None,
            num_watched_episodes: int | None = None,
            priority: int | None = 1,
            num_times_rewatched: int | None = None,
            rewatch_value: int | None = None,
            tags: str | None = None,
            comments: str | None = None
    ) -> MALAnimeInfo:

        if status is not None:
            status = status.value

        r = self.__fetch_api(
            f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status",
            HttpMethod.patch,
            status=status,
            is_rewatching=is_rewatching,
            score=score,
            num_watched_episodes=num_watched_episodes,
            priority=priority,
            num_times_rewatched=num_times_rewatched,
            rewatch_value=rewatch_value,
            tags=tags,
            comments=comments
        )
        if r is None:
            raise MALRequestError()

        match r.status_code:
            case 200:
                return convert_dict_to_MALAnimeInfo(r.json())
            case 404:
                raise MALAnimeNotFound(f"Anime with id {anime_id} doesn't exist", anime_id)
            case _:
                raise MALAddToListError(f"Error to add anime to list", r.status_code, r.json())

    def delete_anime_from_list(self, anime_id: int):

        r = self.__fetch_api(
            f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status",
            HttpMethod.delete
        )
        if r is None:
            raise MALRequestError()

        match r.status_code:
            case 200:
                return True
            case 404:
                raise MALDeleteError(anime_id)

    def __fetch_api(self, url: str, method: HttpMethod, **kwargs):
        match method:
            case HttpMethod.get:
                return requests.get(url, params=kwargs, headers={"Authorization": f"Bearer {self.token.access_token}"})

            case HttpMethod.post:
                return requests.post(url, data=kwargs, headers={"Authorization": f"Bearer {self.token.access_token}"})

            case HttpMethod.put:
                return requests.put(url, data=kwargs, headers={"Authorization": f"Bearer {self.token.access_token}"})

            case HttpMethod.delete:
                return requests.put(url, data=kwargs, headers={"Authorization": f"Bearer {self.token.access_token}"})

            case HttpMethod.patch:
                return requests.patch(url, data=kwargs, headers={"Authorization": f"Bearer {self.token.access_token}"})
            case _:
                return None

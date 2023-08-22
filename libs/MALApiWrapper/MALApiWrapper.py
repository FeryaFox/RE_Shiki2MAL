import requests
from .MALToken import MALToken
from .enum.MALApiWrapperEnum import HttpMethod, MALAnimeWatchStatus, MALMangaAndRanobeReadingStatus
from .dataclass.MALApiWrapperDataclass import MALAnimeInfo, MALMangaInfo
from .utils.MALTokenDataclassUtils import convert_dict_to_MALAnimeInfo, convert_dict_to_MALMangaInfo
from .exception.MALWrapperException import MALAnimeNotFound, MALAddToListError, MALRequestError, MALDeleteError
from .MALToken.MALTokenSaverLoader import BaseMalTokenInfoSaverLoader

# TODO добавить поддержку web сервера для автоматичекского получения кода
# TODO добавить поддержку хранения токенов в БД


class MALApiWrapper:

    def __init__(
            self,
            client_id,
            client_secret,
            token_info_saver_loader: None | BaseMalTokenInfoSaverLoader = None,
            token_saver_loader_params: None | dict = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret

        self.token = MALToken(
            client_id,
            client_secret,
            token_info_saver_loader,
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

        is_rewatching = "true" if is_rewatching else "false"
        rewatch_value = 5 if rewatch_value is not None and rewatch_value > 5 else rewatch_value
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

    def add_manga_to_list(
            self,
            manga_id: int,
            status: MALMangaAndRanobeReadingStatus | None = None,
            is_rereading: bool | None = None,
            score: int | None = None,
            num_volumes_read: int | None = None,
            num_chapters_read: int | None = None,
            priority: int | None = 1,
            num_times_reread: int | None = None,
            reread_value: int | None = None,
            tags: str | None = None,
            comments: str | None = None
    ) -> MALMangaInfo:
        if status is not None:
            status = status.value

        is_rereading = "true" if is_rereading else "false"
        reread_value = 16 if reread_value is not None and reread_value > 16 else reread_value # TODO проверить надо ли это
        r = self.__fetch_api(
            f"https://api.myanimelist.net/v2/manga/{manga_id}/my_list_status",
            HttpMethod.patch,
            status=status,
            is_rereading=is_rereading,
            score=score,
            num_volumes_read=num_volumes_read,
            num_chapters_read=num_chapters_read,
            priority=priority,
            num_times_reread=num_times_reread,
            reread_value=reread_value,
            tags=tags,
            comments=comments
        )
        if r is None:
            raise MALRequestError()

        match r.status_code:
            case 200:
                return convert_dict_to_MALMangaInfo(r.json())
            case 404:
                raise MALAnimeNotFound(f"Manga with id {manga_id} doesn't exist", manga_id)
            case _:
                raise MALAddToListError(f"Error to add anime to list", r.status_code, r.json())

    def delete_manga_from_list(self, manga_id: int):

        r = self.__fetch_api(
            f"https://api.myanimelist.net/v2/manga/{manga_id}/my_list_status",
            HttpMethod.delete
        )
        if r is None:
            raise MALRequestError()

        match r.status_code:
            case 200:
                return True
            case 404:
                raise MALDeleteError(manga_id_id)

    def __fetch_api(self, url: str, method: HttpMethod, **kwargs):
        match method: # заменить вот это на стандартные Enum от requests
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

import requests
from .enums import ARMSource, ARMApiVersion
from .models import ARMResult
from .exceptions import ARMAnimeNotExist, ARMRequestError
import backoff


class ARMWrapper:

    def __init__(
            self,
            url: str = "https://arm.haglund.dev/api"):
        self.url = url

    def fetch_anime_id(
            self,
            anime_id: int,
            source: ARMSource):
        r = self.__fetch_api(
            source,
            anime_id,
            ARMApiVersion.v2
        )
        match r.status_code:
            case 200:
                ...
            case 400:
                raise ARMAnimeNotExist(anime_id, source.value)
            case _:
                raise ARMRequestError(anime_id, source.value, r.status_code)

        if r.text == "null":
            raise ARMAnimeNotExist(anime_id, source.value)

        return ARMResult(**r.json())


    @backoff.on_exception(
        backoff.expo,
        (
            requests.exceptions.RequestException
        ),
        max_time=10,
        max_tries=20
    )
    def __fetch_api(
            self,
            source: ARMSource,
            anime_id: int | str,
            api_version: ARMApiVersion) -> requests.Response:

        url = f"{self.url}/{api_version.value}/ids"
        r = requests.get(
            url,
            params={
                "source": source.value,
                "id": anime_id
            }
        )
        return r

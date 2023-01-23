import requests
import secrets
from typing import Callable
from .MALTokenSaverLoader import token_saver, token_loader
from ..dataclass.MALTokenDataclass import MALTokenInfo

# TODO добавить поддержку веб сервера

# Авторизация была подсмотрена туть https://gitlab.com/-/snippets/2039434
class MALToken:
    def __init__(
            self,
            client_id,
            client_secret,
            token_info_loader_func: None | Callable[[None | dict], MALTokenInfo | None] = None,
            token_info_saver_func: None | Callable[[MALTokenInfo, None | dict], None] = None,
            token_saver_loader_params: None | dict = None
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_type = None
        self.expires_in = None
        self.access_token = None
        self.refresh_token = None

        if token_info_loader_func is None:
            self.token_loader = token_loader
        else:
            self.token_loader = token_info_loader_func

        if token_info_saver_func is None:
            self.token_saver = token_saver
        else:
            self.token_saver = token_info_saver_func

        self.token_saver_loader_params = token_saver_loader_params

    def init_token(self):
        if self.token_type is None and self.expires_in is None and self.access_token is None and self.refresh_token is None:
            t = self.__load_token()
            if t is None:
                self.__generate_first_new_token()
                self.__save_token(self.get_token())
            else:
                self.__load_token_info(t)
                self.__refresh_token()
                self.__save_token(self.get_token())
                # TODO

    def refresh_token(self):
        self.__refresh_token()

    def get_token(self) -> MALTokenInfo:
        return MALTokenInfo(
            self.token_type,
            self.expires_in,
            self.access_token,
            self.refresh_token
        )

    def __refresh_token(self):
        data = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token
        }
        response = requests.post("https://myanimelist.net/v1/oauth2/token", data=data)
        match response.status_code:
            case 200:
                # Successfully refreshed the access token
                access_token = response.json()
                self.__load_token_info(access_token)
            case 401:
                self.__generate_first_new_token()
            case _:
                # There was an error refreshing the access token
                assert Exception
                print(f"Error refreshing the access token: {response.text}")

    def __load_token_info(self, token_info: MALTokenInfo | dict):
        if isinstance(token_info, dict):
            self.expires_in = token_info["expires_in"]
            self.access_token = token_info["access_token"]
            self.refresh_token = token_info["refresh_token"]
            self.token_type = token_info["token_type"]
        else:
            self.expires_in = token_info.expires_in
            self.access_token = token_info.access_token
            self.refresh_token = token_info.refresh_token
            self.token_type = token_info.token_type

    def __generate_first_new_token(self):
        code_verifier = code_challenge = self.__get_new_code_verifier()
        self.__print_new_authorisation_url(code_challenge)

        authorisation_code = input('Copy-paste the Authorisation Code: ').strip()
        token = self.__generate_new_token(authorisation_code, code_verifier)
        self.__load_token_info(token)

    @staticmethod
    def __get_new_code_verifier() -> str:
        token = secrets.token_urlsafe(100)
        return token[:128]

    def __print_new_authorisation_url(self, code_challenge: str):
        url = f'https://myanimelist.net/v1/oauth2/authorize?response_type=code&client_id={self.client_id}&code_challenge={code_challenge}'
        print(f'Authorise your application by clicking here: {url}\n')

    def __generate_new_token(self, authorisation_code: str, code_verifier: str) -> dict:

        url = 'https://myanimelist.net/v1/oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': authorisation_code,
            'code_verifier': code_verifier,
            'grant_type': 'authorization_code'
        }

        response = requests.post(url, data)
        response.raise_for_status()  # Check whether the request contains errors

        token = response.json()
        response.close()
        return token

    def __load_token(self):
        if self.token_saver_loader_params is None:
            return self.token_loader()
        else:
            return self.token_loader(self.token_saver_loader_params)

    def __save_token(self, token_info: MALTokenInfo):
        if self.token_saver_loader_params is None:
            return self.token_saver(token_info)
        else:
            return self.token_saver(token_info, self.token_saver_loader_params)

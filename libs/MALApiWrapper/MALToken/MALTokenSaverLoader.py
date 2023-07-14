import json
from ..dataclass.MALTokenDataclass import MALTokenInfo
import os


def convert_dataclass_to_dict(token_info: MALTokenInfo) -> dict:
    return {
        "token_type": token_info.token_type,
        "expires_in": token_info.expires_in,
        "access_token": token_info.access_token,
        "refresh_token": token_info.refresh_token
    }


class BaseMalTokenInfoSaverLoader:
    def __init__(self, params: dict | None = None):
        self.params = params

    def token_loader(self) -> MALTokenInfo | None:
        ...

    def token_saver(self, token_info: MALTokenInfo) -> bool:
        ...


class StandartMalTokenInfoSaverLoader(BaseMalTokenInfoSaverLoader):

    def __init__(self, params: dict | None = None):
        super().__init__(params)

    def token_loader(self) -> MALTokenInfo | None:
        try:
            target_dir = self.__get_target_dir()
            if self.params is None:
                file_path = os.path.join(target_dir, 'token_mal.json')
            else:
                file_path = os.path.join(target_dir, f'token_{self.params["user_id"]}.json')

            with open(file_path, 'r') as f:
                data = json.load(f)
            return MALTokenInfo(**data)

        except FileNotFoundError:
            return None

    def token_saver(self, token_info: MALTokenInfo):
        target_dir = self.__get_target_dir()
        if self.params is None:
            file_path = os.path.join(target_dir, 'token_mal.json')
        else:
            file_path = os.path.join(target_dir, f'token_{self.params["user_id"]}.json')

        with open(file_path, 'w') as file:
            json.dump(convert_dataclass_to_dict(token_info), file, indent=4)

    @staticmethod
    def __get_target_dir():
        current_dir = os.path.dirname(os.path.abspath(__file__))
        target_dir = os.path.abspath(os.path.join(current_dir, '../..', '..'))
        return target_dir
